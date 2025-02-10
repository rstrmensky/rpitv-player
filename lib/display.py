from configparser import ConfigParser
from .logger import log
from .api import API
import sqlite3

class Display:
    def __init__(self):
        settings_conf = ConfigParser()
        settings_conf.read('conf/settings.ini')
        self.db_app = settings_conf.get('SETTINGS', 'db_app')
        self.dir_media = settings_conf.get('SETTINGS', 'dir_media')

    def display_load(self):
        self.db_conn = sqlite3.connect(self.db_app)
        self.db = self.db_conn.cursor()
        self.db.execute('SELECT window_width, window_height, x_axis, y_axis FROM display')
        display_data = self.db.fetchone()
        self.db.close()

        log.debug('Display.display_load::done')
        return display_data

    def display_sync(self):
        lib_api = API()
        display_data = lib_api.get_display()

        self.db_conn = sqlite3.connect(self.db_app)
        self.db = self.db_conn.cursor()

        self.db.execute('DELETE FROM display')

        self.db.execute(
            'INSERT INTO display (id, window_width, window_height, x_axis, y_axis) VALUES (?, ?, ?, ?, ?)',
            (1, display_data['display_width'], display_data['display_height'], display_data['display_x'], display_data['display_y']))

        self.db_conn.commit()
        self.db_conn.close()
        log.debug('Display.display_sync::done')