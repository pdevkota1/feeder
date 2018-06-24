from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import logging
import configparser
import os

log = logging.getLogger(__name__)


class FeederPublisher(object):

    def __init__(self, channel='feeder_update', listener_callback=None):
        self.pnconfig = PNConfiguration()
        config = configparser.ConfigParser()
        ini_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "feeder.ini")
        config.read(ini_path)
        self.pnconfig.subscribe_key = config["pubnub"]["subscribe_key"]
        self.pnconfig.publish_key = config["pubnub"]["publish_key"]
        self.pubnub = PubNub(self.pnconfig)
        self.channel = channel
        if listener_callback:
            self.add_listener(listener_callback)

    def add_listener(self, listener_callback):
        self.pubnub.add_listener(listener_callback)

    @staticmethod
    def publish_callback(result, status):
        log.debug("message sent.  Result {}".format(result))
        if status.error:
            log.error("{} during message publish. {}".format(result, status.error_data.information))

    def publish(self, message):
        self.pubnub.publish().channel(self.channel).message(message).async(self.publish_callback)

    def subscribe(self, subscriber_channel):
        self.pubnub.subscribe().channels(subscriber_channel).execute()


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        log.debug("presence call {}".format(presence))

    def status(self, pubnub, status):
        log.debug("status called {}".format(status))

    def message(self, pubnub, message):
        log.info("incoming message: [{}]".format(vars(message)))



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    FeederPublisher().publish(["hello", "again"])
