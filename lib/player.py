import subprocess
import time
import os

class Player:
    def __init__(self):
        self.process = None
        self.player = None

    def set_display(self, width = 0, height = 0, x_axis = 0, y_axis = 0):
        self.width = width
        self.height = height
        self.x_axis = x_axis
        self.y_axis = y_axis

    def set_media(self, type, media, duration = 0):
        self.type = type
        if self.type == 'image':
            self.player = 'feh'
        else:
            self.player = 'mpv'
        self.media = media
        self.duration = duration

    def play(self):
        command = [self.player]
        if self.width != 0 and self.height != 0:
            command.append(f"--geometry={self.width}x{self.height}+{self.x_axis}+{self.y_axis}")
            if self.type == 'image':
                command.append("--scale-down")
                command.append("--image-bg=black")
        else:
            command.append("--fullscreen")
        command.append(self.media)

        if self.type == 'video':
            self.process = subprocess.run(command)
        else:
            self.process = subprocess.Popen(command)
            if self.duration != 0:
                time.sleep(int(self.duration))
                self.process.terminate()
                self.process.wait()

    def stop(self):
        os.system(f"sudo killall {self.player}")