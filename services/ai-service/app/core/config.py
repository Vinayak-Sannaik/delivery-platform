from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ai-service"
    app_env: str = "development"
    debug: bool = True

    ai_enabled: bool = True

    catalog_service_url: str

    llm_provider: str = "gemini"
    llm_model: str = ""

    gemini_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()