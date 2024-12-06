from lib.player import Player, VideoPlayer, ImagePlayer
from lib.playlist import Playlist

print(f"Starting player...")
playlist = Playlist()
media = playlist.load()

player = Player()
if len(media) == 1 and media[0]["media_type"] == "image":
    item = media[0]
    print(f"Displaying image: {item['file_path']} for {item['display_time']} seconds")
    player = ImagePlayer()
    player.set_asset(item['file_path'], item['display_time'])
    player.play()
else:
    while True:
        for item in media:
            if item["media_type"] == "video":
                print(f"Displaying video: {item['file_path']}")
                player = VideoPlayer()
                player.set_asset(item['file_path'], item['display_time'])
                player.play()
            elif item["media_type"] == "image":
                print(f"Displaying image: {item['file_path']} for {item['display_time']} seconds")
                player = ImagePlayer()
                player.set_asset(item['file_path'], item['display_time'])
                player.play()
                player.stop()