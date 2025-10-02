# Makefile for deploying and undeploying docker compose stack

SCRIPT := ./sftp_server_mgmt.sh
DOCKER_COMPOSE := docker compose
CONF_EXT_NETWORK := ./conf_external_network.sh
REMOVE_EXT_NETWORK := ./remove_external_network.sh

.PHONY: all deploy undeploy manage-certs conf-ext-network remove-ext-network

all: deploy

conf-ext-network:
	echo ">>> Running script for configuring external network..."
	$(CONF_EXT_NETWORK)
	echo ">>> Script finished."

remove-ext-network:
	echo ">>> Running script for removing external network..."
	$(REMOVE_EXT_NETWORK)
	echo ">>> Script finished."

manage-certs:
	echo ">>> Running script for download capif certificate..."
	$(SCRIPT) provider download
	echo ">>> Script finished."

deploy: conf-ext-network manage-certs
	echo ">>> Starting Docker Compose services..."
	$(DOCKER_COMPOSE) up --build -d
	echo ">>> Deployment complete."

undeploy:
	echo ">>> Stopping and removing Docker Compose services..."
	$(DOCKER_COMPOSE) down
	echo ">>> Undeployment complete."

clean: undeploy remove-ext-network
	echo ">>> Clean complete."