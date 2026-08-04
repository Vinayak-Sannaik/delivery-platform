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
    ):
        start = time.perf_counter()

        for attempt in range(6):
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
                    }

                print(
                    f"{name} returned {response.status_code}, retrying..."
                )

            except Exception as e:
                print(
                    f"{name} error: {str(e)}"
                )

            await asyncio.sleep(5)

        return {
            "name": name,
            "status": "starting",
            "latency_ms": None,
        }
    
    async def get_status(self):
        async with httpx.AsyncClient() as client:

            tasks = [
                self.check_service(
                    client,
                    name,
                    url,
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