import gcn
import telegram
import yaml
import lxml.etree

from grbfunk.notification_lookup import notification_lookup

import os


@gcn.include_notice_types(
    gcn.notice_types.FERMI_GBM_ALERT,  # Fermi GBM localization (flight)
    gcn.notice_types.FERMI_GBM_FLT_POS,  # Fermi GBM localization (flight)
    gcn.notice_types.FERMI_GBM_GND_POS,  # Fermi GBM localization (ground)
    gcn.notice_types.FERMI_GBM_FIN_POS,  # Fermi GBM localization (final)
)
def handler(payload, root):

    alert_type = int(root.find(".//Param[@name='Packet_Type']").attrib["value"])

    notification = notification_lookup[alert_type](root)

    # only send messages if we are NOT testing
