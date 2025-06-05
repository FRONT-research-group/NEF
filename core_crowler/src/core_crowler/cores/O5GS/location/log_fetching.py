import os
import time
import re
from datetime import datetime, timedelta

try:
    import docker
except ImportError:
    docker = None

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

    def clean_ansi_codes(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def parse_timestamp(self, line):
        match = re.match(r'(\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{3}):', line)
        if not match:
            return None
        ts_str = match.group(1)
        full_ts_str = f"{datetime.now().year}/{ts_str}"
        try:
            return datetime.strptime(full_ts_str, "%Y/%m/%d %H:%M:%S.%f")
        except:
            return None

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

        logs = []
        for line in lines:
            line = self.clean_ansi_codes(line.strip())
            ts = self.parse_timestamp(line)
            if ts:
                logs.append((ts, line))
            elif "ueLocation" in line and logs:
                logs[-1] = (logs[-1][0], logs[-1][1] + " " + line)

        self.last_fetch_time = now
        return [l for _, l in logs]

    def run(self, handler_fn):
        logger.info(f"[INFO] Watching container '{self.container_name}' logs every {self.poll_interval}s...")
        while True:
            logs = self.fetch_logs()
            if logs:
                handler_fn(logs)
            time.sleep(self.poll_interval)

# -----------------------------
def handle_logs(logs):
    for log in logs:
        logger.info(f"[LOG] {log}")

if __name__ == "__main__":
    container_name = os.getenv("TARGET_CONTAINER_NAME", "amf")
    fetcher = DockerLogFetcher(container_name=container_name, poll_interval=2)
    fetcher.run(handle_logs)
