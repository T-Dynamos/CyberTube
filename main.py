#!/usr/bin/python3

__version__ = "1.0"

import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import *
from kivy.metrics import dp
from functools import partial
from kivymd.uix.card import MDCard
import threading
from kivy.network.urlrequest import UrlRequest
import sys
from kivymd.uix.behaviors import *
from kivy.core.window import *
from kivymd.toast import toast as Toast2
from kivy.utils import platform
from kivy.utils import get_color_from_hex
import _thread 
from kivy.clock import Clock
import pytube
from pytube import YouTube
from kivy.config import Config
import os
import time



screen_manager = ScreenManager()

if platform != "android":
	Config.set('kivy', 'window_icon', 'logo.png')
	Config.set('kivy', 'height','600')
	Config.set('kivy','width','400')
	Window.size = (dp(400),dp(600))

class Card(MDCard,FakeRectangularElevationBehavior):
	pass

def threadRun(func,args):
	Clock.schedule_once(partial(func,args))


def Toast1(string,*largs):
	Toast2(string)


def Toast(string,*largs):
	if platform=="android":
		Toast2(string,gravity=80)

	else:
		threadRun(Toast1,string)


def download_file(self,link,filename,*largs):
	def change_screen(*largs):
		if screen_manager.has_screen("downloader"):
			screen_manager.remove_widget(screen_manager.get_screen("downloader"))
		screen_manager.add_widget(Builder.load_file("screens/downloader.kv"))
		screen_manager.current = "downloader"
	threadRun(change_screen,())
	path = ("/home/"+str(os.popen("whoami").read().split("\n")[0])+"/CyberTube") if platform != "android" else "/sdcard/CyberTube"
	if os.path.exists(path) == False:
		os.mkdir(path)
	file_path = path+"/"+filename
	def update_progress(request, current_size, total_size,*largs):
		print(current_size,total_size)
		def run(*largs):
			try:
				screen_manager.get_screen("downloader").ids.progressbar.value = current_size / total_size
			except Exception as e:
				print(str(e))
		threadRun(run,())
	def message(*largs):
		Toast("File downloaded successfully")
		time.sleep(1)
		Toast("Saved as  : "+file_path)
		screen_manager.current = "Main"
	req = UrlRequest(link, on_progress=update_progress,
					chunk_size=1024, on_success=message,
					file_path=file_path)

videoCard = open("screens/cards.kv","r").read().split("~~~")[0]

audioCard = open("screens/cards.kv","r").read().split("~~~")[-1]


class CyberTube(MDApp):

	y = Window.size[0]
	x = Window.size[1]

	link_image = ""
	link_title = ""
	total_video_files = 0
	total_audio_files = 0
	total_files = 0
	link_quality = ""
	link_size = 0
	pos = 0.9
	video_links = []
	audio_link = []

	modal = None

	pytube_version = str(pytube.__version__)
	kivy_version = str(kivy.__version__)
	python_version = str(sys.version).split("(")[0]
	__version__ = __version__


	screen_manager = screen_manager
	download_link = ""
	download_file = download_file

	#https://youtu.be/T0lzuaX_7WM

	def build(self):
		screen_manager.add_widget(Builder.load_file("screens/home.kv"))
		return screen_manager
	def show_warn(self):
		self.screen_manager.transition.direction="right"
		self.screen_manager.current = "Main"
	def check_url(self,show_toast=True):
		if "https://" in screen_manager.get_screen("Home").ids.url.text or "http://" in screen_manager.get_screen("Home").ids.url.text:
			self.vaild = True
			screen_manager.get_screen("Home").ids.url_status.text = "Url is Vaild"
			screen_manager.get_screen("Home").ids.url_status.text_color = get_color_from_hex("#35C973")
			screen_manager.get_screen("Home").ids.url_status_button.md_bg_color = get_color_from_hex("#35C973")
			if show_toast == True:
				self.url = str(screen_manager.get_screen("Home").ids.url.text)
				_thread.start_new_thread(self.get_url_info,())
		else:
			if show_toast == True:
				Toast("Please Check your URL first")
			if screen_manager.get_screen("Home").ids.url.text == "":
				screen_manager.get_screen("Home").ids.url_status.text = "Enter the URL"
			else:
				screen_manager.get_screen("Home").ids.url_status.text = "URL is not vaild"
			screen_manager.get_screen("Home").ids.url_status.text_color = get_color_from_hex("#C97174")
			screen_manager.get_screen("Home").ids.url_status_button.md_bg_color = get_color_from_hex("#C97174")
			self.vaild = True

	def spinner(self,text,*largs):
		self.modal = Builder.load_file("screens/util.kv")
		self.modal.open()

	def get_url_info(self,*largs):
		threadRun(self.spinner,())
		try:
			link_info  = YouTube(self.url)
			self.link_image =  link_info.thumbnail_url
			self.link_title =  link_info.title
			self.total_video_files = len(link_info.streams.filter(file_extension="mp4",only_video=True))
			self.total_audio_files = len(link_info.streams.filter(file_extension="webm",only_audio=True))
			self.total_files = self.total_video_files + self.total_audio_files
			self.video_links = link_info.streams.filter(file_extension="mp4",only_video=True)
			self.audio_links = link_info.streams.filter(file_extension="webm",only_audio=True)[::-1]
		except Exception:
			Toast("No or Slow Intenet")
			return self.modal.dismiss()
		self.modal.dismiss()
		def change_screen(*largs):
			screen_manager.add_widget(Builder.load_file("screens/main.kv"))
			screen_manager.transition.direction="left"
			screen_manager.current = "Main"
		threadRun(change_screen,())

	def open_video_downloader(self,*largs):
		import time
		def change(*largs):
			if screen_manager.has_screen("video"):
				screen_manager.remove_widget(screen_manager.get_screen("video"))

			screen_manager.add_widget(Builder.load_file("screens/video.kv"))
			screen_manager.transition.direction="left"
			screen_manager.current ="video"
		threadRun(change,())
		time.sleep(0.5)
		threadRun(self.spinner,())
		for count,links in enumerate(self.video_links):
			time.sleep(0.5)
			self.pos = self.pos-0.1
			self.link_quality = self.video_links[count].resolution
			self.link_size = str((self.video_links[count].filesize/1024)//1024)+" MB"
			self.download_link = self.video_links[count].url
			def addwidget(*largs):
				cardVideo = Builder.load_string(videoCard)
				screen_manager.get_screen("video").ids.card_container.add_widget(cardVideo)
			threadRun(addwidget,())
		threadRun(self.modal.dismiss,())

	def open_audio_downloader(self,*largs):
		import time
		def change(*largs):
			if screen_manager.has_screen("audio"):
				screen_manager.remove_widget(screen_manager.get_screen("audio"))
			screen_manager.add_widget(Builder.load_file("screens/audio.kv"))
			screen_manager.transition.direction="left"
			screen_manager.current ="audio"
		threadRun(change,())
		time.sleep(0.5)
		threadRun(self.spinner,())
		for count,links in enumerate(self.audio_links):
			time.sleep(0.5)
			self.pos = self.pos-0.1
			self.link_quality = self.audio_links[count].abr
			self.link_size = str((self.audio_links[count].filesize/1024)//1024)+" MB"
			self.download_link = self.audio_links[count].url
			def addwidget(*largs):
				cardaudio = Builder.load_string(audioCard)
				screen_manager.get_screen("audio").ids.card_container.add_widget(cardaudio)
			threadRun(addwidget,())
		threadRun(self.modal.dismiss,())			

CyberTube().run()
