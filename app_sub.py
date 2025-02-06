from lib.playlist import Playlist
from lib.display import Display
from lib.player import ImagePlayer, VideoPlayer
from lib.logger import log

log.info("Starting player...")

lib_display = Display()
lib_playlist = Playlist()

display_data = lib_display.display_load()
playlist_media = lib_playlist.playlist_load()
log.debug(f"Display: {display_data}")
log.debug(f"Playlist: {playlist_media}")

while True:
    for media in playlist_media:
        if media[0] == 'image':
            log.info(f"Playing image: {media[1]}, duration: {media[2]}")
            lib_player = ImagePlayer()
            lib_player.set_display(display_data[0], display_data[1], display_data[2], display_data[3])
            lib_player.set_media(media[1], media[2])
            lib_player.play()
        elif media[0] == "video":
            log.info(f"Playing video: {media[1]}")
            lib_player = VideoPlayer()
            lib_player.set_display(display_data[0], display_data[1], display_data[2], display_data[3])
            lib_player.set_media(media[1])
            lib_player.play()