import docker
import time
from datetime import datetime

from core_crowler.utils.log_fetcher_helper import load_logs
from core_crowler.utils.logger import setup_logger
import subprocess

logger = setup_logger(logger_name="amf_log_watcher")

class DockerLogFetcher:
    def __init__(self, container_name: str, poll_interval: int = 2):
        self.container_name = container_name
        self.poll_interval = poll_interval
        self.last_fetch_time = datetime.now()
        self.use_sdk = True

        if docker:
            try:
                self.client = docker.from_env()
                self.container = self.client.containers.get(container_name)
                self.use_sdk = True
                logger.info("[INFO] Docker SDK initialized.")
            except Exception as e:
                logger.warning(f"[WARN] Docker SDK failed: {e}. Falling back to CLI.")
        else:
            logger.warning("[WARN] Docker SDK not available. Falling back to CLI.")

    def fetch_logs_sdk(self):
        logs = self.container.logs(since=int(self.last_fetch_time.timestamp()), stdout=True, stderr=True)
        lines = logs.decode("utf-8").splitlines()
        return lines

    def fetch_logs_cli(self):
        cmd = [
            "docker", "logs", self.container_name,
            "--since", self.last_fetch_time.isoformat()
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.splitlines()

    def fetch_logs(self):
        now = datetime.now()
        try:
            lines = self.fetch_logs_sdk() if self.use_sdk else self.fetch_logs_cli()
        except Exception as e:
            logger.error(f"[ERROR] Failed to fetch logs: {e}")
            return []

        logs = load_logs(lines)

        self.last_fetch_time = now
        return [l for _, l in logs]

    def run(self, handler_fn):
        logger.info(f"[INFO] Watching container '{self.container_name}' logs every {self.poll_interval}s...")
        while True:
            logs = self.fetch_logs()
            if logs:
                handler_fn(logs)
            time.sleep(self.poll_interval)

