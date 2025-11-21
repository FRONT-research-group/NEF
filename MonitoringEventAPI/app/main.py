from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import monitoring_event
from app.dependencies import startup_db_handler, cleanup_db_handler
from app.config import get_settings
from app.utils.logger import get_app_logger

settings = get_settings()

logger = get_app_logger()
logger.info("Starting NEF Monitoring Event API")
logger.info("Host: %s, Port: %s", settings.host, settings.port)
logger.info("MongoDB URI: %s", settings.mongo_db_uri)
logger.info("MongoDB IP: %s, Port: %s", settings.mongo_db_ip, settings.mongo_db_port)
logger.info("MongoDB Name: %s", settings.mongo_db_name)
logger.info("MongoDB Location Collection Name: %s", settings.mongo_location_collection_name)
logger.info("MongoDB Subscription Collection Name: %s", settings.mongo_subscription_collection_name)
logger.info("CAMARA CASE: %s", settings.camara_case)
logger.info("Map MSISDN to IMSI Collection Name: %s", settings.map_msisdn_imsi_collection_name)
logger.info("Map Cell ID to Polygon Collection Name %s:", settings.map_cellId_to_polygon_collection_name)
logger.info("Auth Enabled: %s", settings.auth_enabled)
if settings.auth_enabled:
    logger.info(f"Public Key Path: {settings.pub_key_path}")
    logger.info(f"Algorithm: {settings.algorithm}")
logger.info("Project API Name: %s",settings.project_api_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_handler()
    yield
    await cleanup_db_handler()


app = FastAPI(lifespan=lifespan)

if settings.project_api_name is None or settings.project_api_name == "":
    app.include_router(monitoring_event.router, prefix="/3gpp-monitoring-event/v1")
else:
    app.include_router(monitoring_event.router, prefix="/3gpp-monitoring-event-" + settings.project_api_name +"/v1")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
