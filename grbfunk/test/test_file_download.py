import http.server
import socketserver
import threading
import time
import os
from grbfunk.utils.download_file import BackgroundDownload
from grbfunk.utils.process_counter import _global_proccess_counter
import coloredlogs, logging
import grbfunk.utils.log

# logger = logging.getLogger("grbfunk.download")


PORT = 8080


def server():
    Handler = http.server.SimpleHTTPRequestHandler

    httpd = socketserver.TCPServer(("", PORT), Handler)

    print("serving at port", PORT)
    httpd.serve_forever()


thread = threading.Thread(target=server)
thread.daemon = True
thread.start()


def test_background_download():

    url = "http://0.0.0.0:8080/clowns.txt"

    dl = BackgroundDownload(url, _global_proccess_counter, wait_time=1, max_time=60)

    time.sleep(5)

    os.system("touch clowns.txt")

    time.sleep(10)

    os.remove("clowns.txt")


def test_background_download_timeout():

    url = "http://0.0.0.0:8080/clowns.txt"

    dl = BackgroundDownload(url, _global_proccess_counter, wait_time=1, max_time=9)

    time.sleep(10)
