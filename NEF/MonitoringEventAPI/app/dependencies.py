from app.utils.db_data_handler import DbDataHandler
from app.utils.logger import get_app_logger
from app.config import get_settings
from app.utils.db_data_handler import db_data_handler as db_handler

settings = get_settings()

log = get_app_logger()


async def startup_db_handler() -> None:
    log.info("Mongo's DB Client instantiation process begin")
    if settings.mongo_db_uri is not None:
        temp_db_handler = await DbDataHandler.client_from_uri(settings.mongo_db_uri,settings.mongo_db_name,settings.mongo_location_collection_name)
    elif settings.mongo_db_ip is not None and settings.mongo_db_port is not None:
        temp_db_handler = await DbDataHandler.client_from_ip_and_port(settings.mongo_db_ip,settings.mongo_db_port,settings.mongo_db_name,settings.mongo_location_collection_name)
    else:
        raise RuntimeError("Could not initialize mongo's db client. Check the connection client settings.")
    
    db_handler.client = temp_db_handler.client
    db_handler.db = temp_db_handler.db
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
        await db_handler.client.close()
    log.info("Mongo's DB Client cleanup process finished successfully")