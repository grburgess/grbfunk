import os
import threading
import time
import requests
import  astropy.utils.data as astro_data

import coloredlogs, logging
import grbfunk.utils.log

logger = logging.getLogger("grbfunk.download")





def download_file(url, path="/tmp"):
    """
    Download a file to the given path
    """

    fname = url.split("/")[-1]
    f = astro_data.download_file(url)

    return f

class BackgroundDownload(object):


    def __init__(self, url, bot=None, description=None, wait_time=60, max_time=60*60):

        self._wait_time = wait_time
        self._max_time = max_time
        
        self._url = url
        self._bot = bot
        self._description = description


        thread = threading.Thread(target=self._run, args=())
        thread.daemon = True
        thread.start()


    def _run(self):


        flag = True

        time_spent = 0 # seconds
        
        while flag:


            try:

                logging.info(f'Trying to download file from {self._url}')

                path = download_file(self._url)

                logging.info(f'Successfully downloaded {self._url}')

                if self._bot is not None:

                    self._bot.show(path, self._description)

                flag = False
                
                

            except:

                logging.warning(f'Could not download from {self._url}')

                if time_spent >= self._max_time:

                    logging.warning(f'I waited for a long time and {self._url} never appeared')
                    logging.warning(f'I give up!')

                    flag = False
                    
                else:
                
                    logging.warning(f'I will try again in {self._wait_time} secs')


                    time.sleep(self._wait_time)
                    time_spent += self._wait_time
                



# def download_file(url, path="/tmp"):
#     """
#     Download a file to the given path
#     """

#     fname = url.split("/")[-1]
#     path = os.path.join(path, fname)

#     r = requests.get(url, stream=True)

#     with open(path, "wb") as f:

#         for ch in r:

#             f.write(ch)
#     return path
