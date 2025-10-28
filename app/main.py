from fastapi import FastAPI
import uvicorn
from api import router as api_router
from app.core.models.db_helper import db_helper
from core.config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #shutdown
    db_helper.dispose()



main_app = FastAPI(
    lifespan=lifespan
)
main_app.include_router(api_router,
                        prefix=settings.api.prefix)


@main_app.get("/")
async def root():
    return {"message": "Hello World"}


@main_app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run(main_app,
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
