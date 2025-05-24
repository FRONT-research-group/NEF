from app.utils.location_db_data_handler import LocationDbDataHandler
from app.utils.logger import get_app_logger
from app.config import Settings
from app.utils.location_db_data_handler import location_db_data_handler as db_handler

log = get_app_logger()

settings = Settings()


async def startup_db_handler() -> None:
    log.info("Mongo's DB Client instantiation process begin")
    if settings.mongo_db_uri is not None:
        temp_db_handler = await LocationDbDataHandler.client_from_uri(settings.mongo_db_uri,settings.mongo_db_name,settings.mongo_collection_name)
    elif settings.mongo_db_ip is not None and settings.mongo_db_port is not None:
        temp_db_handler = await LocationDbDataHandler.client_from_ip_and_port(settings.mongo_db_ip,settings.mongo_db_port,settings.mongo_db_name,settings.mongo_collection_name)
    else:
        raise RuntimeError("Could not initialize mongo's db client. Check the connection client settings.")
    
    db_handler.client = temp_db_handler.client
    db_handler.db = temp_db_handler.client
    db_handler.collection = temp_db_handler.collection
    try:
        await db_handler.client.admin.command("ping")
    except Exception as exc:
        log.error(f"Mongo's DB Client instantiation process failed: {exc}")
        raise RuntimeError("Could not connect to mongo database. Check the connection settings.")
    log.info("Mongo's DB Client instantiation process finished successfully")

async def cleanup_db_handler() -> None:
    log.info("Mongo's DB Client cleanup process begin")
    if db_handler.client:
        db_handler.client.close()
    log.info("Mongo's DB Client cleanup process finished successfully")