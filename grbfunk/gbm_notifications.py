import os
import re

from grbfunk.notifications import Notification


class GBMNotification(Notification):
    def __init__(self, root, notify_type):
        """
        Generic GBM alert providing basic 
        functionality

        :param root: the parsed xml file
        :param notify_type: the type of notification (str)
        :returns: 
        :rtype: 

        """

        super(GBMNotification, self).__init__(
            instrument_name="GBM", root=root, notify_type=notify_type
        )

    def action(self):

        # parse the name of the GRB
        self._form_burst_name()

        # add it to the list
        self._add_line_to_msg(f"Name: {self._burst_name}")

    def _form_burst_name(self):
        """
        forms the burst name form the GCN
        """
        tmp = self._root.find(".//{*}ISOTime").text
        yy, mm, dd = re.match(
            "^\d\d(\d\d)-(\d\d)-(\d\d)T\d\d:\d\d:\d\d\.\d\d$", tmp
        ).groups()

        self._burst_name = f"GRB{yy}{mm}{dd}xxx"

    def _get_light_curve_file(self):
        """
        download a light curve file

        :returns: 
        :rtype: 

        """
        
        lc_file = self._root.find(".//Param[@name='LightCurve_URL']").attrib["value"]

        directory = os.path.join("/tmp", self._burst_name)

        if not os.path.exists(directory):

            os.mkdir(directory)

        self._lc_file = self._download(lc_file, directory, "GBM Lightcurve")


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

    def action(self):

        super(GBMFLTNotification, self).action()

        self._get_light_curve_file()


class GBMGNDNotification(GBMLocationNotification):
    def __init__(self, root):

        super(GBMGNDNotification, self).__init__(root=root, notify_type="GND Position")

    def action(self):

        super(GBMGNDNotification, self).action()

        self._get_light_curve_file()


class GBMFinalNotification(GBMLocationNotification):
    def __init__(self, root):

        super(GBMFinalNotification, self).__init__(
            root=root, notify_type="Final Position"
        )

    def action(self):

        super(GBMFinalNotification, self).action()

        self._get_light_curve_file()


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