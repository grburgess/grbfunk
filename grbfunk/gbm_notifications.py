import os
import re
import numpy as np
from datetime import datetime, timedelta
import coloredlogs, logging
from grbfunk.notifications import Notification
from grbfunk.bot import GBMBot
import grbfunk.utils.log

logger = logging.getLogger("grbfunk.notification.GBM")


class GBMNotification(Notification):
    _current_grbs = {}

    def __init__(self, root, notify_type):
        """
        Generic GBM alert providing basic 
        functionality

        :param root: the parsed xml file
        :param notify_type: the type of notification (str)
        :returns: 
        :rtype: 

        """

        bot = GBMBot()

        # this 
        self._first_time = False
        
        super(GBMNotification, self).__init__(
            instrument_name="GBM", root=root, notify_type=notify_type, bot=bot
        )

        logger.debug("GBM notification is being created")

    def action(self):

        # parse the name of the GRB
        self._form_burst_name()

        logger.info(f"Start to process {self._burst_name}")

        # add it to the list
        self._add_line_to_msg(f"Name: {self._burst_name}")

    def _form_burst_name(self):
        """
        forms the burst name form the GCN
        """
        tmp = self._root.find(".//{*}ISOTime").text
        yy, mm, dd = re.match(
            r"^\d{2}(\d{2})-(\d{2})-(\d{2})T\d{2}:\d{2}:\d{2}\.\d{2}$", tmp
        ).groups()

        trigger_day_start = f"20{yy}-{mm}-{dd}"

        time_frac = (
            datetime.strptime(tmp, "%Y-%m-%dT%H:%M:%S.%f")
            - datetime.strptime(trigger_day_start, "%Y-%m-%d")
        ).total_seconds() / timedelta(1).total_seconds()

        frac = int(np.floor(time_frac * 1000))

        self._burst_name = f"GRB{yy}{mm}{dd}{frac}"
        
        if self._burst_name not in  GBMNotification._current_grbs:

            # This should start the pipe line
            GBMNotification._current_grbs[self._burst_name] = True

        


class GBMLocationNotification(GBMNotification):
    def __init__(self, root, notify_type):
        """
        Generic GBM location alert 

        :param root: parsed XML object
        :param notify_type: notification type (str)
        :returns: 
        :rtype: 

        """

        super(GBMLocationNotification, self).__init__(
            root=root, notify_type=notify_type
        )

    def action(self):

        # call the super action
        super(GBMLocationNotification, self).action()

        # parse the location info

        logger.debug(f"{self._burst_name} is gathering the location info")

        pos2d = self._root.find(".//{*}Position2D")
        ra = float(pos2d.find(".//{*}C1").text)
        dec = float(pos2d.find(".//{*}C2").text)
        radius = float(pos2d.find(".//{*}Error2Radius").text)

        # add the location informatioon onto the message

        self._add_line_to_msg(f"RA: {ra}")
        self._add_line_to_msg(f"Dec: {dec}")
        self._add_line_to_msg(f"Err: {radius}")


class GBMFLTNotification(GBMLocationNotification):
    
    def __init__(self, root):

        super(GBMFLTNotification, self).__init__(root=root, notify_type="FLT Position")

        
    def _get_light_curve_file(self):
        """
        download a light curve file

        :returns: 
        :rtype: 

        """

        logger.debug(f"{self._burst_name} is about to find its lightcurve file")

        lc_file = self._root.find(".//Param[@name='LightCurve_URL']").attrib["value"]

        for mod in ['all', 'lores34', 'medres34', 'hires34']:

            new_url = lc_file.replace('medres34', mod)


            self._download(new_url, f"{self._burst_name} GBM {mod} Lightcurve", use_bot=True)

    def action(self):

        super(GBMFLTNotification, self).action()

        self._get_light_curve_file()

        
        
    # def action(self):

    #     super(GBMFLTNotification, self).action()

    #     self._get_light_curve_file()


class GBMGNDNotification(GBMLocationNotification):
    def __init__(self, root):

        super(GBMGNDNotification, self).__init__(root=root, notify_type="GND Position")

    def action(self):

        super(GBMGNDNotification, self).action()




class GBMFinalNotification(GBMLocationNotification):
    def __init__(self, root):

        super(GBMFinalNotification, self).__init__(
            root=root, notify_type="Final Position"
        )

    def action(self):

        super(GBMFinalNotification, self).action()

        self._get_position_plot()

    def _get_position_plot(self):

        pos_file = self._root.find(".//Param[@name='LocationMap_URL']").attrib["value"]

        logger.debug(
            f"{self._burst_name} is attempting to download its GBM position plot"
        )

        
        
        
        self._download(pos_file, f"{self._burst_name} GBM 'Official' Position", use_bot=True)

        skymap_file = pos_file.replace('locplot','skymap')

        self._download(skymap_file, f"{self._burst_name} GBM 'Official' Skymap", use_bot=True)
        
        

class GBMAlertNotification(GBMNotification):
    def __init__(self, root):

        super(GBMAlertNotification, self).__init__(
            root=root, notify_type="General Alert"
        )


__all__ = [
    "GBMAlertNotification",
    "GBMFinalNotification",
    "GBMFLTNotification",
    "GBMGNDNotification",
]
