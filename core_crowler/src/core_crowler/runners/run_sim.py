import os
from core_crowler.utils.logger import setup_logger
from core_crowler.cores.O5GS.location.log_simulator import FileLogSimulator
from core_crowler.cores.O5GS.location.log_parser import LogParser  

MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASS", "secret")
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "amf_logs")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "/data/threeUEs_amf_logs.txt")

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

# Logger setup
logger = setup_logger(logger_name="amf_log_simulator")

# Parser and simulator setup
parser = LogParser(
    mongo_uri=MONGO_URI,
    db_name=MONGO_DB_NAME,
    collection_name="ue_events"
)

def handle_logs(logs):
    for log in logs:
        parser.process_line(log)

if __name__ == "__main__":
    simulator = FileLogSimulator(
        filepath=LOG_FILE_PATH,
        poll_interval=2
    )
    try:
        simulator.run_polling_loop(handle_logs)
    except KeyboardInterrupt:
        logger.info("\n[INTERRUPT] Displaying final event history...")
