#!/usr/bin/python3

__version__ = 1.0

import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import *
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import *
from kivy.core.window import *
from api import Downloader

screen_manager = ScreenManager()


class Card(MDCard,FakeRectangularElevationBehavior):
	pass



class CyberTube(MDApp):

	y = Window.size[0]
	x = Window.size[1]
	
	def build(self):
		screen_manager.add_widget(Builder.load_file("screens/home.kv"))
		return screen_manager

CyberTube().run()
