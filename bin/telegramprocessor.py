import logging
import bin.settings as settings
from api.telegram.telegramupdates import TelegramUpdates

# Configure logging
logger = logging.getLogger(__name__)

class TelegramProcessor():
    def __init__(self):
        logger.info("Start TelegramProcessor Processor")

    def process_telegramupdatebatch(self):
        logger.info("Process telegrambatch")
        self.tgu = TelegramUpdates()

        for update in self.tgu.json['result']:
            # Get all the keys from the update
            updatekeys = update.keys()

            if 'channel_post' in updatekeys:
                self.process_channelpost(update)

    def process_channelpost(self,update):
        if update['channel_post']['text'].upper() == '/START':
            channelid = str(update['channel_post']['sender_chat']['id'])
            logger.info("Request to enable channel: {}".format(channelid))
            if channelid in settings.config.telegramactivatedchannels:
                logger.info("Channel is already enabled")
            else:
                logger.info("Enabling channel")
                settings.config.update_telegramsettings(
                    telegramchannel=channelid)
        else:
            logger.info("Someone is talking, but I can't understand it")

        currentupdateid = int(settings.config.telegramlastprocessedupdateid)
        if currentupdateid <= update['update_id']:
            logger.info("Updating Telegram Update ID")
            settings.config.update_telegramsettings(
                updateid=(str(update['update_id'])))

    def start(self,pollinterval=60):
        logger.info("Starting Telegram processor cycle")
        while True:
            self.process_telegramupdatebatch()
            logger.info("Telegram cycle keep alive message")

