import logging

LOG_FILE = "/home/pi/tmp/feeder.log"
INFO_FILE = "/home/pi/Documents/feeder_info.log"


def set_logging(log_file=LOG_FILE, info_file=INFO_FILE):
    root_logger = logging.getLogger()
    debug_hdlr = logging.FileHandler(log_file)
    info_hdlr = logging.FileHandler(info_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    debug_hdlr.setFormatter(formatter)
    debug_hdlr.setLevel(logging.DEBUG)
    info_hdlr.setFormatter(formatter)
    info_hdlr.setLevel(logging.INFO)
    root_logger.addHandler(debug_hdlr)
    root_logger.addHandler(info_hdlr)
    root_logger.setLevel(logging.DEBUG)