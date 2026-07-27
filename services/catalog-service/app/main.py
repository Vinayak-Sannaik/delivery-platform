from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.grpc.server import start_grpc_server
from app.routers.category import router as category_router
from app.routers.menu_item import router as menu_item_router
from app.routers.restaurant import router as restaurant_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    grpc_server = await start_grpc_server()

    try:
        yield
    finally:
        await grpc_server.stop(grace=5)


app = FastAPI(
    title="Catalog Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(restaurant_router)
app.include_router(category_router)
app.include_router(menu_item_router)


@app.get("/health")
def health():
    return {"status": "ok"}