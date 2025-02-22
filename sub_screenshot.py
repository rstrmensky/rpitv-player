from lib.api import API
import time

lib_api = API()

while True:
    time.sleep(1)

    lib_api.set_screenshot()

    time.sleep(119) # Sleep 120sec = 2min