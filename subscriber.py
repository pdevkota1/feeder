from publisher import FeederPublisher
from publisher import MySubscribeCallback
import logging
import datetime
from feeder_control import turn_feeder

log = logging.getLogger(__name__)


def subscribe():
    subscriber = FeederPublisher(listener_callback=FeederSubscriberCallback())
    log.info("starting subscriber")
    subscriber.subscribe("feeder_input")


class FeederSubscriberCallback(MySubscribeCallback):

    TOKEN_KEY = "feedher"

    def message(self, pubnub, message):
        try:
            self.handle_message(message)
        except Exception as e:
            log.error("some exception occurred while handling message {}".format(e))

    def handle_message(self, message):
        log.debug("incoming message: [{}]".format(vars(message)))
        log.debug("incoming message message [{}]".format(message.message))
        log.debug("time stamp is {}".format(message.timetoken))
        received_time = datetime.datetime.fromtimestamp(int(message.timetoken) / 10000000)
        now = datetime.datetime.now()
        time_diff = now - received_time
        log.debug("difference in time is {}".format(time_diff))
        log.debug("received at {}".format(received_time))
        token_value = message.message["token"]
        if token_value == self.TOKEN_KEY and time_diff < datetime.timedelta(minutes=1):
            log.info("time to feed")
            turn_feeder()
        else:
            log.debug("not time to feed")

if __name__ == "__main__":
    from log_setting import set_logging
    set_logging()
    # logging.basicConfig(level=logging.DEBUG)
    subscribe()




