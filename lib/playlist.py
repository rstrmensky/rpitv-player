from configparser import ConfigParser
import requests
import hashlib
import csv
import os

class Playlist:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('conf/config.ini')

    def fetch_media(self):
        try:
            request = requests.get(self.config['main']['api_url'], params={
                'licence': self.config['licence']['licence_token'],
                'rpi_token': self.config['licence']['rpi_token']
            })
            request.raise_for_status()
            response = request.json()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            exit(1)

    def download_media(self, url, path):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            exit(1)

    def clean_up(self, current_media):
        for filename in os.listdir(self.config['main']['media_dir']):
            file_path = os.path.join(self.config['main']['media_dir'], filename)
            if file_path not in current_media:
                print(f"Cleaning up file: {file_path}")
                os.remove(file_path)

    def get_hash(self):
        try:
            with open(self.config['main']['playlist_file'], 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            return file_hash
        except FileNotFoundError:
            return None

    def load(self):
        playlist = []
        with open(self.config['main']['playlist_file'], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                playlist.append(row)
        return sorted(playlist, key=lambda x: int(x['display_order']))

    def update(self):
        print("Updating playlist...")
        media = self.fetch_media()

        # Track actual media
        current_media = set()

        # Open the playlist for writing
        with open(self.config['main']['playlist_file'], 'w', newline='') as csvfile:
            fieldnames = ['media_type', 'file_path', 'display_time', 'display_order']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Process each media item
            for item in media:
                file_url = item['file_path']
                local_path = os.path.join(self.config['main']['media_dir'], os.path.basename(file_url))
                current_media.add(local_path)

                # Download the file if it doesn't already exist
                if not os.path.exists(local_path):
                    print(f"Downloading {file_url} to {local_path}")
                    self.download_media(file_url, local_path)

                # Write the media item to the playlist file
                writer.writerow({
                    'media_type': item['media_type'],
                    'file_path': local_path,
                    'display_time': item['display_time'],
                    'display_order': item['display_order']
                })

        # Clean up old files in the media directory
        self.clean_up(current_media)

        print("Playlist updated successfully!")