#!/bin/sh

#run using sudo
# set -e
# apt-get install sshpass -y

# --- Configuration ---
REMOTE_NODE="10.220.2.43"
SFTP_PORT="2222"
SFTP_USER="foo"
SFTP_PASS="pass"

REMOTE_DIR="upload"

# --- Argument check ---
if [ $# -ne 2 ]; then
    echo "Usage: $0 [provider] [download]"
    exit 1
fi

ROLE=$1
ACTION="$2"
FILE=""

if [ "$ROLE" = "provider" ]; then
  FILE="capif_cert_server.pem"
else
  echo "Invalid argument: $ROLE (must be 'provider')"
  exit 1
fi

if [ "$ACTION" = "download" ]; then
    echo \"Downloading $FILE from remote node...\"
    SFTP_CMD="get $REMOTE_DIR/$ROLE/$FILE ./MonitoringEventAPI/certs/"
else
    echo "Invalid action: $ACTION (must be download)"
    exit 1
fi

sshpass -p "$SFTP_PASS" sftp -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null \
    -oPort=$SFTP_PORT $SFTP_USER@$REMOTE_NODE <<EOF
$SFTP_CMD
EOF

echo "SFTP command completed successfully."
