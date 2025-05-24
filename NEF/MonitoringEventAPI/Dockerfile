FROM python:3.12.10-slim

WORKDIR /

COPY requirements.txt ./app/

#COPY outbound-cert-2024.crt /usr/local/share/ca-certificates

#TODO change root as user, security hardening
RUN update-ca-certificates && rm -rf /var/lib/apt/lists/* && \
    groupadd -r appuser && useradd -r -g appuser appuser && \
    pip install --upgrade pip && \ 
    pip install --no-cache-dir -r ./app/requirements.txt

COPY ./app /app

ENV HOST="127.0.0.1"
ENV PORT="8080"
ENV LOG_DIRECTORY_PATH="./app/log1/"
ENV LOG_FILENAME_PATH="${LOG_DIRECTORY_PATH}logger"

EXPOSE 8000
ENTRYPOINT ["uvicorn", "app.main:app"]
CMD ["--host", "${HOST}", "--port", "${PORT}"]
