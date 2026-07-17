from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    IDENTITY_SERVICE_URL: str = "http://identity-service:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()