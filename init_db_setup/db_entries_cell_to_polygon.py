from pymongo import MongoClient
 
# MongoDB connection
client = MongoClient("mongodb://0.0.0.0:27018/")
db = client["amf_logs"]
collection = db["cell_to_polygons"]
 
collection.delete_many({})

#_id as cellid
report = [{
  "_id" : "001234501",
  "geographicArea": {
      "polygon": {
        "point_list": {
          "geographical_coords": [
            {
              "lon": 23.7275,
              "lat": 37.9838
            },
            {
              "lon": 23.75,
              "lat": 37.98
            },
            {
              "lon": 23.73,
              "lat": 37.97
            },
            {
              "lon": 23.71,
              "lat": 37.975
            }
          ]
        }
      }
    }
}]
 
result = collection.insert_many(report)
client.close()
print(f"Inserted {len(result.inserted_ids)} mappings.")