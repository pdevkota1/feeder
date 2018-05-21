import logging

log = logging.getLogger(__name__)

class State(object):

    INIT_PRESS = "INIT_PRESS"
    OPEN = "OPEN"
    FINAL_PRESS = "FINAL_PRESS"

    def __init__(self, initial_state):
        if initial_state == 0:
            logging.debug("initial state is INIT_PRESSED")
            self.__state__ = self.INIT_PRESS
        else:
            logging.debug("initial state is OPEN")
            self.__state__ = self.OPEN

    def change_state(self, value):
        if value == 1:
            if self.__state__ == self.INIT_PRESS:
                logging.debug("changing state from INIT_PRESS to OPEN")
                self.__state__ = self.OPEN
        else:
            if self.__state__ == self.OPEN:
                logging.debug("changing state from OPEN to FINAL_PRESS")
                self.__state__ = self.FINAL_PRESS
     
    @property          
    def state(self):
        return self.__state__

