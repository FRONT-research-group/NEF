#!/bin/sh
set -e
python /app/provider_capif_connector.py
exec /app/sftp_server_mgmt.sh "$@"