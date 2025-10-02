FROM python:3.12.10-bullseye

WORKDIR /

COPY requirements.txt ./app/
COPY ./certs/capif_cert_server.pem ./app/certs/capif_cert_server.pem

#TODO change root as user, security hardening
RUN rm -rf /var/lib/apt/lists/* && \
    groupadd -r appuser && useradd -r -g appuser appuser && \
    pip install --upgrade pip && \ 
    pip install --no-cache-dir -r ./app/requirements.txt

COPY ./app /app

ENV HOST="127.0.0.1"
ENV PORT="8080"
ENV LOG_DIRECTORY_PATH="./app/log1/"
ENV LOG_FILENAME_PATH="${LOG_DIRECTORY_PATH}logger"



EXPOSE 8000


# # Using `sh -c` allows us to expand environment variables (HOST and PORT) at runtime,
# # which Docker's default CMD/ENTRYPOINT parsing does not support.
# # Without `sh -c`, Docker passes "${PORT}" literally to uvicorn, resulting in an invalid value.
# # We set default values for HOST and PORT here, which can be overridden by docker-compose
# # or runtime environment variables.
ENTRYPOINT ["sh", "-c", "uvicorn app.main:app --host ${HOST} --port ${PORT}"]
