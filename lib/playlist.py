from configparser import ConfigParser
from .logger import log
from .api import API
import requests
import sqlite3
import os

class Playlist:
    def __init__(self):
        settings_conf = ConfigParser()
        settings_conf.read('conf/settings.ini')
        self.db_app = settings_conf.get('SETTINGS', 'db_app')
        self.dir_media = settings_conf.get('SETTINGS', 'dir_media')
        self.img_first = settings_conf.get('SETTINGS', 'img_first')

    def playlist_load(self):
        self.db_conn = sqlite3.connect(self.db_app)
        self.db = self.db_conn.cursor()
        self.db.execute('SELECT media_type, file_path, display_time, display_order FROM playlist')
        playlist_media = self.db.fetchall()
        self.db.close()

        log.debug('Playlist.playlist_load::done')
        return playlist_media

    def playlist_sync(self):
        lib_api = API()
        playlist_media = lib_api.get_playlist()

        if playlist_media:
            self.db_conn = sqlite3.connect(self.db_app)
            self.db = self.db_conn.cursor()

            self.db.execute('DELETE FROM playlist')

            actual_media = set()

            # !IMPORTANT! - Don't remove files
            actual_media.add(self.img_first)

            for index, media in enumerate(playlist_media, start = 1):
                local_path = os.path.join(self.dir_media, os.path.basename(media['file_path']))
                actual_media.add(local_path)
                log.debug(f"Playlist.playlist_sync::media: {local_path}")
                self.db.execute(
                    'INSERT INTO playlist (id, media_type, file_path, display_time, display_order) VALUES (?, ?, ?, ?, ?)',
                    (index, media['media_type'], local_path, media['display_time'], media['display_order']))
                if not os.path.exists(local_path):
                    log.debug(f"Playlist.playlist_sync::downloading media...")
                    try:
                        response = requests.get(media['file_path'], stream = True)
                        response.raise_for_status()
                    except requests.RequestException as req_err:
                        log.error(f"Playlist.playlist_sync::download error occurred: {req_err}")
                    else:
                        with open(local_path, 'wb') as file:
                            file.write(response.content)
                            log.debug(f"Playlist.playlist_sync::downloading done")
                else:
                    log.debug(f"Playlist.playlist_sync::media already exists")

            for filename in os.listdir(self.dir_media):
                file_path = os.path.join(self.dir_media, filename)
                if file_path not in actual_media:
                    log.debug(f"Playlist.playlist_sync::cleaning up file: {file_path}")
                    os.remove(file_path)

            self.db_conn.commit()
            self.db_conn.close()
            log.debug('Playlist.playlist_sync::done')
        else:
            log.debug('Playlist.playlist_sync::error')

        return self.playlist_load()