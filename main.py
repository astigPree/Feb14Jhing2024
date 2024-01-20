
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.behaviors import BackgroundColorBehavior, CommonElevationBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image

from kivy.properties import ListProperty, DictProperty, NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.core.audio import SoundLoader, Sound
from kivy.core.video import VideoBase, Video

import random

import variables as data

# ======= Timer Year Screen Activities
class PopUpImageOurPicture(MDBoxLayout,CommonElevationBehavior,BackgroundColorBehavior):
	my_image : Image = ObjectProperty(None)
	

class PopUpImageRedFlower(Image):
	currentAngle : int = NumericProperty(0)
	isOkeyToIncrement : bool = BooleanProperty(True)
	
	def increment(self , num = 1 ):
		if self.currentAngle == 180:
			self.isOkeyToIncrement = False
		
		if not self.isOkeyToIncrement:
			return 
		
		self.currentAngle += num
				
	def decrement(self , num = 1):
		if self.currentAngle == 0:
			self.isOkeyToIncrement = True
		
		if self.isOkeyToIncrement:
			return 
		
		self.currentAngle -= num
		
		

class ShowPopUpImageScreen(Screen):
	f_pic : PopUpImageOurPicture = ObjectProperty()
	s_pic : PopUpImageOurPicture = ObjectProperty()
	t_pic : PopUpImageOurPicture = ObjectProperty()
	
	f1 : PopUpImageRedFlower = ObjectProperty()
	f2 : PopUpImageRedFlower = ObjectProperty()
	f3 : PopUpImageRedFlower = ObjectProperty()
	f4 : PopUpImageRedFlower = ObjectProperty()
	
	rotation_delay = 1/30
	pop_up_delay = 2
	
	images = data.list_of_images
	
	open_animation = Animation( opacity = 1 , duration = pop_up_delay - 1)
	close_animation = Animation(opacity = 0 , duration = pop_up_delay - 1)
	
	def checkIfOpacity(self, num : int) -> bool : 
		if num == 1:
			return self.f_pic.opacity
		elif num == 2:
			return self.s_pic.opacity
		else:
			return self.t_pic.opacity
			
	
	def selectionOfImages(self, anim : Animation , num : int , image : str):
		if num == 1:
			selected_image = self.f_pic
		elif num == 2:
			selected_image = self.s_pic
		else:
			selected_image = self.t_pic
		
		if image:
			selected_image.my_image.source = image
		anim.start(selected_image)
		
	
	def animatePopUpImages(self , interval : float):
		what_to_open = random.randint(1 , 3)
		what_to_close = random.randint(1 , 3)
		what_image = random.randint(0, len(self.images)-1)
		
		if not self.checkIfOpacity(what_to_open):
			self.selectionOfImages(self.open_animation , what_to_open , self.images[what_image])	
		if what_to_close == what_to_open:
			Clock.schedule_once(self.animatePopUpImages, self.pop_up_delay)
			return 
		self.selectionOfImages(self.close_animation, what_to_close, None)
		Clock.schedule_once(self.animatePopUpImages , self.pop_up_delay)
		
	def animateMovingFlower(self , interval : float):
		self.f1.increment()
		self.f1.decrement()
		self.f2.increment()
		self.f2.decrement()	
		self.f3.increment()
		self.f3.decrement()
		self.f4.increment()
		self.f4.decrement()
		
		Clock.schedule_once(self.animateMovingFlower , self.rotation_delay)
	
	def on_enter(self , *args):
		self.f1.currentAngle = 180
		self.f3.currentAngle = 180
		
		Clock.schedule_once(self.animateMovingFlower , self.rotation_delay)
		Clock.schedule_once(self.animatePopUpImages, self.pop_up_delay)
		
		
		
		
	
# ======= Timer Year Screen Activities
class ShowTimerYearScreen(Screen):
	numer_3 : Label = ObjectProperty(None)
	numer_4 : Label = ObjectProperty(None)
	with_you : Label = ObjectProperty(None)
	labyu : Label = ObjectProperty(None)
	
	duration : int = NumericProperty(1.5)
	
	def withYouAnimation(self , interval : int):
		if self.numer_4.opacity >= 0.65 :
			anim = Animation( pos_hint = {"top":0.85} , duration = 1 )
			anim.start(self.with_you)
			anim = Animation(opacity= 1 , duration = 1.5 )
			anim.start(self.labyu)
			return 
		Clock.schedule_once(self.withYouAnimation , 1/30)
	
	def on_enter(self , *args):
		def delay(_):
			anim_3 = Animation(
				opacity = 0,
				pos_hint ={ "center_x" :  -0.5 } , 
				duration = self.duration) 
			anim_3.start(self.numer_3)
			
			anim_4 = Animation(
				opacity = 1 , pos_hint ={ "center_x" : 0.5 } ,
			 	duration = self.duration)
			anim_4.start(self.numer_4)
		
		
		Clock.schedule_once(delay , 1)
		Clock.schedule_once(self.withYouAnimation , 1/30)


# ======= Songs Screen Activities
class LyricsContainer(MDBoxLayout,CommonElevationBehavior,BackgroundColorBehavior):
	pass

class ShowLoveSoundScreen(Screen):
	
	sound : Sound= ObjectProperty(None)
	video : Video = ObjectProperty(None)
	
	content_holder : MDBoxLayout = ObjectProperty(None)
	
	lyrics : str = data.miss_miss_lyrics
	lyrics_holder : Label = ObjectProperty(None)
	song_duration = 20
	
	def animateText(self , interval : float):
		if not self.lyrics:
			return 
		
		print(self.sound.state)
		print(f"current sound pos : {self.sound.get_pos()} and word {self.lyrics[0]}")
		self.lyrics_holder.text = self.lyrics_holder.text + self.lyrics[0]
		self.lyrics = self.lyrics[1:]
		Clock.schedule_once(self.animateText , interval)
		
	def on_enter(self , *args):
		self.sound = SoundLoader.load("Musics/miss miss cutted.mp3")
		if self.sound:
			self.sound.play()

		def delayMusic(interval : float):
			interval = self.song_duration / len(self.lyrics)
			Clock.schedule_once(self.animateText , interval)
		
		Clock.schedule_once(delayMusic , 2.7)
		

# ======= I Love You Screen Activities
class  ILoveYouExitButton(MDBoxLayout):
	command : callable = ObjectProperty()
	isOkeyToNext : bool = BooleanProperty(False)

class ILoveYouBox(MDBoxLayout):
	pass

class ShowILoveYouScreen(Screen):
	iloveyoubox : ILoveYouBox = ObjectProperty(None)
	
	maximum_height = data.maximum_height
	
	duration : float = NumericProperty(1.0)
	
	list_of_heights = data.list_of_heights
	
	
	def checkIsDoneAnimating(self , interval : int) :
		if self.iloveyoubox.size_hint_y == self.maximum_height:
			anim = Animation(opacity = 1 , duration = 4)
			anim.start(self.ids["header"])
			anim.start(self.ids["footer"])
			return 
		Clock.schedule_once(self.checkIsDoneAnimating, 1 /30)
	
	def checkIsDoneToNextPage(self, interval : float):
		if self.ids["header"].opacity and self.ids["footer"].opacity:
			Animation(size_hint_y= 0 , duration= 3).start(self.ids["cover"])
			return 
		Clock.schedule_once(self.checkIsDoneToNextPage, 1/30)
	
	def on_enter(self , *args):
		animation : Animation = None
		#self.iloveyoubox.size_hint_y = 0.3
		for hint_y , duration in self.list_of_heights:
			if animation:
				animation = animation + Animation(size_hint_y = hint_y , duration=duration )
			else:
				animation = Animation(size_hint_y = hint_y , duration=duration)
		animation.start(self.iloveyoubox)
		
		Clock.schedule_once(self.checkIsDoneAnimating, 1/30)
		Clock.schedule_once(self.checkIsDoneToNextPage, 1/30)
	
	
		
		
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
	
	duration : float = NumericProperty(1.0)
	
	isOpen : bool = BooleanProperty(False)
	
	content : str = StringProperty(data.content)
	
	def animateText(self , interval : float):
		if not self.content:
			exit_button = EnvelopeExitButton()
			exit_button.command = lambda : self.parent.changeScreen("i love you")
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
	
	def on_leave(self, *args):
		Animation(opacity = 0 ).start(self)
	
	
class MainWindow(ScreenManager):
	
	list_of_screens : dict = DictProperty({})
	
	def changeScreen(self, name : str):
		self.switch_to(self.list_of_screens[name])
	
	def on_kv_post(self , *args):
		self.list_of_screens["i love you"] = ShowILoveYouScreen(name = "i love you")
		self.list_of_screens["envelope"] = ShowEnvelopeScreen(name = "envelope")
		self.list_of_screens["love sound"] = ShowLoveSoundScreen(name = "love sond")
		self.list_of_screens["timer year"] = ShowTimerYearScreen(name = "timer year")
		self.list_of_screens["popup image"] = ShowPopUpImageScreen(name = "popup image")
		
		self.switch_to(self.list_of_screens["popup image"])
		#self.switch_to(self.list_of_screens["timer year"])
		#self.switch_to(self.list_of_screens["love sound"])
		#self.switch_to(self.list_of_screens["envelope"])
		#self.switch_to(self.list_of_screens["i love you"])


class GiftApp(MDApp):
	
	def build(self):
		#current_icon_font = self.theme_cls.i
#		print(f"Current Icon Font: {current_icon_font}")
#		self.theme_cls.icon_font = "mdi"
		return Builder.load_file("main_design.kv")
		

LabelBase.register(name = "title_font", fn_regular="fonts/Love Castle Demo.ttf")
LabelBase.register(name="content_font", fn_regular="fonts/RomanticLove-Regular.ttf")
GiftApp().run()
