
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import monitoring_event
from app.config import Settings
from app.dependencies import startup_db_handler,cleanup_db_handler

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_handler()
    yield
    await cleanup_db_handler()

app = FastAPI(lifespan=lifespan)

app.include_router(monitoring_event.router, prefix="/3gpp-monitoring-event/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host=settings.host,port=settings.port)