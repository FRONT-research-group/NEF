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


settings = Settings()

def get_settings() -> Settings:
    return settings