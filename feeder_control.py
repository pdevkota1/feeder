import RPi.GPIO as GPIO
from state import State
import time
import datetime
import logging
import picamera
import os.path


log = logging.getLogger(__name__)

MOTOR_PIN = 18
BUTTON_PIN = 25
KILL_TIME = 4
LOG_FILE = "/home/pi/tmp/feeder.log"
CAPTURE_DIR = "/home/pi/tmp/"
INFO_FILE = "/home/pi/Documents/feeder_info.log"



def setup_feeder():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def turn_motor_on():
    log.debug("MOTOR ON")
    GPIO.output(MOTOR_PIN, GPIO.HIGH)

def turn_motor_off():
    log.debug("MOTOR OFF")
    GPIO.output(MOTOR_PIN, GPIO.LOW)

def call_motor_off(ev=None):
    log.debug("BUTTON PRESSED")
    turn_motor_off()

def get_button_state():
    return GPIO.input(BUTTON_PIN)

def turn_motor_on_off(kill_time=KILL_TIME):
    state = State(get_button_state())
    init_time = time.time()
    turn_motor_on()
    while state.state != State.FINAL_PRESS and time.time() - init_time < kill_time:
        state.change_state(get_button_state())
        time.sleep(0.1)
    log.info("MOTOR ON: {:.2f} seconds".format(time.time() - init_time))
    turn_motor_off()

#def turn_feeder(kill_time=KILL_TIME):
#	camera = setup_camera()
#	setup_feeder()
#	log.debug("Turning feeder until button press or for {} secs".format(kill_time))
#	capture(camera, get_file_path())
#	turn_motor_on_off(kill_time=kill_time)
#	time.sleep(1)
#	capture(camera, get_file_path())

def turn_feeder(kill_time=KILL_TIME):
	camera = setup_camera()
	setup_feeder()
	capture(camera, get_file_path())
	turn_feeder_half_cycle(kill_time=kill_time)
	time.sleep(1)
	capture(camera, get_file_path())

def turn_feeder_half_cycle(kill_time=KILL_TIME):
    state = State(get_button_state())
    if state.state == State.INIT_PRESS:
        turn_feeder_until_state(State.OPEN, kill_time, state_plus_time=0.2)
    elif state.state == State.OPEN:
        turn_feeder_until_state(State.FINAL_PRESS, kill_time, state_plus_time=None)
    else:
        log.error("UNKNOWN INIT STATE ERROR {}".format(state))

def turn_feeder_until_state(final_state, kill_time, state_plus_time=None):
    state = State(get_button_state())
    log.debug("current state: {}, final requested state {}. extra time {}".format(state.state, final_state, state_plus_time))
    init_time = time.time()
    turn_motor_on()
    while state.state != final_state:
        if time.time() - init_time > kill_time:
            log.error("Kill time {} elapsed.  switch state {}. Killing motor".format(kill_time, state.state))
            turn_motor_off()
            return
        state.change_state(get_button_state())
        time.sleep(0.1)
    if state_plus_time:
        log.debug("sleeping past {} for time {}".format(state.state, state_plus_time))
        time.sleep(state_plus_time)
    log.info("MOTOR ON: {:.2f} seconds".format(time.time() - init_time))
    turn_motor_off()



######### CAMERA ########


def setup_camera():
	log.debug("setting up camera ... ")
	camera = picamera.PiCamera()
	camera.brightness = 80
	camera.iso = 1600
	camera.shutter_speed = camera.exposure_speed
	camera.start_preview()
	time.sleep(2)
	return camera

def capture(camera, picture_path):
	log.debug("taking picture and saving at %s " % picture_path)
	camera.capture(picture_path)

def get_file_path(root_dir=CAPTURE_DIR):
	dst_dir = os.path.join(root_dir, datetime.datetime.today().strftime("%y_%m_%d"))
	if not os.path.exists(dst_dir):
		os.makedirs(dst_dir)
	return os.path.join(dst_dir, datetime.datetime.now().strftime("%H_%M_%S")) + ".jpg"


######## MAIN ########

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

#if __name__ == "__main__":
#	import sys
#	set_logging()
#	if len(sys.argv) == 1:
#		turn_feeder(kill_time=KILL_TIME)
#	elif len(sys.argv) > 1:
#		turn_feeder(kill_time=float(sys.argv[1]))

if __name__ == "__main__":
	import sys
	set_logging()
	turn_feeder()

