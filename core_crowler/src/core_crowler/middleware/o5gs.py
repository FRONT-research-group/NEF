import json
from pymongo import MongoClient
from core_crowler.utils.logger import setup_logger

logger = setup_logger(logger_name="o5gs_middleware")

class O5GSMiddleware():
    def __init__(self, mongo_uri="mongodb://localhost:27017", db_name="amf_logs", collection_name="location_info"):
        try:
            self.mongo_client = MongoClient(mongo_uri)
            self.mongo_db = self.mongo_client[db_name]
            self.mongo_collection = self.mongo_db[collection_name]
            logger.info("[MONGODB] Connected to MongoDB")
        except Exception as e:
            logger.error(f"[MONGODB] Failed to connect: {e}")
            self.mongo_collection = None

    def write_location_info(self, event):
        if self.mongo_collection is not None:
            refined_event = {
                "_id": event["_id"],
                "cellId": event["amf_info"]["ueLocation"]["nrLocation"]["ncgi"]["nrCellId"],
                "trackingAreaId": event["amf_info"]["ueLocation"]["nrLocation"]["tai"]["tac"],
                "plmnId": event["amf_info"]["guami"]["plmnId"], # TODO: Check if this is correct
                "routingAreaId": None,
                "enodeBId": None,
                "twanId": None,
                "UELocationTimestamp": event["amf_info"]["ueLocation"]["nrLocation"]["ueLocationTimestamp"]
            }
            try:
                self.mongo_collection.replace_one({"_id": event["_id"]}, refined_event, upsert=True)
                logger.info(f"[MONGODB] Stored location for IMSI: {event['_id']}")
                logger.info(json.dumps(refined_event, indent=4))
            except Exception as e:
                logger.error(f"[MONGODB] Failed to insert location: {e}")
