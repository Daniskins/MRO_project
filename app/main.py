from fastapi import FastAPI
from api import router as api_router
from core.config import settings

app = FastAPI()
app.include_router(api_router,
                   prefix=settings.api.prefix)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
