from pymongo import MongoClient
 
# MongoDB connection
client = MongoClient("mongodb://0.0.0.0:27018/")
db = client["amf_logs"]
collection = db["imsi_to_phone_number"]
 
collection.delete_many({})

#_id as imsi
mappings = [
    {
        "_id": "001010143245445",
        "msisdn": "306912345678"
    },
    {
        "_id": "987654321098765",
        "msisdn": "306911112222"
    }
]
 
result = collection.insert_many(mappings)
client.close()
print(f"Inserted {len(result.inserted_ids)} mappings.")