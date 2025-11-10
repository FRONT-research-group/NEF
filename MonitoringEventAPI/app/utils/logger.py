import os
import logging
from logging.handlers import RotatingFileHandler

from app.config import get_settings


settings = get_settings()

def check_log_path_exists():
    '''
        Docstring
    '''
    if not os.path.exists(settings.log_directory_path):
        os.makedirs(settings.log_directory_path)


def get_app_logger(logger_name : str):
    '''
        Docstring
    '''

    check_log_path_exists()

    app_logger = logging.getLogger(logger_name)

    if not app_logger.handlers:
        #logger = logging.getLogger(logger_name)
        app_logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S')

        #10 MB max per file, 5 files max
        file_handler = RotatingFileHandler(settings.log_filename_path + ".log",
                                           maxBytes=10*1024*1024,
                                           backupCount=5)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        app_logger.addHandler(file_handler)
        app_logger.addHandler(stream_handler)
        app_logger.propagate = False
        
        # Disable pymongo logs
        logging.getLogger("pymongo").setLevel(logging.CRITICAL)
        # Or completely disable it
        logging.getLogger("pymongo").propagate = False
        logging.getLogger("pymongo").handlers.clear()

        return app_logger

    return app_logger