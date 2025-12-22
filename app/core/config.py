from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
import os
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(project_root, ".env"))

class ApiPrefix(BaseModel):
    prefix: str = "/api"

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

class PathConfig(BaseModel):
    templates_dir: str = os.path.join(project_root, "templates")
    static_dir: str = os.path.join(project_root, "static")

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
    paths: PathConfig = PathConfig()

settings = Settings()

print(settings.paths.static_dir)
