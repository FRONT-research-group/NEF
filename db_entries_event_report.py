from pymongo import MongoClient
 
# MongoDB connection
client = MongoClient("mongodb://0.0.0.0:27018/")
db = client["amf_logs"]
collection = db["cache_reports"]
 
collection.delete_many({})

#_id as imsi
report = [{
  "_id" : "001010143245445",
  "msisdn": "306912345678",
  "locationInfo": {
    "cellId": "000000010",
    "trackingAreaId": "TA-GREECE-002",
    "enodeBId": "ENB-PIREAS-010",
    "routingAreaId": "RA-CENTRAL-ATH",
    "plmnId": {
      "mcc": "202",
      "mnc": "01"
    },
    "twanId": None,
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
  },
  "monitoringType": "LOCATION_REPORTING",
  "eventTime": "2025-06-23T20:47:22.000000"
}]
 
result = collection.insert_many(report)
client.close()
print(f"Inserted {len(result.inserted_ids)} mappings.")