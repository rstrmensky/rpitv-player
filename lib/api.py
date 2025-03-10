from configparser import ConfigParser
from .logger import log
import screeninfo
import subprocess
import requests
import os.path
import base64

class API:
    def __init__(self):
        app_conf = ConfigParser()
        app_conf.read('conf/app.ini')
        self.url = app_conf.get('API', 'api_url')
        self.licence = app_conf.get('API', 'licence_token')
        self.display = app_conf.get('API', 'rpi_token')
        self.post_data = {
            'Api[licence_key]': self.licence,
            'Api[display_key]': self.display
        }
        self.screenshot = None

    def check_update(self):
        return self.do_request('check-update')

    def get_display(self):
        return self.do_request('get-display')

    def get_playlist(self):
        return self.do_request('get-playlist')

    def set_display(self):
        self.post_data['Api[resolution_width]'] = screeninfo.get_monitors()[0].width
        self.post_data['Api[resolution_height]'] = screeninfo.get_monitors()[0].height

        return self.do_request('set-display')

    def set_screenshot(self):
        file_screenshot = os.path.realpath("screenshot.jpg")
        file_screenshot_thumb = os.path.realpath("screenshot-thumb.jpg")

        subprocess.run(f"scrot -o -q 40 -t 30 {file_screenshot}", shell = True)
        with open(file_screenshot_thumb, "rb") as file:
            self.screenshot = base64.b64encode(file.read()).decode('utf-8')

        os.system(f"sudo rm {file_screenshot}")
        os.system(f"sudo rm {file_screenshot_thumb}")

        self.post_data['Api[screenshot]'] = self.screenshot
        return self.do_request('set-screenshot')

    def do_request(self, request_type):
        log.debug(f"API.do_request::request type: {request_type}")
        response = None
        try:
            response = requests.post(f"{self.url}/{request_type}", self.post_data)
            response.raise_for_status()
        except requests.HTTPError as http_err:
            log.error(f"API.do_request::HTTP error occurred: {http_err}")
        except requests.Timeout as timeout_err:
            log.error(f"API.do_request::timeout error occurred: {timeout_err}")
        except requests.RequestException as req_err:
            log.error(f"API.do_request::request error occurred: {req_err}")
        finally:
            if response is not None:
                log.debug(f"API.do_request::request status: {response.status_code} ")
                return response.json()