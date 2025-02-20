from configparser import ConfigParser
from lib.playlist import Playlist
from lib.display import Display
from lib.player import Player
from lib.logger import log

settings_conf = ConfigParser()
settings_conf.read('conf/settings.ini')

display_data = Display().display_load()
playlist_media = Playlist().playlist_load()

log.debug(f"Display.info:: {display_data}")
log.debug(f"Playlist.info:: {playlist_media}")

if display_data and playlist_media:
    while True:
        for media in playlist_media:
            log.info(f"Player:: {media[1]}, duration: {media[2]}")
            lib_player = Player()
            lib_player.set_display(display_data[0], display_data[1], display_data[2], display_data[3])
            lib_player.set_media(media[0], media[1], media[2])
            lib_player.play()
else:
    log.warning(f"!!! Empty playlist !!!")
    lib_player = Player()
    lib_player.set_display()
    lib_player.set_media('image', settings_conf.get('SETTINGS', 'img_first'))
    lib_player.play()