from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from contextlib import asynccontextmanager

from app.database.db_helper import db_helper
from app.core.config import settings

from app.routers.uav import router as api_uav
from app.routers.operating_time_log import router as api_operating_time_log
from app.routers.maintenance_type import router as api_maintenance_type
from app.routers.maintenance_record import router as api_maintenance_record
from app.routers.web.dashboard import router as dashboard_router
from app.routers.web.add_new_uav import router as add_uav_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #shutdown
    await db_helper.dispose()

main_app = FastAPI(lifespan=lifespan)
main_app.mount('/static', StaticFiles(directory=settings.paths.static_dir), name="static")
main_app.include_router(api_uav, prefix=settings.api.prefix)
main_app.include_router(api_operating_time_log, prefix=settings.api.prefix)
main_app.include_router(api_maintenance_type, prefix=settings.api.prefix)
main_app.include_router(api_maintenance_record, prefix=settings.api.prefix)
main_app.include_router(dashboard_router)
main_app.include_router(add_uav_router)


if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
