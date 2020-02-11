import os
import threading
import time
import requests
import astropy.utils.data as astro_data

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
    def __init__(self, url, process_counter ,bot=None, description=None, wait_time=60, max_time=60 * 60):
        """
        An worker to download objects in the background to avoid blocking the GCN
        listen function.

        If a bot is specfied, it will upload an the image with the bot.


        :param url: The URL to download the file
        :param bot: the optional bot
        :param description: the description for the bot's plot
        :param wait_time: the wait time interval for checking files
        :param max_time: the max time to wait for files
        :returns: 
        :rtype: 

        """

        self._wait_time = wait_time
        self._max_time = max_time

        self._url = url
        self._bot = bot
        self._description = description

        self._process_counter = process_counter

        # create a background thread that will go and download the files

        self._process_counter.add_proccess()
        thread = threading.Thread(target=self._run, args=())
        thread.daemon = True
        thread.start()

    def _run(self):

        # set a flag to kill the job
        
        flag = True

        # the time spent waiting so far
        time_spent = 0  # seconds

        while flag:

            # try to download the file
            
            try:

                logging.info(f"Trying to download file from {self._url}")

                path = download_file(self._url)

                logging.info(f"Successfully downloaded {self._url}")

                # if we succeeded and there is a bot
                # then let's upload it to telegram
                
                if self._bot is not None:

                    self._bot.show(path, self._description)

                # kill the loop
                    
                flag = False

            except:

                # ok, we have not found a file yet
                
                logging.warning(f"Could not download from {self._url}")

                # see if we should still wait for the file
                
                if time_spent >= self._max_time:

                    logging.warning(
                        f"I waited for a long time and {self._url} never appeared"
                    )
                    logging.warning(f"I give up!")

                    # we are out of time so give up
                    
                    flag = False

                else:

                    # ok, let's sleep for a bit and then check again
                    
                    logging.warning(f"I will try again in {self._wait_time} secs")

                    time.sleep(self._wait_time)

                    # up date the time we have left

                    logging.debug(f"we have {self._max_time - time_spent} seconds left before I give up")
                    
                    time_spent += self._wait_time
        self._process_counter.kill_process()

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
