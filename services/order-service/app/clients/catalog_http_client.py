import logging
import time
from enum import Enum
from typing import Awaitable, Callable, TypeVar

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import settings

logger = logging.getLogger(__name__)

RETRY_STATUS_CODES = {502, 503, 504}

T = TypeVar("T")


def should_retry(exception: Exception) -> bool:
    if isinstance(
        exception,
        (httpx.ConnectError, httpx.ReadTimeout),
    ):
        return True

    if isinstance(exception, httpx.HTTPStatusError):
        return exception.response.status_code in RETRY_STATUS_CODES

    return False


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitOpenError(Exception):
    """Raised when the circuit breaker is open."""


class CatalogCircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 30.0,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.opened_at: float | None = None

        # Prevent multiple requests from becoming
        # HALF_OPEN probes simultaneously.
        self.half_open_probe_in_progress = False

    def _can_attempt(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            if self.opened_at is None:
                return False

            elapsed = time.monotonic() - self.opened_at

            if elapsed >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_probe_in_progress = False

                logger.info(
                    "Catalog circuit transitioned OPEN -> HALF_OPEN"
                )

            else:
                return False

        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_probe_in_progress:
                return False

            self.half_open_probe_in_progress = True

        return True

    def _record_success(self) -> None:
        if self.state == CircuitState.HALF_OPEN:
            logger.info(
                "Catalog circuit transitioned HALF_OPEN -> CLOSED"
            )

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.opened_at = None
        self.half_open_probe_in_progress = False

    def _record_failure(self) -> None:
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.opened_at = time.monotonic()
            self.half_open_probe_in_progress = False

            logger.error(
                "Catalog circuit transitioned HALF_OPEN -> OPEN"
            )

            return

        self.failure_count += 1

        logger.warning(
            "Catalog circuit failure count: %s/%s",
            self.failure_count,
            self.failure_threshold,
        )

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = time.monotonic()

            logger.error(
                "Catalog circuit transitioned CLOSED -> OPEN"
            )

    async def call(
        self,
        operation: Callable[[], Awaitable[T]],
    ) -> T:

        if not self._can_attempt():
            raise CircuitOpenError(
                "Catalog service circuit breaker is OPEN"
            )

        try:
            result = await operation()

            self._record_success()

            return result

        except Exception as exc:
            # Only transient/downstream failures should
            # contribute to circuit breaking.
            if should_retry(exc):
                self._record_failure()

            else:
                # Non-transient errors such as 400/404
                # should not open the circuit.
                if self.state == CircuitState.HALF_OPEN:
                    self.half_open_probe_in_progress = False

            raise


class CatalogHttpClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.CATALOG_SERVICE_URL,
            timeout=httpx.Timeout(10.0),
        )

        self.circuit_breaker = CatalogCircuitBreaker(
            failure_threshold=3,
            recovery_timeout=30,
        )

    async def close(self):
        await self.client.aclose()

    @retry(
        retry=retry_if_exception(should_retry),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=8,
        ),
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(
            logger,
            logging.WARNING,
        ),
        reraise=True,
    )
    async def _get_menu_items(
        self,
        menu_item_ids: list[str],
    ):
        response = await self.client.post(
            "/internal/menu-items",
            json={
                "menu_item_ids": [
                    str(item_id)
                    for item_id in menu_item_ids
                ]
            },
        )

        response.raise_for_status()

        return [
            type(
                "MenuItemDTO",
                (),
                {
                    "id": item["id"],
                    "restaurant_id": item["restaurant_id"],
                    "name": item["name"],
                    "price": item["price"],
                    "is_available": item["is_available"],
                },
            )
            for item in response.json()
        ]

    async def get_menu_items(
        self,
        menu_item_ids: list[str],
    ):
        return await self.circuit_breaker.call(
            lambda: self._get_menu_items(menu_item_ids)
        )

    @retry(
        retry=retry_if_exception(should_retry),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=8,
        ),
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(
            logger,
            logging.WARNING,
        ),
        reraise=True,
    )
    async def _get_restaurant_owner(
        self,
        restaurant_id: str,
    ):
        response = await self.client.get(
            f"/internal/restaurants/{restaurant_id}/owner"
        )

        response.raise_for_status()

        return response.json()

    async def get_restaurant_owner(
        self,
        restaurant_id: str,
    ):
        return await self.circuit_breaker.call(
            lambda: self._get_restaurant_owner(restaurant_id)
        )