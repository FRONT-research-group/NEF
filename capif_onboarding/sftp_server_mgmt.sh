#!/bin/sh

# run using sudo
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
    echo "Usage: $0 [provider|invoker] [upload|download]"
    exit 1
fi

ROLE=$1
ACTION="$2"
FILE=""

echo "DEBUG: role='$ROLE' action='$ACTION'"

if [ "$ROLE" = "provider" ]; then
  #LOCAL_DIR="./provider_impl/provider_folder/ppavlidis"
  LOCAL_DIR="./provider_folder/ppavlidis"
  FILE="capif_cert_server.pem"
elif [ "$ROLE" = "invoker" ]; then
  LOCAL_DIR="./invoker_folder/ppavlidis"
  FILE="jwt_token.txt"
else
  echo "Invalid argument: $ROLE (must be 'invoker' or 'provider')"
  exit 1
fi

LOCAL_PATH="$LOCAL_DIR/$FILE"

if [ "$ACTION" = "upload" ]; then
    if [ ! -f "$LOCAL_PATH" ]; then
        echo "File not found: $LOCAL_PATH"
        exit 1
    fi
    echo \"Uploading $FILE on remote node...\"
    SFTP_CMD="put $LOCAL_PATH $REMOTE_DIR/$ROLE/$FILE"  
elif [ "$ACTION" = "download" ]; then
    echo \"Downloading $FILE from remote node...\"
    SFTP_CMD="get $REMOTE_DIR/$ROLE/$FILE ./certs/"
else
    echo "Invalid action: $ACTION (must be upload or download)"
    exit 1
fi

sshpass -p "$SFTP_PASS" sftp -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null \
    -oPort=$SFTP_PORT $SFTP_USER@$REMOTE_NODE <<EOF
$SFTP_CMD
EOF

echo "SFTP command completed successfully."
