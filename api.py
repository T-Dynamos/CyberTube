
import os
from pytube import YouTube
import platform


class Downloader:
    def __init__(self , link , filename):

        self.link = link
        self.filename = filename

    def download(self):

        if "Linux" in platform.platform():
            path = "/home/Cyber-Tube"
        elif "Windows" in platform.platform():
            path = os.getcwd()
        else:
            path = "/sdcard/Cyber-Tube"

        object = YouTube(self.link).streams.get_by_resolution("720p").download(output_path=path , filename=self.filename)
