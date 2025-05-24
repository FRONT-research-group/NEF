import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer


import os
import logging
from logging.handlers import RotatingFileHandler


def check_log_path_exists(directory_path):
    '''
        Docstring
    '''
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_app_logger(directory_path):
    '''
        Docstring
    '''

    check_log_path_exists(directory_path)

    app_logger = logging.getLogger('local_allocation_manager')

    if not app_logger.handlers:
        logger = logging.getLogger('local_allocation_manager')
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S')

        #10 MB max per file, 5 files max
        file_handler = RotatingFileHandler("test_server" + ".log",
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

log = get_app_logger("/server_logs")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        content_length = int(self.headers.get('Content-Length', 0)) 
        post_data = self.rfile.read(content_length)  
        post_data_str = post_data.decode('utf-8')  

        try:
            json_data = json.loads(post_data_str)  
        except json.JSONDecodeError:
            json_data = {"error": "Invalid JSON"}

        
        log.info(f"[{datetime.now()}] Received POST request:")
        log.info(json.dumps(json_data, indent=4))



        self.send_response(204)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response_data = {
            "message": "Request received",
            "status": "success"
        }

        log.info(f"[{datetime.now()}]before send the response")
        self.wfile.write(json.dumps(response_data).encode())

        log.info(f"[{datetime.now()}]response has been sent")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, server_address=None):
    if server_address is None:
        server_address = ('', 8001)
    httpd = server_class(server_address, handler_class)
    log.info(f'Starting server at http://{httpd.server_name}:{httpd.server_port}')
    httpd.allow_reuse_address = True
    httpd.serve_forever()

if __name__ == '__main__':
    run()
