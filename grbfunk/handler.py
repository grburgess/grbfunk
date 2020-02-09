import gcn

from notifications import notification_lookup


@gcn.include_notice_types(
    gcn.notice_types.FERMI_GBM_ALERT,  # Fermi GBM localization (flight)
    gcn.notice_types.FERMI_GBM_FLT_POS,  # Fermi GBM localization (flight)
    gcn.notice_types.FERMI_GBM_GND_POS,  # Fermi GBM localization (ground)
    gcn.notice_types.FERMI_GBM_FIN_POS,# Fermi GBM localization (final)
)  
def handler(payload, root):
    # Look up right ascension, declination, and error radius fields.
    alert_type = root.find(".//Param[@name='Packet_Type']").attrib["value"]

    notification = notification_lookup[alert_type](root)

    
