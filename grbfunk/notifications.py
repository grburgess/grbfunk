import re
import os
import lxml.etree
import gcn
import collections
import coloredlogs, logging


from grbfunk.utils.download_file import download_file
import grbfunk.utils.log

logger = logging.getLogger("grbfunk.notification")





_DEBUG = False
if os.environ.get('GRBFUNK_DEBUG') is not None:

    if os.environ.get('GRBFUNK_DEBUG') == 'True':

        _DEBUG = True


class Notification(object):
    def __init__(self, root, instrument_name, notify_type):
        """
        
        Generic notification
        

        :param root: 
        :param instrument_name: 
        :param notify_type: 
        :returns: 
        :rtype: 

        """

        self._instrument_name = instrument_name
        self._notify_type = notify_type

        logger.debug(f'constructing {instrument_name} {notify_type} notification')
        
        # if _DEBUG:
        
        #     self._root = lxml.etree.parse(open(root, "r"))

#        else:

        self._root = root

        self._downloads = collections.OrderedDict()
        self._message = ""

        
        self._build_message_header()
        self._build_message()

    def _add_line_to_msg(self, line):
        self._message += f"{line}\n"
        logger.debug(f"adding '{line}' to the total message of {self._instrument_name} {self._notify_type}")

        
    def action(self):
        pass

    def _build_message_header(self):

        logger.debug(f'building message header for {self._instrument_name} {self._notify_type}')
        
        self._add_line_to_msg(f"{self._instrument_name} Notification")
        self._add_line_to_msg(f"Alert: {self._notify_type}")

    def _build_message(self):

        logger.info(f"Start of _action_ for {self._instrument_name} {self._notify_type}")
        self.action()

    def _download(self, url, path, description):

        logger.debug(f"{self._instrument_name} {self._notify_type} is about to download '{url}' to '{path}'" )
        
        try:
            tmp = download_file(url, path)

            logger.info(f"Succesfully downloaded '{url}' to '{path}'")
            
            self._downloads[description] = tmp

            return tmp

        except:

            logger.warning(f"{self._instrument_name} {self._notify_type} could not download {url}")

            return None


        
    def print(self):

        print(self._message)

    def cleanup(self):

        logger.debug(f'{self._instrument_name} {self._notify_type} is starting to clean up')
        for k,v in self._downloads.items():

            try:
                os.remove(v)

                logger.info(f"{self._instrument_name} {self._notify_type} deleted '{v}'")

            except:

                logger.warning(f"could not delete '{v}'")
                
    @property
    def message(self):

        return self._message

    @property
    def downloads(self):

        return self._downloads


