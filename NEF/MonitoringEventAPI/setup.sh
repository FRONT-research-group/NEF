#!/bin/sh
echo "HOST=0.0.0.0" > .env
echo "PORT=8000" >> .env
echo "LOG_DIRECTORY_PATH=./app/log1/" >> .env 
echo "LOG_FILENAME_PATH=./app/log1/app_logger" >> .env
echo "MONGO_DB_URI=mongodb://mongo:27017/" >> .env
echo "MONGO_DB_IP=127.0.0.1" >> .env
echo "MONGO_DB_PORT=27017" >> .env
echo "MONGO_DB_NAME=amf_logs" >> .env
echo "MONGO_LOCATION_COLLECTION_NAME=location_info" >> .env
echo "MONGO_SUBSCRIPTION_COLLECTION_NAME=subscriptions" >> .env
echo "CACHE_IN_MONGO=True" >> .env
echo "CACHE_COLLECTION_NAME=cache_reports" >> .env
echo "MAP_MSISDN_IMSI_COLLECTION_NAME=imsi_to_phone_number" >> .env
echo "MAP_CELLID_TO_POLYGON_COLLECTION_NAME=cell_to_polygons" >> .env


       