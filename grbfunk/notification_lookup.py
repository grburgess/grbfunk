import gcn
from gbm_notifications import *

notification_lookup = {
    gcn.notice_types.FERMI_GBM_ALERT: GBMAlertNotification,
    gcn.notice_types.FERMI_GBM_FLT_POS: GBMFLTNotification,
    gcn.notice_types.FERMI_GBM_GND_POS: GBMGNDNotification,
    gcn.notice_types.FERMI_GBM_FIN_POS: GBMFinalNotification,
}
