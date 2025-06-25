from pymongo import AsyncMongoClient
from app.config import get_settings
from app.utils.logger import get_app_logger

settings = get_settings()

log = get_app_logger()


class DbDataHandler:
    def __init__(self, client: AsyncMongoClient | None, db_name: str | None, collection_name: str | None):
        if client is None and db_name is None and collection_name is None:
            self.client = None
            self.db = None
            self.collection = None
        else:
            self.client = client
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
    
    @classmethod
    async def client_from_uri(cls,uri:str,db_name:str, collection_name: str) -> "DbDataHandler":
        client = AsyncMongoClient(uri)
        return cls(client,db_name,collection_name)

    @classmethod
    async def client_from_ip_and_port(cls,ip:str,port:int, db_name: str, collection_name: str) -> "DbDataHandler":
        client = AsyncMongoClient(ip,port)
        return cls(client,db_name,collection_name)
    
    async def find_location_by_imsi(self, imsi: str) -> dict | None:
        """Finds location data based on IMSI."""
        self.collection = self.db[settings.mongo_location_collection_name]
        return await self.collection.find_one({"_id": imsi})
    
    async def fetch_report_from_db_cache(self,imsi: str) -> dict | None:
        self.collection = self.db[settings.cache_collection_name]
        return await self.collection.find_one({"_id": imsi},projection={'_id': False})
    
    async def fetch_mapping_from_msisdn_to_imsi(self,msisdn: str) -> dict | None:
        self.collection = self.db[settings.map_msisdn_imsi_collection_name]
        return await self.collection.find_one({"msisdn": msisdn},projection={'msisdn' : False})
    
    async def fetch_mapping_from_cell_id_to_polygon(self,cell_id: str) -> dict | None:
        self.collection = self.db[settings.map_cellId_to_polygon_collection_name]
        return await self.collection.find_one({"_id": cell_id},projection={'_id': False})
    
    async def register_subscription_in_db(self, af_id:str, subscription_id:str, monitoring_sub_req: dict) -> None:
        """Register a new subscription in database."""
        self.collection = self.db[settings.mongo_subscription_collection_name]
        document = {"_id": subscription_id, "af_id": af_id, "monitoringEventSubscription":monitoring_sub_req}
        try:
            await self.collection.insert_one(document)
            log.info("Document inserted successfully.")
        except Exception as exc:
            log.error("Error during insertion of the document.",exc_info=exc)
    
    async def fetch_subscriptions_for_af_id(self, af_id: str) -> list | None:
        self.collection = self.db[settings.mongo_subscription_collection_name]
        try:
            
            results = self.collection.find({"af_id": af_id},projection={'_id': True, "af_id": False})
            return await results.to_list(length=None) 
        except TypeError as exc:
            log.error(f"Error while fetching the subscriptions for {af_id}.",exc_info=exc)
    
    async def fetch_unique_subscription_for_af_id(self, af_id: str, subscription_id: str) -> dict | None:
        self.collection = self.db[settings.mongo_subscription_collection_name]
        try:
            return await self.collection.find_one({"af_id": af_id, "_id": subscription_id}, projection={"af_id": False})
        except TypeError as exc:
            log.error(f"Error while fetching the specific id {subscription_id} for af {af_id}.",exc_info=exc)
    
    async def delete_unique_subscription_for_af_id(self, af_id: str, subscription_id: str) -> None:
        self.collection = self.db[settings.mongo_subscription_collection_name]
        await self.collection.delete_one({"af_id": af_id, "_id": subscription_id})


        
db_data_handler = DbDataHandler(None,None,None)

async def get_db_data_handler() -> DbDataHandler:
    return db_data_handler