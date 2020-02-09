import gcn
import telegram
import yaml

from grbfunk.notification_lookup import notification_lookup

import os


path = os.path.join(os.path.expanduser("~"), ".grbfunk", "access.yaml")

with open(path) as f:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    access = yaml.load(f, Loader=yaml.SafeLoader)

token = access["token"]
chat_id = access["chat_id"]


bot = telegram.Bot(token=token)


@gcn.include_notice_types(
    gcn.notice_types.FERMI_GBM_ALERT,  # Fermi GBM localization (flight)
    gcn.notice_types.FERMI_GBM_FLT_POS,  # Fermi GBM localization (flight)
    gcn.notice_types.FERMI_GBM_GND_POS,  # Fermi GBM localization (ground)
    gcn.notice_types.FERMI_GBM_FIN_POS,  # Fermi GBM localization (final)
)
def handler(payload, root):

    # tmp_root = lxml.etree.parse(open(root, "r"))
    # alert_type = tmp_root.find(".//Param[@name='Packet_Type']").attrib["value"]
    alert_type = int(root.find(".//Param[@name='Packet_Type']").attrib["value"])

    notification = notification_lookup[alert_type](root)

    bot.send_message(chat_id=chat_id, text=notification.message)

    for descr, download in notification.downloads.items():

        bot.send_photo(chat_id=chat_id, photo=open(download, 'rb'), caption=descr)

    notification.cleanup()
