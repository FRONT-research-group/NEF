from contextlib import asynccontextmanager
from fastapi import FastAPI

# from app.routers import monitoring_event
from app.dependencies import startup_db_handler, cleanup_db_handler, onboard_to_capif, offboard_from_capif
from app.config import get_settings
from app.utils.logger import get_app_logger

settings = get_settings()


logger = get_app_logger(__name__)
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
    logger.info("Provider folder path: %s", settings.provider_folder_path)
    logger.info("Algorithm: %s", settings.algorithm)
    
    onboard_to_capif()

#TODO check proper way of importing when i depend on env variables
from app.routers import monitoring_event





@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_handler()
    yield
    await cleanup_db_handler()
    if settings.auth_enabled:
        await offboard_from_capif()


app = FastAPI(lifespan=lifespan)

app.include_router(monitoring_event.router, prefix="/3gpp-monitoring-event/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
