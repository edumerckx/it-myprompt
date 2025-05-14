from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_API_URL: str
    OPENROUTER_MODEL: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str
    LOGGER_LEVEL: str
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
