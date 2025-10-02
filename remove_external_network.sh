#!/bin/bash
NETWORK_NAME="shared"

if ! docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
  echo ">>> Docker network $NETWORK_NAME already deleted"
else
  echo ">>> Removing Docker network: $NETWORK_NAME"
  docker network rm $NETWORK_NAME
fi