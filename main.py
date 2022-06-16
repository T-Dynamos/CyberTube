#!/usr/bin/python3

__version__ = "1.0"

import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import *
from kivy.metrics import dp
from functools import partial
from kivymd.uix.card import MDCard
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

screen_manager = ScreenManager()

if platform != "android":
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

videoCard = """
AnchorLayout:
	size_hint:None,None
	size:app.y,"50dp"
	Card:
		radius:dp(10)
		size_hint:None,None 
		ripple_behavior:True
		size:app.y-dp(30),"50dp"
		md_bg_color:app.theme_cls.primary_light
		RelativeLayout:
			BoxLayout:
				padding:dp(10)
				MDLabel:
					pos_hint:{"center_x":0.5,"center_y":0.5}
					text:"Download "+app.link_quality
					font_name:"assets/Poppins-Regular.ttf"
				MDLabel:
					id:text_total_audio
					pos_hint:{"center_x":0.5,"center_y":0.5}
					text:"File size "+app.link_size
					font_name:"assets/Poppins-Regular.ttf"
					font_size:"10sp"
				MDIconButton:
					pos_hint:{"center_x":0.9,"center_y":0.5}
					icon:"download"
"""


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

	#https://youtu.be/T0lzuaX_7WM

	def build(self):
		screen_manager.add_widget(Builder.load_file("screens/home.kv"))
		return screen_manager

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
			self.audio_links = link_info.streams.filter(file_extension="webm",only_audio=True)
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
			screen_manager.current ="video"
		threadRun(change,())
		time.sleep(0.5)
		threadRun(self.spinner,())
		for count,links in enumerate(self.video_links):
			time.sleep(0.5)
			self.pos = self.pos-0.1
			self.link_quality = self.video_links[count].resolution
			self.link_size = str((self.video_links[count].filesize/1024)//1024)+" MB"
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
			screen_manager.current ="audio"
		threadRun(change,())
		time.sleep(0.5)
		threadRun(self.spinner,())
		for count,links in enumerate(self.audio_links):
			time.sleep(0.5)
			self.pos = self.pos-0.1
			self.link_quality = self.audio_links[count].resolution
			self.link_size = str((self.audio_links[count].filesize/1024)//1024)+" MB"
			def addwidget(*largs):
				cardaudio = Builder.load_string(audioCard)
				screen_manager.get_screen("audio").ids.card_container.add_widget(cardaudio)
			threadRun(addwidget,())
		threadRun(self.modal.dismiss,())			

CyberTube().run()
