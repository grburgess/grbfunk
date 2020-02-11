import telegram
import os

from grbfunk.utils.package_data import get_access_file


import coloredlogs, logging
import grbfunk.utils.log

logger = logging.getLogger("grbfunk.bot")


_DEBUG = False
if os.environ.get("GRBFUNK_DEBUG") is not None:

    if os.environ.get("GRBFUNK_DEBUG") == "True":

        _DEBUG = True

    # for travisCI
    _TRAVIS_TOKEN = os.environ("TOKEN")


class Bot(object):
    def __init__(self, name, token, chat_id):
        """
        A generic telegram bot

        :param name: the name of the bot
        :param token: the bot token
        :param chat_id: the chat id to talk to
        :returns: 
        :rtype: 

        """
        logger.debug(f"{name} bot is being constructed")

        # create the bot

        self._name = name
        self._chat_id = chat_id

        if _DEBUG:

            # if we are testing we send stuff to a special
            # chat. go ahead and spam me

            self._chat_id = "-1001284769525"
            if _TRAVIS_TOKEN is not None:

                token = _TRAVIS_TOKEN

        self._bot = telegram.Bot(token=token)

        self._msg_header = f"{self._name} says:\n"

    def speak(self, message):
        """
        send a message

        :param message: 
        :returns: 
        :rtype: 

        """

        full_msg = f"{self._msg_header}{message}"

        logger.info(f"{self._name} bot is sending: {message}")

        self._bot.send_message(chat_id=self._chat_id, text=full_msg)

    def show(self, image, description):
        """
        send an image

        :param image: 
        :param description: 
        :returns: 
        :rtype: 

        """

        full_msg = f"{self._msg_header}{description}"

        logger.info(f"{self._name} bot is sending the {description} image")

        self._bot.send_photo(
            chat_id=self._chat_id, photo=open(image, "rb"), caption=full_msg
        )


class GBMBot(Bot):
    def __init__(self):
        """
        A GBM bot

        :returns: 
        :rtype: 

        """

        token = access["token"]
        access = get_access_file()
        chat_id = access["chat_id"]

        super(GBMBot, self).__init__(name="GBM", token=token, chat_id=chat_id)
