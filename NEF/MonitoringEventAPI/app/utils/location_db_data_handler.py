from pymongo import AsyncMongoClient

class LocationDbDataHandler:
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
    async def client_from_uri(cls,uri:str,db_name:str, collection_name: str) -> "LocationDbDataHandler":
        client = AsyncMongoClient(uri)
        return cls(client,db_name,collection_name)

    @classmethod
    async def client_from_ip_and_port(cls,ip:str,port:int, db_name: str, collection_name: str) -> "LocationDbDataHandler":
        client = AsyncMongoClient(ip,port)
        return cls(client,db_name,collection_name)
    
    async def find_location_by_imsi(self, imsi: str) -> dict | None:
        """Finds location data based on IMSI."""
        return await self.collection.find_one({"_id": imsi})
    
location_db_data_handler = LocationDbDataHandler(None,None,None)

async def get_location_data_handler() -> LocationDbDataHandler:
    return location_db_data_handler