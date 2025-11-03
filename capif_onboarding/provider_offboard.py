import os
from opencapif_sdk import capif_provider_connector

PROVIDER_CONFIG_FILE = os.getenv('PROVIDER_CONFIG_FILE', './provider_config_sample.json')

def offboard_capif_nef_connector():
    capif_connector = capif_provider_connector(config_file=PROVIDER_CONFIG_FILE)
    capif_connector.offboard_provider()
    
    print("OFFBOARD the provider completed")

if __name__ == "__main__":
    offboard_capif_nef_connector()
