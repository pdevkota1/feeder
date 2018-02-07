from feeder_control import setup_camera, capture, get_file_path

camera = setup_camera()
capture(camera, get_file_path())
