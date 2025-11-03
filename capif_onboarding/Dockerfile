FROM python:3.12.10-bullseye

WORKDIR /

COPY ../requirements.txt ./app/

#TODO change root as user, security hardening
RUN apt-get update && apt-get install sshpass -y  && rm -rf /var/lib/apt/lists/* && \
    groupadd -r appuser && useradd -r -g appuser appuser && \
    pip install --upgrade pip && \ 
    pip install --no-cache-dir -r ./app/requirements.txt

COPY ./capif_onboarding/openapi.yaml /app 
COPY ./capif_onboarding/provider_config_sample.json /app
COPY ./capif_onboarding/provider_capif_connector.py /app
COPY ./capif_onboarding/sftp_server_mgmt.sh /app
COPY ./capif_onboarding/entrypoint.sh /app
RUN chmod +x /app/sftp_server_mgmt.sh /app/entrypoint.sh

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["provider", "upload"]

#CMD ["sh", "-c", "python ./provider_capif_connector.py && ./sftp_server_mgmt.sh provider upload"]
