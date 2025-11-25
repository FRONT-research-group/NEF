import os
from opencapif_sdk import capif_provider_connector, api_schema_translator
from app.utils.logger import get_app_logger

logger = get_app_logger(__name__)


#API_HOST = os.getenv('API_HOST', '10.220.2.43')
PROJECT_API_NAME = os.getenv('PROJECT_API_NAME', '')
PROVIDER_API_HOST = os.getenv('PROVIDER_API_HOST', '127.0.0.1')
PROVIDER_API_PORT = os.getenv('PROVIDER_API_PORT', '8001')
PROVIDER_CONFIG_FILE = os.getenv('PROVIDER_CONFIG_FILE', './provider_config_sample.json')
PROVIDER_OPENAPI_FILE = os.getenv('PROVIDER_OPENAPI_FILE', './openapi.yaml')
PROVIDER_API_DESC_FILE = os.getenv('PROVIDER_API_DESC_FILE', './3gpp-monitoring-event.json') # should match the prefix of the URL
#API_DESC_FILE = os.getenv('API_DESC_FILE', './provider-app.json') # should match the prefix of the URL

if PROJECT_API_NAME is None or PROJECT_API_NAME == "":
    API_URL = f"https://{PROVIDER_API_HOST}:{PROVIDER_API_PORT}/3gpp-monitoring-event/v1"
else:
    API_URL = f"https://{PROVIDER_API_HOST}:{PROVIDER_API_PORT}/3gpp-monitoring-event-{PROJECT_API_NAME}/v1"
    api_name_with_suffix = f"-{PROJECT_API_NAME}.json"
    PROVIDER_API_DESC_FILE = PROVIDER_API_DESC_FILE.replace(".json",api_name_with_suffix) 
#API_URL = f"https://{API_HOST}:{API_PORT}/provider-app/v1"

def onboard_provider() -> None:
    """
    Demonstrates the process of onboarding a provider and publishing services to CAPIF NEF.
    This function performs the following steps:
    1. Initializes the CAPIF provider connector using the specified configuration file.
    2. Onboards the provider to the CAPIF system.
    3. Translates the OpenAPI schema and builds the API description.
    4. Sets the API description path and retrieves CAPIF IDs for APF and AEF.
    5. Prepares the publish request with APF and AEF IDs, and supported features.
    6. Publishes the provider's services to CAPIF.
    
    Raises:
        Any exceptions raised by the connector or translator methods.
    """

    capif_connector = capif_provider_connector(config_file=PROVIDER_CONFIG_FILE)
    
    capif_connector.onboard_provider()

    translator = api_schema_translator(PROVIDER_OPENAPI_FILE)
    translator.build(API_URL, "0", "0")


    capif_connector.api_description_path = PROVIDER_API_DESC_FILE
    apf = capif_connector.provider_capif_ids["APF-1"]

    #TODO enhancne to support a list of AEFs
    aef = capif_connector.provider_capif_ids["AEF-1"]
    
    capif_connector.publish_req['publisher_apf_id'] = apf
    capif_connector.publish_req['publisher_aefs_ids'] = [aef]
    capif_connector.supported_features ="0"

    capif_connector.publish_services()
    logger.info("Publication of provider's service is completed")
    
def offboard_provider() -> None:
    capif_connector = capif_provider_connector(config_file=PROVIDER_CONFIG_FILE)
    capif_connector.offboard_provider()
    
    logger.info("Offboarding of the provider is completed")

if __name__ == "__main__":
    onboard_provider()
