from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    
    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str
    
    CATALOG_GRPC_ADDRESS: str = "host.docker.internal:50051"
    
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    
    CATALOG_SERVICE_URL: str
    CATALOG_MODE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()