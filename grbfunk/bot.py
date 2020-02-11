import telegram
import yaml


# we do not want to try and load all the tokens if they aren't there

path = os.path.join(os.path.expanduser("~"), ".grbfunk", "access.yaml")

with open(path) as f:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    access = yaml.load(f, Loader=yaml.SafeLoader)

token = access["token"]
chat_id = access["chat_id"]



class Bot(self):

    def __init__(self,name, token, chat_id):

        self._bot = telegram.Bot(token=token)
        self._name = name
        
        self._msg_header = f"{self._name} says:\n"

        
    def speak(self, message):

        full_msg = f"{self._msg_header}{message}"
        self._bot.send_message(chat_id = self._chat_id, text=full_msg)

    def show(self, image, description):

        full_msg = f"{self._msg_header}{description}"
        
        
        self._bot.send_photo(chat_id=self._chat_id,
                             photo=open(image, "rb"), caption=full_msg)

        
        
        
