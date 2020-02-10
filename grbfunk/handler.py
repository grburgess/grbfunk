import gcn
import telegram
import yaml
import lxml.etree

from grbfunk.notification_lookup import notification_lookup

import os


_DEBUG = False
if os.environ.get("GRBFUNK_DEBUG") is not None:

    if os.environ.get("GRBFUNK_DEBUG") == "True":

        _DEBUG = True


if not _DEBUG
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

    alert_type = int(root.find(".//Param[@name='Packet_Type']").attrib["value"])

    notification = notification_lookup[alert_type](root)

    # only send messages if we are NOT testing

    if not _DEBUG:
        bot.send_message(chat_id=chat_id, text=notification.message)

        for descr, download in notification.downloads.items():

            bot.send_photo(chat_id=chat_id, photo=open(download, "rb"), caption=descr)

    notification.cleanup()
