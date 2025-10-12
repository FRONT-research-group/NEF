import pytest

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    docker0_ip: str
    nef_host_port: int
    test_server_host_port: int
    nef_base_url: str
    test_server_url: str

    model_config = SettingsConfigDict(env_file=".env")

@pytest.fixture(scope="session", autouse=True)
def test_settings() -> Settings:
    """Loads test settings using the Settings Pydantic class."""
    return Settings()

