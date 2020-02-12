import re
import os
import lxml.etree
import gcn
import collections
from grbfunk.utils.download_file import BackgroundDownload
from grbfunk.utils.process_counter import _global_proccess_counter
import coloredlogs, logging
import grbfunk.utils.log


logger = logging.getLogger("grbfunk.notification")


_DEBUG = False
if os.environ.get("GRBFUNK_DEBUG") is not None:

    if os.environ.get("GRBFUNK_DEBUG") == "True":

        _DEBUG = True


class Notification(object):
    def __init__(self, root, instrument_name, notify_type, bot=None):
        """
        
        Generic notification
        

        :param root: 
        :param instrument_name: 
        :param notify_type: 
        :param bot: the notifier's bot
        :returns: 
        :rtype: 

        """

        self._instrument_name = instrument_name
        self._notify_type = notify_type
        self._process_counter = _global_proccess_counter

        logger.debug(f"constructing {instrument_name} {notify_type} notification")

        self._bot = bot

        self._root = root

        self._downloads = collections.OrderedDict()
        self._message = ""

        self._build_message_header()
        self._build_message()

        # if not _DEBUG:
        #     self._bot.speak(self._message)

        self._bot.speak(self._message)

    def _add_line_to_msg(self, line):
        self._message += f"{line}\n"
        logger.debug(
            f"adding '{line}' to the total message of {self._instrument_name} {self._notify_type}"
        )

    def action(self):
        pass

    def _build_message_header(self):

        logger.debug(
            f"building message header for {self._instrument_name} {self._notify_type}"
        )

        self._add_line_to_msg(f"{self._instrument_name} Notification")
        self._add_line_to_msg(f"Alert: {self._notify_type}")

    def _build_message(self):

        logger.info(
            f"Start of _action_ for {self._instrument_name} {self._notify_type}"
        )
        self.action()

    def _download(
        self, url, description=None, path=None, use_bot=True, wait_time=60, max_time=60 * 60
    ):

        logger.debug(
            f"{self._instrument_name} {self._notify_type} is about to download '{url}' to '{path}'"
        )

        # create a downloader in the background
        if use_bot:

            downloader = BackgroundDownload(
                url,
                self._process_counter,
                bot=self._bot,
                description=description,
                wait_time=wait_time,
                max_time=max_time,
            )

        else:

            assert path is not None, "there is no path set!"

            downloader = BackgroundDownload(
                url,
                self._process_counter,
                store_path=path,
                wait_time=wait_time,
                max_time=max_time,
            )

    def print(self):

        print(self._message)

    def cleanup(self):

        logger.debug(
            f"{self._instrument_name} {self._notify_type} is starting to clean up"
        )
        for k, v in self._downloads.items():

            try:
                os.remove(v)

                logger.info(
                    f"{self._instrument_name} {self._notify_type} deleted '{v}'"
                )

            except:

                logger.warning(f"could not delete '{v}'")

    @property
    def message(self):

        return self._message

    @property
    def downloads(self):

        return self._downloads
