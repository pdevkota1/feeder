from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import logging

log = logging.getLogger(__name__)


class FeederPublisher(object):

    def __init__(self, channel='feeder_update'):
        self.pnconfig = PNConfiguration()
        self.pnconfig.subscribe_key = 'sub-c-6ee929f0-03c3-11e8-91aa-36923a88c219'
        self.pnconfig.publish_key = 'pub-c-335c509e-e691-41ce-9161-9949a4cda8b2'
        self.pubnub = PubNub(self.pnconfig)
        self.channel = channel

    @staticmethod
    def publish_callback(result, status):
        log.debug("message sent.  Result {}".format(result))
        if status.error:
            log.error("{} during message publish. {}".format(result, status.error_data.information))

    def publish(self, message):
        self.pubnub.publish().channel(self.channel).message(message).async(self.publish_callback)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    FeederPublisher().publish(["hello", "again"])
