#!/bin/bash
NETWORK_NAME="shared"

if ! docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
  echo ">>> Creating Docker network: $NETWORK_NAME"
  docker network create $NETWORK_NAME
else
  echo ">>> Docker network $NETWORK_NAME already exists"
fi