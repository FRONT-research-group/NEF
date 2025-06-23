from pymongo import AsyncMongoClient
 
# Connect to MongoDB
client = AsyncMongoClient("mongodb://mongo:27017/")  # Change if needed
db = client["amf_logs"]
collection = db["cell_to_polygons"]
 
# Optional: Clear existing data
collection.delete_many({})
 
#  RFC 7946  GeoJSON polygon
#_id is cellId that will map to points in order to create a Polygon.
cell_entries = [
	{
	    "_id": "000000010",
		"coordinates": [[
            [23.818348, 37.998598],  # Point 1 (top-left)
            [23.819458, 37.997698],  # Point 2 (bottom-right)
            [23.817000, 37.997000],  # Point 3 (new, e.g., bottom-left)
            [23.818348, 37.998598]   # Close by repeating Point 1
        ]]
	}
]
 
# Insert into the collection
result = collection.insert_many(cell_entries)
# Log με την δική σου method
print(f"Inserted {len(result.inserted_ids)} polygon entries into 'cell_polygons' collection.")