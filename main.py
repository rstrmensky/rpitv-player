from lib.playlist import Playlist
from lib.player import Player
import subprocess
import time

def run_player():
    return subprocess.Popen(["python", "start_player.py"])

player = None

try:
    playlist = Playlist()

    # Update playlist
    playlist.update()
    last_playlist_hash = playlist.get_hash()

    # Start player process
    player = run_player()

    # Check for updates every 5 minutes
    while True:
        time.sleep(300) # 300 seconds = 5 minutes

        playlist.update()
        new_playlist_hash = playlist.get_hash()

        # Reload player if playlist has changed
        if new_playlist_hash != last_playlist_hash:
            if player:
                player.terminate()

            player = run_player()
            last_playlist_hash = new_playlist_hash

        if player is None:
            player = run_player()

except KeyboardInterrupt:
    if player:
        Player().stop()