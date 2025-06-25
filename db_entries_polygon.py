from pymongo import AsyncMongoClient
 
client = AsyncMongoClient("mongodb://0.0.0.0:27018/")  
db = client["amf_logs"]
collection = db["cell_to_polygons"]
 
collection.delete_many({})
 
#_id is cellId that will map to points in order to create a Polygon.
cell_entries = {
    "_id": "000000010",
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
}


# "coordinates": [[
#             [23.818348, 37.998598],  # Point 1 (top-left)
#             [23.819458, 37.997698],  # Point 2 (bottom-right)
#             [23.817000, 37.997000],  # Point 3 (new, e.g., bottom-left)
#             [23.818348, 37.998598]   # Close by repeating Point 1
#         ]]
 
# Insert into the collection
result = collection.insert_many(cell_entries)


print(f"Inserted {len(result.inserted_ids)} polygon entries into 'cell_polygons' collection.")