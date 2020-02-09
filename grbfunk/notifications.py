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
        
    

