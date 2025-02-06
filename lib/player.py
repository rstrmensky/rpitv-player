import subprocess
import time
import os

class Player:
    def __init__(self):
        self.process = None

    def set_display(self, width, height, x_axis, y_axis):
        self.width = width
        self.height = height
        self.x_axis = x_axis
        self.y_axis = y_axis

    def set_media(self, media, duration = 0):
        self.media = media
        self.duration = duration

    def play(self):
        raise NotImplemented

    def stop(self):
        raise NotImplemented

class VideoPlayer(Player):
    def __init__(self):
        super().__init__()
        self.player = 'mpv'

    def play(self):
        command = [self.player]
        if self.width != 0 and self.height != 0:
            command.append(f"--geometry={self.width}x{self.height}+{self.x_axis}+{self.y_axis}")
        else:
            command.append("--fullscreen")
        command.append(self.media)
        self.process = subprocess.run(command)

    def stop(self):
        os.system(f"sudo killall {self.player}")

class ImagePlayer(Player):
    def __init__(self):
        super().__init__()
        self.player = 'feh'

    def play(self):
        command = [self.player]
        if self.width != 0 and self.height != 0:
            command.append(f"--geometry={self.width}x{self.height}+{self.x_axis}+{self.y_axis}")
            command.append("--scale-down")
            command.append("--image-bg=black")
        else:
            command.append("--fullscreen")
        command.append(self.media)
        self.process = subprocess.Popen(command)
        if self.duration != 0:
            time.sleep(int(self.duration))
            self.process.terminate()
            self.process.wait()

    def stop(self):
        os.system(f"sudo killall {self.player}")