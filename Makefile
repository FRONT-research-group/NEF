# Makefile for deploying and undeploying docker compose stack

# Load variables from .env if it exists
ifneq (,$(wildcard .env))
  include .env
  export
endif

SCRIPT := ./sftp_server_mgmt.sh
DOCKER_COMPOSE := docker compose
CONF_EXT_NETWORK := ./conf_external_network.sh
REMOVE_EXT_NETWORK := ./remove_external_network.sh

.PHONY: all deploy deploy-auth deploy-provider-onboard deploy-no-auth undeploy-auth undeploy-no-auth undeploy-provider-onboard offboard-capif-provider manage-certs conf-ext-network remove-ext-network clean clean-auth clean-no-auth

all: deploy

conf-ext-network:
	@echo ">>> Running script for configuring external network..."
	$(CONF_EXT_NETWORK)
	@echo ">>> Script finished."

remove-ext-network:
	@echo "Running script for removing external network..."
	$(REMOVE_EXT_NETWORK)
	@echo "Script finished."

manage-certs:
	@echo "Running script for download capif certificate..."
	$(SCRIPT) provider download
	@echo "Script finished."

offboard-capif-provider:
	@echo "Offboarding CAPIF provider..."
	cd capif_onboarding && \
	docker cp provider_onboard:/app/provider_folder/$(CAPIF_USER)/ ./provider_folder/$(CAPIF_USER)/ && \
	python ./provider_offboard.py
	@echo "CAPIF provider offboarding complete."

deploy-provider-onboard:
	@echo "Deploying provider onboarding service..."
	$(DOCKER_COMPOSE) -f docker-compose.provider-onboard.yaml up --build -d
	@echo "Provider onboarding deployment complete."

undeploy-provider-onboard: offboard-capif-provider
	@echo "Undeploying provider onboarding service..."
	$(DOCKER_COMPOSE) -f docker-compose.provider-onboard.yaml down
	@echo "Provider onboarding undeployment complete."

undeploy-auth:
	@echo "Stopping and removing Docker Compose services..."
	$(DOCKER_COMPOSE) -f docker-compose.yaml -f docker-compose.auth.yaml down
	@echo "Undeployment complete."

undeploy-no-auth:
	@echo "Stopping and removing Docker Compose services..."
	$(DOCKER_COMPOSE) -f docker-compose.yaml down
	@echo "Undeployment complete."

deploy-auth: deploy-provider-onboard conf-ext-network manage-certs
	@echo "Auth enabled: running full deployment..."
	$(DOCKER_COMPOSE) -f docker-compose.yaml -f docker-compose.auth.yaml up --build -d
	@echo "Deployment complete (auth enabled)."

deploy-no-auth:
	@echo "Auth disabled: running minimal deployment..."
	$(DOCKER_COMPOSE) -f docker-compose.yaml up --build -d
	@echo "Deployment complete (no auth)."
#undeploy-provider-onboard
clean-auth: undeploy-provider-onboard undeploy-auth remove-ext-network
	@echo "Auth enabled: full cleanup with external network removal complete."

clean-no-auth: undeploy-no-auth
	@echo "Auth disabled: basic cleanup complete."

deploy:
ifeq ($(AUTH_ENABLED),True)
	$(MAKE) deploy-auth
else
	$(MAKE) deploy-no-auth
endif

clean:
ifeq ($(AUTH_ENABLED),True)
	$(MAKE) clean-auth
else
	$(MAKE) clean-no-auth
endif
