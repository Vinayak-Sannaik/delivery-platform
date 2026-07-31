import grpc

from app.grpc.catalog_service import CatalogServiceServicer
from app.grpc import catalog_pb2_grpc


async def start_grpc_server():

    server = grpc.aio.server()

    catalog_pb2_grpc.add_CatalogServiceServicer_to_server(
        CatalogServiceServicer(),
        server,
    )

    server.add_insecure_port("[::]:50051")

    await server.start()

    return server