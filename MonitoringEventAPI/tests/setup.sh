#!/bin/bash

# --- Configuration ---
NEF_CONTAINER_NAME="nef"
TEST_SERVER_CONTAINER_NAME="test_server"

NEF_EXPOSED_PORT="8000"            
TEST_SERVER_EXPOSED_PORT="8001"

ENV_FILE="./tests/.env"
# --- End Configuration ---


# Erase the .env file if it exists
if [ -f "$ENV_FILE" ]; then
  echo "Erasing existing $ENV_FILE"
  rm "$ENV_FILE"
fi

# Get the IP address of the docker0 interface
docker0_ip=$(ip addr show docker0 | grep "inet " | awk '{print $2}' | cut -d'/' -f1)

# Get the host port mapping for the specified container and exposed port
nef_host_port=$(docker port "$NEF_CONTAINER_NAME" "$NEF_EXPOSED_CONTAINER_PORT" | cut -d':' -f2)
test_server_host_port=$(docker port "$TEST_SERVER_CONTAINER_NAME" "$TEST_SERVER_EXPOSED_CONTAINER_PORT" | cut -d':' -f2)

# Check if the IP address was found
if [ -n "$docker0_ip" ]; then
  echo "DOCKER0_IP=$docker0_ip" >> "$ENV_FILE"
  echo "Successfully wrote DOCKER0_IP=$docker0_ip to $ENV_FILE"
else
  echo "Could not find the IP address of the docker0 interface."
fi

echo "" >> "$ENV_FILE" # Add a newline for better readability

# Check if the host port mapping was found
if [ -n "$nef_host_port" ]; then
  echo "NEF_HOST_PORT=$nef_host_port" >> "$ENV_FILE"
  echo "Successfully wrote NEF_HOST_PORT=$nef_host_port to $ENV_FILE"
else
  echo "Could not find the host port mapping for container '$NEF_CONTAINER_NAME' and port '$NEF_EXPOSED_CONTAINER_PORT'."
fi

echo "" >> "$ENV_FILE" # Add a newline for better readability

if [ -n "$test_server_host_port" ]; then
  echo "TEST_SERVER_HOST_PORT=$test_server_host_port" >> "$ENV_FILE"
  echo "Successfully wrote TEST_SERVER_HOST_PORT=$test_server_host_port to $ENV_FILE"
else
  echo "Could not find the host port mapping for container '$TEST_SERVER_CONTAINER_NAME' and port '$TEST_SERVER_EXPOSED_CONTAINER_PORT'."
fi

echo "" >> "$ENV_FILE" # Add a newline for better readability

# Construct the API URL
nef_base_url="http://${docker0_ip}:${host_port}/3gpp-monitoring-event/v1/"

if [ -n "$nef_base_url" ]; then
  echo "NEF_BASE_URL=$nef_base_url" >> "$ENV_FILE"
  echo "Successfully wrote NEF_BASE_URL=\"$nef_base_url\" to $ENV_FILE"
else
  echo "Could not construct the API URL."
fi

echo "" >> "$ENV_FILE" # Add a newline for better readability

test_server_url="http://localhost:${test_server_host_port}/"

if [ -n "$test_server_url" ]; then
  echo "TEST_SERVER_URL=$test_server_url" >> "$ENV_FILE"
  echo "Successfully wrote TEST_SERVER_URL=\"$test_server_url\" to $ENV_FILE"
else
  echo "Could not construct the Test Server URL."
fi

echo "" >> "$ENV_FILE" # Add a newline for better readability