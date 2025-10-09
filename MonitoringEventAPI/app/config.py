from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8080
    log_directory_path: str = "./app/log/"
    log_filename_path: str = f"{log_directory_path}app_logger"
    mongo_db_uri: str | None = None
    mongo_db_ip: str | None = None
    mongo_db_port: int | None = None
    mongo_db_name: str | None = None
    mongo_location_collection_name: str
    mongo_subscription_collection_name: str
    cache_in_mongo: bool | None = False
    cache_collection_name: str | None
    map_msisdn_imsi_collection_name: str | None
    map_cellId_to_polygon_collection_name: str | None
    auth_enabled: bool = True
    pub_key_path: str | None = None
    algorithm: str | None = "RS256"

settings = Settings()

def get_settings() -> Settings:
    """
    Retrieve the current application settings.

    Returns:
        Settings: An instance containing the application's configuration settings.
    """
    return settings