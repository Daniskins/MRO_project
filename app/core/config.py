from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn, Field
import os
from dotenv import load_dotenv

# load .env (если нужно)
project_root = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(project_root, ".env"))

class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"

class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class GunicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    timeout: int = 900

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(project_root, ".env"),
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        case_sensitive=False,
    )
    api: ApiPrefix = ApiPrefix()
    run: RunConfig = RunConfig()
    db: DatabaseConfig

settings = Settings()
