import httpx
import asyncio
from app.core.config import settings
import time

class SystemStatusService:

    SERVICES = {
        "Identity": f"{settings.IDENTITY_SERVICE_URL}/health",
        "Catalog": f"{settings.CATALOG_SERVICE_URL}/health",
        "Order": f"{settings.ORDER_SERVICE_URL}/health",
        "Delivery": f"{settings.DELIVERY_SERVICE_URL}/health",
        "Notification": f"{settings.NOTIFICATION_SERVICE_URL}/health",
    }

    async def check_service(
        self,
        client: httpx.AsyncClient,
        name: str,
        url: str,
        retries=1,
    ):
        start = time.perf_counter(retries)

        for attempt in range():
            try:
                response = await client.get(
                    url,
                    timeout=30,
                )

                if response.status_code == 200:
                    latency = (
                        time.perf_counter() - start
                    ) * 1000

                    return {
                        "name": name,
                        "status": "healthy",
                        "latency_ms": round(latency, 2),
                         "error": None,
                    }

                print(
                    f"{name} returned {response.status_code}, retrying..."
                )

            except Exception as e:
                print(
                    f"{name} error: {type(e).__name__}: {repr(e)}"
                )

            await asyncio.sleep(5)

        return {
            "name": name,
            "status": "starting",
            "latency_ms": None,
            "error": f"Last response: {response.status_code}",
        }
    
    async def get_status(self, retries: int = 1,):
        async with httpx.AsyncClient() as client:

            tasks = [
                self.check_service(
                    client,
                    name,
                    url,
                    retries,
                )
                for name, url in self.SERVICES.items()
            ]

            services = await asyncio.gather(*tasks)

            return [
                {
                    "name": "Gateway",
                    "status": "healthy",
                    "latency_ms": 0,
                },
                *services,
            ]
            
    async def warmup(self):
        max_attempts = 12

        for attempt in range(max_attempts):

            services = await self.get_status()

            non_gateway_services = [
                service
                for service in services
                if service["name"] != "Gateway"
            ]

            all_ready = all(
                service["status"] == "healthy"
                for service in non_gateway_services
            )

            if all_ready:
                return services

            print(
                f"Warmup attempt {attempt + 1}/{max_attempts} failed. Retrying..."
            )

            await asyncio.sleep(6)

        return services