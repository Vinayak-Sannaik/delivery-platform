from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    IDENTITY_SERVICE_URL: str = "http://identity-service:8000"
    CATALOG_SERVICE_URL:  str = "http://catalog-service:8002"
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()