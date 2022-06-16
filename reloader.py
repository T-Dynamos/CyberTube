#!/usr/bin/python3
import kivy 
import sys
from kivy.lang import *
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import *
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import *
from kivy.utils import *
from kivy.metrics import dp
import _thread

screen_manager = ScreenManager()

class Card(MDCard,FakeRectangularElevationBehavior):
	pass

if platform != "android":
    Window.size = (dp(400),dp(600))

class Reload(MDApp):
    y = Window.size[0]
    x = Window.size[1]

    def build(self):
        screen_manager.add_widget(Builder.load_file(sys.argv[1]))
        return screen_manager
    def on_start(self):
        self.file_data = open(sys.argv[1],"r")
        _thread.start_new_thread(Clock.schedule_interval,(self.reload,0.5))
    def reload(self,*largs):
        if open(sys.argv[1],"r") != self.file_data:
            screen_manager.clear_widgets()
            try:
                screen_manager.add_widget(Builder.load_file(sys.argv[1]))
            except Exception as e:
                e = str(e).replace("\n","")
                screen_manager.add_widget(Builder.load_string(f"""
MDScreen:
    name:"Main"
    md_bg_color:1,0,0,1
    MDLabel: 
        text:'{str(e)}'  
        halign:"center"         
                """))
        else:
            pass

Reload().run()