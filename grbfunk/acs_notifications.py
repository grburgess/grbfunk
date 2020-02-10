import os
import re
import numpy as np
import coloredlogs, logging
from grbfunk.notifications import Notification
import grbfunk.utils.log

logger = logging.getLogger("grbfunk.notification.ACS")


class ACSNotification(Notification):
    def __init__(self, root, notify_type):
        """
        Generic ACS  alert providing basic 
        functionality

        :param root: the parsed xml file
        :param notify_type: the type of notification (str)
        :returns: 
        :rtype: 

        """

        super(ACSNotification, self).__init__(
            instrument_name="ACS", root=root, notify_type=notify_type
        )

        logger.debug("ACS notification is being created")
