from configparser import ConfigParser
from lib.playlist import Playlist
from lib.display import Display
from lib.logger import log
from lib.api import API
import subprocess
import hashlib
import time
import os

log.info("Player V2 started")
os.system('export DISPLAY=:0')

settings_conf = ConfigParser()
settings_conf.read('conf/settings.ini')

def hash(list):
    convert_list = str(list)
    return hashlib.md5(convert_list.encode()).hexdigest()

# Play function
def play():
    return subprocess.Popen(['python3', 'app_sub.py'])

# Main script
lib_display = Display()
lib_playlist = Playlist()

if settings_conf.getboolean('SETTINGS', 'use_offline'):
    log.debug("Player::offline mode")
    play()
else:
    log.debug("Player::online mode")
    lib_api = API()

    player = None
    last_playlist_hash = None
    first_time = True
    while True:
        if lib_api.check_internet():
            log.debug("Internet::online")

            lib_display.display_sync()
            lib_playlist.playlist_sync()

            display_data = lib_display.display_load()
            playlist_media = lib_playlist.playlist_load()

            new_playlist_hash = hash(playlist_media)
            log.debug(f"Playlist::last hash: {last_playlist_hash}")
            log.debug(f"Playlist::new hash: {new_playlist_hash}")

            if first_time:
                player = play()

                time.sleep(2)
            else:
                time.sleep(120)  # 120 seconds = 2min

            lib_api.set_screenshot()

            if first_time:
                first_time = False
                last_playlist_hash = new_playlist_hash
            else:
                if new_playlist_hash != last_playlist_hash:
                    player.terminate()
                    player.wait()

                    last_playlist_hash = new_playlist_hash
                    player = play()
        else:
            log.debug("Internet::offline")
            if not player:
                player = play()