import re
import os
import lxml.etree
import gcn

import collections

from grbfunk.utils.download_file import download_file


class Notification(object):
    def __init__(self, root, instrument_name, notify_type):

        self._instrument_name = instrument_name
        self._notify_type = notify_type
        
        #self._root = lxml.etree.parse(open(root, "r"))
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

    
class GBMNotification(Notification):
    def __init__(self, root, notify_type):

        super(GBMNotification, self).__init__(
            instrument_name="GBM", root=root, notify_type=notify_type
        )

    def action(self):
        self._form_burst_name()

        self._add_line_to_msg(f"Name: {self._burst_name}")

    def _form_burst_name(self):
        tmp = self._root.find(".//{*}ISOTime").text
        yy, mm, dd = re.match(
            "^\d\d(\d\d)-(\d\d)-(\d\d)T\d\d:\d\d:\d\d\.\d\d$", tmp
        ).groups()

        self._burst_name = f"GRB{yy}{mm}{dd}xxx"

    def _get_light_curve_file(self):

        lc_file = self._root.find(".//Param[@name='LightCurve_URL']").attrib["value"]

        directory = os.path.join("/tmp", self._burst_name)

        if not os.path.exists(directory):
            
            os.mkdir(directory)
        
        self._lc_file = self._download(lc_file, directory, 'GBM Lightcurve')


class GBMLocationNotification(GBMNotification):
    def __init__(self, root, notify_type):

        super(GBMLocationNotification, self).__init__(
            root=root, notify_type=notify_type
        )

    def action(self):

        super(GBMLocationNotification, self).action()

        pos2d = self._root.find(".//{*}Position2D")
        ra = float(pos2d.find(".//{*}C1").text)
        dec = float(pos2d.find(".//{*}C2").text)
        radius = float(pos2d.find(".//{*}Error2Radius").text)

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


notification_lookup = {
    gcn.notice_types.FERMI_GBM_ALERT: GBMAlertNotification,
    gcn.notice_types.FERMI_GBM_FLT_POS: GBMFLTNotification,
    gcn.notice_types.FERMI_GBM_GND_POS: GBMGNDNotification,
    gcn.notice_types.FERMI_GBM_FIN_POS: GBMFinalNotification,
}
