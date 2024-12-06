import os
import time

class Player:
    def __init__(self):
        os.environ['DISPLAY'] = ':0.0'

    def set_asset(self, path, duration):
        raise NotImplementedError

    def play(self):
        raise NotImplementedError

    def stop(self):
        os.system("sudo killall mpv")
        os.system("sudo killall fbi")

    def restart(self):
        os.system("sudo killall mpv")
        os.system("sudo killall fbi")

class VideoPlayer(Player):
    def __init__(self):
        super().__init__()

    def set_asset(self, path, duration = 5):
        self.path = path
        self.duration = duration

    def play(self):
        os.system(f"sudo mpv --fullscreen {self.path}")

    def stop(self):
        os.system("sudo killall mpv")

    def restart(self):
        super().restart()

class ImagePlayer(Player):
    def __init__(self):
        super().__init__()

    def set_asset(self, path, duration = 5):
        self.path = path
        self.duration = duration

    def play(self):
        os.system(f"sudo fbi -T 1 -d /dev/fb0 -noverbose -a {self.path}")
        if self.duration != 0:
            time.sleep(int(self.duration))

    def stop(self):
        os.system("sudo killall fbi")

    def restart(self):
        super().restart()