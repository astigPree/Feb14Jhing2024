
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.behaviors import BackgroundColorBehavior, CommonElevationBehavior
from kivy.uix.label import Label

from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock

import variables as data


# ======= Envelope Screen Activities
class EnvelopeExitButton(MDBoxLayout):
	command = ObjectProperty(None)


class EnvelopeBox(MDBoxLayout,CommonElevationBehavior,BackgroundColorBehavior):
	pass

		
class ShowEnvelopeScreen(Screen):
	maximum_height : float = NumericProperty(0.86)
	envelope_box : Widget = ObjectProperty(None)
	content_holder : Label = ObjectProperty(None)
	content_layout : Widget = ObjectProperty(None)
	
	duration : float = NumericProperty(2.0)
	
	isOpen : bool = BooleanProperty(False)
	
	content : str = StringProperty(data.content)
	
	def animateText(self , interval : float):
		if not self.content:
			exit_button = EnvelopeExitButton()
			exit_button.command = self.parent.changeScreen("new")
			self.content_layout.add_widget(exit_button)
			Animation(opacity = 1 ).start(exit_button)
			return 
		self.content_holder.text = self.content_holder.text + self.content[0]
		self.content = self.content[1:]
		Clock.schedule_once(self.animateText , interval)
	
	def animate(self):
		self.isOpen = True
		Animation(size_hint_y = self.maximum_height, duration = self.duration).start(self.envelope_box)
		
		speed = (self.duration * 2) / len(self.content)
		Clock.schedule_once(self.animateText, speed)
	
class MainWindow(ScreenManager):
	
	def changeScreen(self, name : str):
		pass
	
	def on_kv_post(self , *args):
		self.add_widget(ShowEnvelopeScreen(name = "envelope"))


class GiftApp(MDApp):
	
	def build(self):
		return Builder.load_file("main_design.kv")
		

LabelBase.register(name = "title_font", fn_regular="fonts/Love Castle Demo.ttf")
LabelBase.register(name="content_font", fn_regular="fonts/RomanticLove-Regular.ttf")
GiftApp().run()
