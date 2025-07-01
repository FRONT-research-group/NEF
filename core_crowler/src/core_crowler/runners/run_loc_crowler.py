import os
from core_crowler.utils.logger import setup_logger
from core_crowler.cores.O5GS.location.log_fetching import DockerLogFetcher
from core_crowler.cores.O5GS.location.log_parser import LogParser  

# Need changes
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASS", "secret")
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "amf_logs")

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

# Logger setup
logger = setup_logger(logger_name="amf_log_parser")

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
    simulator = DockerLogFetcher(
        container_name="amf",
        poll_interval=2
    )
    try:
        simulator.run(handle_logs)
    except KeyboardInterrupt:
        logger.info("\n[INTERRUPT] Displaying final event history...")
