from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    max_filters: int = 5

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()