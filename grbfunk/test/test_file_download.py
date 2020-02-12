import http.server
import socketserver
import threading
import time
import os
from grbfunk.utils.download_file import BackgroundDownload
from grbfunk.utils.process_counter import _global_proccess_counter
from grbfunk.bot import Bot
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

_DEBUG = False
_TESTING = False
if os.environ.get("GRBFUNK_DEBUG") is not None:

    if os.environ.get("GRBFUNK_DEBUG") == "True":

        _DEBUG = True

    # for travisCI
    _TRAVIS_TOKEN = os.environ.get("TOKEN")
    
    if _TRAVIS_TOKEN is not None:

        _TESTING = True



def test_background_download():

    url = "http://0.0.0.0:8080/clowns.txt"

    token = _TRAVIS_TOKEN
    
    bot = Bot('test',token = token, chat_id = None )
    
    dl = BackgroundDownload(url, _global_proccess_counter, bot=bot, wait_time=1, max_time=60)

    time.sleep(5)

    os.system("touch clowns.txt")

    time.sleep(10)

    os.remove("clowns.txt")


def test_background_download_timeout():

    url = "http://0.0.0.0:8080/clowns.txt"

    token = _TRAVIS_TOKEN
    
    bot = Bot('test',token = token, chat_id = None )

    
    dl = BackgroundDownload(url, _global_proccess_counter, bot=bot, wait_time=1, max_time=9)

    time.sleep(10)
