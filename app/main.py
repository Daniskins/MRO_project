from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from contextlib import asynccontextmanager

from app.core.models.db_helper import db_helper
from app.core.config import settings
from app.core.paths import STATIC_DIR

from app.routers.plane import router as api_plane
from app.routers.web.dashboard import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #shutdown
    db_helper.dispose()

main_app = FastAPI(lifespan=lifespan)
main_app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
main_app.include_router(api_plane,
                        prefix=settings.api.prefix)
main_app.include_router(dashboard_router)


if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
