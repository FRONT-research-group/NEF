import time
import docker
from datetime import datetime, timedelta
from core_crowler.utils.logger import setup_logger

logger = setup_logger(logger_name="amf_log_docker_simulator")

class DockerLogFetcher:
    def __init__(self, container_name: str, poll_interval: int = 2):
        self.client = docker.from_env()
        self.container = self.client.containers.get(container_name)
        self.poll_interval = poll_interval
        self.buffer = []
        self.last_fetch_time = datetime.now()
        self.log_stream = self.container.logs(stream=True, follow=True, since=int(self.last_fetch_time.timestamp()))

    def clean_ansi_codes(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def parse_timestamp(self, line):
        try:
            match = re.match(r'(\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{3}):', line)
            if not match:
                return None
            ts_str = match.group(1)
            full_ts_str = f"2025/{ts_str}"
            return datetime.strptime(full_ts_str, "%Y/%m/%d %H:%M:%S.%f")
        except Exception:
            return None

    def start_streaming(self):
        for line in self.log_stream:
            line = self.clean_ansi_codes(line.decode("utf-8").strip())
            ts = self.parse_timestamp(line)
            if ts:
                self.buffer.append((ts, line))
            elif "ueLocation" in line and self.buffer:
                self.buffer[-1] = (self.buffer[-1][0], f"{self.buffer[-1][1]} {line}")

    def fetch_logs(self):
        now = datetime.now()
        logs_in_window = [line for (ts, line) in self.buffer if self.last_fetch_time <= ts < now]
        self.last_fetch_time = now
        return logs_in_window

    def run_polling_loop(self, handler_fn):
        logger.info(f"[SDK] Polling logs from AMF Docker container every {self.poll_interval}s...")
        import threading
        t = threading.Thread(target=self.start_streaming, daemon=True)
        t.start()

        while True:
            logs = self.fetch_logs()
            if logs:
                handler_fn(logs)
            time.sleep(self.poll_interval)
