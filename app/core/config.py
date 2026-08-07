from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    API_NAME: str
    API_VERSION: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DATABASE_URL: str

    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    ENCRYPTION_KEY: str

    LOG_LEVEL: str
    ENVIRONMENT: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()