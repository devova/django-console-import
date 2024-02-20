from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_file=".env", env_file_encoding="utf-8", extra="ignore"
    # )

    name: str
    user: str
    password: SecretStr
    host: str
    port: int = 5432


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    debug: bool = False
    db: Database


validated_env = Settings()
