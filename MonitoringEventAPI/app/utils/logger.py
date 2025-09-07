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


def get_app_logger():
    '''
        Docstring
    '''

    check_log_path_exists()

    app_logger = logging.getLogger('local_allocation_manager')

    if not app_logger.handlers:
        logger = logging.getLogger('local_allocation_manager')
        logger.setLevel(logging.DEBUG)

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

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        return logger

    return app_logger