from configparser import ConfigParser
from lib.playlist import Playlist
from lib.display import Display
from lib.logger import log
from lib.api import API
import subprocess
import hashlib
import signal
import time
import os

log.info("-----------------------------")
log.info("|  RPiTV Player V2 started  |")
log.info("-----------------------------")
os.system('export DISPLAY=:0')

settings_conf = ConfigParser()
settings_conf.read('conf/settings.ini')

def hash(list):
    convert_list = str(list)
    return hashlib.md5(convert_list.encode()).hexdigest()

def sub_player():
    return subprocess.Popen(['python3', 'sub_player.py'], preexec_fn = os.setsid)

def sub_screenshot():
    return subprocess.Popen(['python3', 'sub_screenshot.py'])

player = sub_player()
player.run = True

sub_screenshot()

if not settings_conf.getboolean('SETTINGS', 'use_offline'):
    lib_display = Display()
    lib_playlist = Playlist()
    lib_api = API()

    # First run - check empty playlist
    display_data = lib_display.display_load()
    playlist_media = lib_playlist.playlist_load()

    if not display_data and not playlist_media:
        last_playlist_hash = hash(playlist_media)

        lib_api.set_display()
        display_data = lib_display.display_sync()
        playlist_media = lib_playlist.playlist_sync()

        new_playlist_hash = hash(playlist_media)

        if last_playlist_hash != new_playlist_hash:
            os.killpg(os.getpgid(player.pid), signal.SIGKILL)
            player.run = False

    while True:
        if not player.run:
            player = sub_player()
            player.run = True

        time.sleep(300)  # Sleep 300sec = 5min

        if bool(lib_api.check_update()):
            lib_display.display_sync()
            lib_playlist.playlist_sync()
            os.killpg(os.getpgid(player.pid), signal.SIGKILL)
            player.run = False