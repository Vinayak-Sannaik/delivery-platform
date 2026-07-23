import asyncio
import logging
import uuid

import httpx
from fastapi import HTTPException, Request, Response

logger = logging.getLogger(__name__)

TIMEOUT = httpx.Timeout(60.0)

MAX_RETRIES = 3
INITIAL_DELAY = 1  # seconds


async def forward_request(
    request: Request,
    target_base_url: str,
    path: str,
) -> Response:
    
    idempotency_key = request.headers.get("idempotency-key")
    if not idempotency_key:
        idempotency_key = str(uuid.uuid4())
    
    target_url = f"{target_base_url.rstrip('/')}/{path.lstrip('/')}"

    body = await request.body()

    headers = {}
    
    headers["idempotency-key"] = idempotency_key

    if content_type := request.headers.get("content-type"):
        headers["content-type"] = content_type

    if authorization := request.headers.get("authorization"):
        headers["authorization"] = authorization

    if accept := request.headers.get("accept"):
        headers["accept"] = accept

    logger.info("=" * 50)
    logger.info("Incoming path: %s", request.url.path)
    logger.info("Captured path: %s", path)
    logger.info("Target URL: %s", target_url)
    logger.info("Method: %s", request.method)
    logger.info("=" * 50)

    async with httpx.AsyncClient(
        timeout=TIMEOUT,
        follow_redirects=True,
    ) as client:

        delay = INITIAL_DELAY

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(
                    "Proxy attempt %d/%d",
                    attempt,
                    MAX_RETRIES,
                )

                response = await client.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    params=request.query_params,
                    content=body,
                )

                logger.info(
                    "Downstream status: %s",
                    response.status_code,
                )

                # Success or client error -> don't retry
                if response.status_code not in (502, 503, 504):
                    return Response(
                        content=response.content,
                        status_code=response.status_code,
                        media_type=response.headers.get("content-type"),
                        headers={
                            k: v
                            for k, v in response.headers.items()
                            if k.lower()
                            not in ("content-length", "transfer-encoding")
                        },
                    )

                logger.warning(
                    "Received %s from downstream. Retrying in %s second(s)...",
                    response.status_code,
                    delay,
                )

            except httpx.RequestError as exc:
                logger.warning(
                    "Network error (%s). Retrying in %s second(s)...",
                    type(exc).__name__,
                    delay,
                )

            if attempt < MAX_RETRIES:
                await asyncio.sleep(delay)
                delay *= 2

        logger.error("All retry attempts exhausted.")

        raise HTTPException(
            status_code=502,
            detail="Downstream service unavailable after retries.",
        )