from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    IDENTITY_SERVICE_URL: str
    CATALOG_SERVICE_URL: str
    ORDER_SERVICE_URL: str
    DELIVERY_SERVICE_URL: str
    NOTIFICATION_SERVICE_URL: str
    
    REDIS_URL: str
    REDIS_TOKEN: str
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()