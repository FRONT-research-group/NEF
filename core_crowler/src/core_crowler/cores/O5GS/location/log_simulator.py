import time
import re
from datetime import datetime, timedelta

from core_crowler.utils.logger import setup_logger

logger = setup_logger(logger_name = "amf_log_simulator")

class FileLogSimulator:
    def __init__(self, filepath: str, poll_interval: int = 5):
        self.filepath = filepath
        self.poll_interval = poll_interval
        self.logs = self.load_logs()  # (timestamp, line) tuples
        self.last_fetch_time = self.logs[0][0] if self.logs else datetime.now()

    def clean_ansi_codes(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def parse_timestamp(self, line):
        """
        Parse timestamp from the log line: '04/08 13:06:42.933: ...'
        Returns a datetime object.
        """
        try:
            match = re.match(r'(\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{3}):', line)
            if not match:
                return None
            ts_str = match.group(1)
            full_ts_str = f"2025/{ts_str}"  # hardcoded year for this simulation
            return datetime.strptime(full_ts_str, "%Y/%m/%d %H:%M:%S.%f")
        except Exception:
            return None

    def load_logs(self):
        logs = []
        with open(self.filepath, 'r') as f:
            for line in f:
                line = self.clean_ansi_codes(line.strip())
                if not line or line == '-':
                    continue
                ts = self.parse_timestamp(line)
                if ts:
                    logs.append((ts, line))
                else:
                    if "ueLocation" in line:
                        # This is the json. Append it to the last log
                        logs[-1] = (logs[-1][0], f"{logs[-1][1]} {line}")
                        
        return logs

    def fetch_logs(self):
        now = self.last_fetch_time + timedelta(seconds=self.poll_interval)
        logs_in_window = [line for (ts, line) in self.logs if self.last_fetch_time <= ts < now]
        self.last_fetch_time = now
        return logs_in_window

    def run_polling_loop(self, handler_fn):
        logger.info(f"[SIM] Polling logs from file every {self.poll_interval}s...")
        while self.last_fetch_time < self.logs[-1][0]:
            logs = self.fetch_logs()
            if logs:
                handler_fn(logs)
            time.sleep(self.poll_interval)

# -------------------------------------------------------- #
def handle_logs(logs):
    for log in logs:
        logger.info(f"[LOG] {log}")

if __name__ == "__main__":
    simulator = FileLogSimulator(
        filepath="/Users/georgebatsis/Documents/FRONT/amf_log_parser/storage/threeUEs_amf_logs.txt",
        poll_interval=2
    )
    
    simulator.run_polling_loop(handle_logs)
