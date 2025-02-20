from lib.api import API
import time

lib_api = API()

while True:
    lib_api.set_screenshot()

    time.sleep(120) # Sleep 60sec = 1min