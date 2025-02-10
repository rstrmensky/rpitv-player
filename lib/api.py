from configparser import ConfigParser
from .logger import log
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
        self.screenshot = None

    def check_internet(self):
        try:
            response = requests.get('http://www.google.com', timeout=5)
            return True if response.status_code == 200 else False
        except requests.ConnectionError:
            return False

    def get_display(self):
        return self.do_request('get-display')

    def get_playlist(self):
        return self.do_request('get-playlist')

    def set_screenshot(self):
        file_screenshot = os.path.realpath("screenshot.jpg")
        file_screenshot_thumb = os.path.realpath("screenshot-thumb.jpg")

        subprocess.run(f"scrot -o -q 40 -t 30 {file_screenshot}", shell=True)
        with open(file_screenshot_thumb, "rb") as file:
            self.screenshot = base64.b64encode(file.read()).decode('utf-8')
        response = self.do_request('set-screenshot')

        os.system(f"sudo rm {file_screenshot}")
        os.system(f"sudo rm {file_screenshot_thumb}")
        return response

    def do_request(self, request_type):
        log.debug(f"API.do_request::request type: {request_type}")
        try:
            response = requests.post(f"{self.url}/{request_type}", {
                'licence_token': self.licence,
                'rpi_token': self.display,
                'screenshot': self.screenshot
            })
            response.raise_for_status()
        except requests.HTTPError as http_err:
            log.error(f"API.do_request::HTTP error occurred: {http_err}")
        except requests.Timeout as timeout_err:
            log.error(f"API.do_request::Timeout error occurred: {timeout_err}")
        except requests.RequestException as req_err:
            log.error(f"API.do_request::Request error occurred: {req_err}")
        else:
            log.debug(f"API.do_request::Request status: {response.status_code} ")
            return response.json()