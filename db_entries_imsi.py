from pymongo import AsyncMongoClient
 
# MongoDB connection
client = AsyncMongoClient("mongodb://mongo:27017/")
db = client["amf_logs"]
collection = db["imsi_to_phone_number"]
 
# Optional: clear old test data
collection.delete_many({})
 
# Sample entries
mappings = [
    {
        "imsi": "imsi-123456789012345",
        "phoneNumber": "+306912345678"
    },
    {
        "imsi": "imsi-987654321098765",
        "phoneNumber": "+306911112222"
    }
]
 
# Insert into DB
result = collection.insert_many(mappings)
 
# Log με την δική σου method
print(f"Inserted {len(result.inserted_ids)} mappings.")