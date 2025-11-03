import os
from opencapif_sdk import capif_provider_connector

PROVIDER_CONFIG_FILE = os.getenv('PROVIDER_CONFIG_FILE', './provider_config_sample.json')

def showcase_capif_nef_connector():
    """

    """
    capif_connector = capif_provider_connector(config_file=PROVIDER_CONFIG_FILE)

    capif_connector.unpublish_service()
    print("COMPLETED")


if __name__ == "__main__":
    # Register a NEF to CAPIF. This should happen exactly once
    showcase_capif_nef_connector()
