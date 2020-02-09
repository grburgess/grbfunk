import re
import os
import lxml.etree
import gcn

import collections

from grbfunk.utils.download_file import download_file


_DEBUG = False
if os.environ.get('GRBFUNK_DEBUG') is not None:

    if os.environ.get('GRBFUNK_DEBUG') == 'True':

        _DEBUG = True


class Notification(object):
    def __init__(self, root, instrument_name, notify_type):
        """
        
        

        :param root: 
        :param instrument_name: 
        :param notify_type: 
        :returns: 
        :rtype: 

        """

        self._instrument_name = instrument_name
        self._notify_type = notify_type
        
        if _DEBUG:
        
            self._root = lxml.etree.parse(open(root, "r"))

        else:
            
            self._root = root

        self._downloads = collections.OrderedDict()
        self._message = ""

        self._build_message_header()
        self._build_message()

    def _add_line_to_msg(self, line):
        self._message += f"{line}\n"

    def action(self):
        pass

    def _build_message_header(self):

        self._add_line_to_msg(f"{self._instrument_name} Notification")
        self._add_line_to_msg(f"Alert: {self._notify_type}")

    def _build_message(self):

        self.action()

    def _download(self, url, path, description):

        tmp = download_file(url, path)

        self._downloads[description] = tmp

        return tmp

    def print(self):

        print(self._message)

    def cleanup(self):

        for k,v in self._downloads.items():
            os.remove(v)

    @property
    def message(self):

        return self._message

    @property
    def downloads(self):

        return self._downloads


