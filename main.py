#!/usr/bin/python3

__version__ = 1.0

import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import *
from kivy.metrics import dp
from functools import partial
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import *
from kivy.core.window import *
from kivymd.toast import toast as Toast2
from kivy.utils import platform
from kivy.utils import get_color_from_hex
import _thread 
from kivy.clock import Clock
from api import Downloader
from pytube import YouTube

screen_manager = ScreenManager()

if platform != "Android":
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


class CyberTube(MDApp):

	y = Window.size[0]
	x = Window.size[1]

	link_image = ""
	link_title = ""
	total_video_files = 0
	total_audio_files = 0
	total_files = 0
	video_links = []
	audio_link = []

	modal = None

	screen_manager = screen_manager

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

	def spinner(self,open=False,*largs):
		self.modal = Builder.load_file("screens/util.kv")
		self.modal.open()

	def get_url_info(self,*largs):
		threadRun(self.spinner,())
		link_info  = YouTube(self.url)
		self.link_image =  link_info.thumbnail_url
		self.link_title =  link_info.title
		self.total_video_files = len(link_info.streams.filter(file_extension="mp4",only_video=True))
		self.total_audio_files = len(link_info.streams.filter(file_extension="webm",only_audio=True))
		self.total_files = self.total_video_files + self.total_audio_files
		self.video_links = link_info.streams.filter(file_extension="mp4",only_video=True)
		self.audio_links = link_info.streams.filter(file_extension="webm",only_audio=True)
		print("Done")
		self.modal.dismiss()
		def change_screen(*largs):
			screen_manager.add_widget(Builder.load_file("screens/main.kv"))
			screen_manager.current = "Main"
		threadRun(change_screen,())
CyberTube().run()
