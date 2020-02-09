import re
import lxml.etree


class Notification(object):
    
    def __init__(self, root, instrument_name, notify_type):
        
        self._instrument_name  = instrument_name
        self._notify_type = notify_type
        self._root = lxml.etree.parse(open(root,'r'))
        
        self._message = ""
        
        self._build_message_header()


    def _add_line_to_msg(self, line):
        self._message += f"{line}\n"
        
    def action(self):
        pass 
    
    def _build_message_header(self):
        
        self._add_line_to_msg(f'{self._instrument_name} Notification')
        self._add_line_to_msg( f'Alert: {self._notify_type}')

    
    def _build_message(self):
        
        action_string = self.action()
        
        self._message += action_string
    
    def print(self):
        
        print(self._message)
    
    def send(self):
        
        pass
        
    

class GBMNotification(Notification):
    
    def __init__(self,root, notify_type):
        
        
        super(GBMNotification, self).__init__(instrument_name='GBM',root=root, notify_type=notify_type)
        
        
    def action(self):
        self._form_burst_name()
        
        pos2d = self._root.find('.//{*}Position2D')
        ra = float(pos2d.find('.//{*}C1').text)
        dec = float(pos2d.find('.//{*}C2').text)
        radius = float(pos2d.find('.//{*}Error2Radius').text)
        
    def _form_burst_name(self):
        tmp = self._root.find('.//{*}ISOTime').text
        yy, mm, dd = re.match('^\d\d(\d\d)-(\d\d)-(\d\d)T\d\d:\d\d:\d\d\.\d\d$', tmp).groups()
        
        
        self._burst_name = 'GRB{yy}{mm}{dd}xxx'
        
    
    
