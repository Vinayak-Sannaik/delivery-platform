from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_USERNAME: str | None = None
    KAFKA_PASSWORD: str | None = None
    KAFKA_SECURITY_PROTOCOL: str = "PLAINTEXT"
    KAFKA_SASL_MECHANISM: str | None = None
    KAFKA_SSL_CA_LOCATION: str | None = None
    
    REDIS_URL: str 
    REDIS_TOKEN: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()