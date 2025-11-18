from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import monitoring_event
from app.dependencies import startup_db_handler, cleanup_db_handler
from app.config import get_settings
from app.utils.logger import get_app_logger

settings = get_settings()

logger = get_app_logger()
logger.info("Starting NEF Monitoring Event API")
logger.info(f"Host: {settings.host}, Port: {settings.port}")
logger.info(f"MongoDB URI: {settings.mongo_db_uri}")
logger.info(
    f"MongoDB IP: {settings.mongo_db_ip}, Port: {settings.mongo_db_port}")
logger.info(f"MongoDB Name: {settings.mongo_db_name}")
logger.info(
    f"MongoDB Location Collection Name: {settings.mongo_location_collection_name}"
)
logger.info(
    f"MongoDB Subscription Collection Name: {settings.mongo_subscription_collection_name}"
)
logger.info(f"CAMARA CASE: {settings.camara_case}")
#logger.info(f"Cache Collection Name: {settings.cache_collection_name}")
logger.info(
    f"Map MSISDN to IMSI Collection Name: {settings.map_msisdn_imsi_collection_name}"
)
logger.info(
    f"Map Cell ID to Polygon Collection Name: {settings.map_cellId_to_polygon_collection_name}"
)
logger.info(f"Auth Enabled: {settings.auth_enabled}")
if settings.auth_enabled:
    logger.info(f"Public Key Path: {settings.pub_key_path}")
    logger.info(f"Algorithm: {settings.algorithm}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_handler()
    yield
    await cleanup_db_handler()


app = FastAPI(lifespan=lifespan)

app.include_router(monitoring_event.router, prefix="/3gpp-monitoring-event/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
