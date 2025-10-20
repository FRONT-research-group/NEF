import time
from datetime import datetime, timedelta

from core_crowler.utils.log_fetcher_helper import load_logs
from core_crowler.utils.logger import setup_logger

logger = setup_logger(logger_name = "amf_log_simulator")

class FileLogSimulator:
    def __init__(self, filepath: str, poll_interval: int = 5):
        self.filepath = filepath
        self.poll_interval = poll_interval
        self.logs = self.init_logs_from_log_file()  # (timestamp, line) tuples
        self.last_fetch_time = self.logs[0][0] if self.logs else datetime.now()

    def init_logs_from_log_file(self):
        with open(self.filepath, 'r',encoding='UTF-8') as f:
            logs = load_logs(f.readlines())       
        return logs

    def fetch_logs(self):
        now = self.last_fetch_time + timedelta(seconds=self.poll_interval)
        logs_in_window = [line for (ts, line) in self.logs if self.last_fetch_time <= ts < now]
        self.last_fetch_time = now
        return logs_in_window

    def run_polling_loop(self, handler_fn):
        logger.info("[SIM] Polling logs from file every %ds...", self.poll_interval)

        while True:

            if not self.logs:
                logger.warning("[SIM] No valid logs found yet — waiting for new entries...")
                time.sleep(self.poll_interval)
                continue  # Try again next cycle

            try:
                # Process new logs since last fetch
                while self.last_fetch_time < self.logs[-1][0]:
                    logs = self.fetch_logs()
                    if logs:
                        handler_fn(logs)
                    time.sleep(self.poll_interval)

            except IndexError:
                # In case logs become empty between iterations
                logger.warning("[SIM] No logs available — retrying...")
                time.sleep(self.poll_interval)
                continue
            except Exception as e:
                logger.exception("[SIM] Unexpected error in polling loop: %s", e)
                time.sleep(self.poll_interval)


