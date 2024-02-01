
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.behaviors import BackgroundColorBehavior, CommonElevationBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from kivy.properties import  DictProperty, NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.core.audio import SoundLoader, Sound

import random, math, os

import variables as data

# ======= Flowering Picture Screen Activities
class PopUpImageImageBackground(MDBoxLayout, CommonElevationBehavior, BackgroundColorBehavior):
	pass
	
class ShowFloweringPictureScreen(Screen):
	
	lyrics : str = StringProperty("")
	
	isDoneAllActivities : bool = BooleanProperty(False)
	
	command : callable = ObjectProperty(None)
	
	sound : Sound = ObjectProperty(None)
	
	lyrics_text = data.miss_miss_lyrics
	lyrics_time = data.miss_miss_lyrics_delay
	
	def on_kv_post(self , *args):
		self.sound = SoundLoader.load(os.path.join(os.path.dirname(__file__), 'Music', 'miss_miss_cutted.mp3'))
	
	def displayMusic(self , *_):
		
		delay = self.lyrics_time / len(self.lyrics_text)
		
		def mainEvent(_):
			text = self.lyrics_text[1]
			
			if text == "*":
				return
				
			if text == ",":
				self.lyrics = ""
			else:
				self.lyrics = self.lyrics + self.lyrics_text[1]
				
			self.lyrics_text = self.lyrics_text[1:]
			Clock.schedule_once(mainEvent , delay)
			
		Clock.schedule_once(mainEvent , delay)
			
	
	def on_enter(self , *args):
		self.command = lambda : self.parent.changeScreen("timer year")
		
		def doneMusic(*args):
			self.isDoneAllActivities = True
					
		def delayMusic(*args):
			if self.sound:
				self.sound.bind(on_stop = doneMusic)
				Clock.schedule_once(self.displayMusic)
				self.sound.play()
		
		delay = 0.5
				
		Clock.schedule_once(self.displayMusic , delay)
		Clock.schedule_once(delayMusic , delay)
		
		
# ======= Prupose Screen Activities
class PruposeAnswerButton(ButtonBehavior, Image):
	pass

class ShowProposeScreen(Screen):
	hand : Image = ObjectProperty()
	info : Label = ObjectProperty()
	yes_button : PruposeAnswerButton = ObjectProperty()
	no_button : PruposeAnswerButton = ObjectProperty()
	result : Image = ObjectProperty()
	
	isDoneAllActivities : bool = BooleanProperty(False)
	isMoveUp = False
	delay = 0.5
	
	music : Sound = ObjectProperty(None)
	
	location = ( (0.2 , 0.2) , (0.2 , 0.8) , (0.8 , 0.8) , (0.7 , 0.6) )
	
	anim = Animation(opacity = 0, duration = 1 , size_hint =(0,0))
	
	commad : callable = ObjectProperty(None)
	event_clock : Clock = ObjectProperty()
	
	def on_kv_post(self, *args):
		self.music = SoundLoader.load(os.path.join(os.path.dirname(__file__), 'Music', 'labyu_too.mp3'))
	
	def actionIfYes(self):
		self.yes_button.disabled = True
		self.no_button.disabled = True
		
		self.anim.start(self.yes_button)
		self.anim.start(self.no_button)
		self.anim.start(self.info)
		
		def done(*_):
			self.isDoneAllActivities = True
		
		def processing(*_):
			if self.music:
				self.music.play()
			
		anim = Animation(opacity = 1 , size_hint = (0.8 , 0.4), duration = 3 )
		anim.bind(on_complete = done , on_start = processing )
		anim.start(self.result)
		
	def moveIfNo(self):
		past_loc = ( self.no_button.pos_hint["center_x"], self.no_button.pos_hint["center_y"])
		while True:
			new_loc = self.location[random.randint(0 , len(self.location) - 1)]
			
			if new_loc != past_loc:
				break
			
		self.no_button.pos_hint = { "center_x" : new_loc[0] , "center_y" : new_loc[1] }
	
	def animateMovement(self , _):
		if self.isMoveUp:
			self.hand.pos_hint = {  "center_x" : 0.5 , "center_y" : self.hand.pos_hint["center_y"] + 0.01 }
			self.yes_button.pos_hint = {   "center_x" : 0.39,  "center_y" : self.yes_button.pos_hint["center_y"] + 0.01 }
			self.isMoveUp = False
		else:
			self.hand.pos_hint = {  "center_x" : 0.5 , "center_y" : self.hand.pos_hint["center_y"] - 0.01 }
			self.yes_button.pos_hint = {   "center_x" : 0.39,  "center_y" : self.yes_button.pos_hint["center_y"] - 0.01 }
			self.isMoveUp = True
		
		self.event_clock = Clock.schedule_once(self.animateMovement , self.delay)
	
	def on_enter(self , *args):
		self.event_clock = Clock.schedule_once(self.animateMovement , self.delay)
		self.command = lambda : self.parent.changeScreen("flowering picture")
		
	def on_leave(self , *args):
		Clock.unschedule(self.event_clock)
	

# ======= Pop Up Image Screen Activities
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
	
	isDoneAllActivities : bool = BooleanProperty(False)
	
	sound : Sound = ObjectProperty(None)
	
	command : callable = ObjectProperty(None)
	
	event_clock : Clock = ObjectProperty()
	flowering_clock : Clock = ObjectProperty()
	
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
			selected_image.my_image.source = os.path.join(os.path.dirname(__file__), 'Pictures', image)
		anim.start(selected_image)
	
	def animatePopUpImages(self , interval : float):
		what_to_open = random.randint(1 , 3)
		what_to_close = random.randint(1 , 3)
		what_image = random.randint(0, len(self.images)-1)
		
		if not self.checkIfOpacity(what_to_open):
			self.selectionOfImages(self.open_animation , what_to_open , self.images[what_image])	
		if what_to_close == what_to_open:
			self.event_clock =  Clock.schedule_once(self.animatePopUpImages, self.pop_up_delay)
			return 
		self.selectionOfImages(self.close_animation, what_to_close, None)
		self.event_clock = Clock.schedule_once(self.animatePopUpImages , self.pop_up_delay)
		
	def animateMovingFlower(self , interval : float):
		self.f1.increment()
		self.f1.decrement()
		self.f2.increment()
		self.f2.decrement()	
		self.f3.increment()
		self.f3.decrement()
		self.f4.increment()
		self.f4.decrement()
		
		self.flowering_clock = Clock.schedule_once(self.animateMovingFlower , self.rotation_delay)
	
	def on_enter(self , *args):
		self.f1.currentAngle = 180
		self.f3.currentAngle = 180
		
		def delayMusic(*args):
			if self.sound:
				self.sound.play()
				def doneMusic(*args):
					self.isDoneAllActivities = True
				
				self.sound.bind(on_stop = doneMusic)
		
		Clock.schedule_once(delayMusic , self.pop_up_delay)
		
		self.flowering_clock = Clock.schedule_once(self.animateMovingFlower , self.rotation_delay)
		self.event_clock = Clock.schedule_once(self.animatePopUpImages, self.pop_up_delay)
		
		self.command = lambda : self.parent.changeScreen("propose")
	
	def on_kv_post(self , *args):
		path = os.path.join(os.path.dirname(__file__), 'Music', 'Bruno_Mar_Music.mp3')
		if os.path.exists(path):
			self.sound = SoundLoader.load(path)
		else:
			print("Does not exist")
	
	def on_leave(self , *args):
		Clock.unschedule(self.flowering_clock)
		Clock.unschedule(self.event_clock)
	
# ======= Timer Year Screen Activities
class ShowTimerYearScreen(Screen):
	numer_3 : Label = ObjectProperty(None)
	numer_4 : Label = ObjectProperty(None)
	with_you : Label = ObjectProperty(None)
	labyu : Label = ObjectProperty(None)
	
	duration : int = NumericProperty(1.5)
	
	sound : Sound = ObjectProperty(None)
	
	def withYouAnimation(self , interval : int):
		if self.numer_4.opacity >= 0.65 :
			anim = Animation( pos_hint = {"top":0.85} , duration = 1 )
			anim.start(self.with_you)
			anim = Animation(opacity= 1 , duration = 1.5 )
			anim.bind(on_start = self.activity)
			anim.start(self.labyu)
			return 
		Clock.schedule_once(self.withYouAnimation , 1/30)
	
	def activity(self , *args):
		if self.sound:
			self.sound.play()
			
	def on_kv_post(self , *args):
		self.sound = SoundLoader.load(os.path.join(os.path.dirname(__file__), 'Music', 'Crowd_Cheering.mp3'))
				
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

# ======= I Love You Screen Activities
class  ILoveYouExitButton(MDBoxLayout):
	command : callable = ObjectProperty()
	isOkeyToNext : bool = BooleanProperty(False)

class ILoveYouBox(MDBoxLayout):
	pass

class ShowILoveYouScreen(Screen):
	iloveyoubox : ILoveYouBox = ObjectProperty(None)
	exit_button : ILoveYouExitButton = ObjectProperty(None)
	
	maximum_height = data.maximum_height
	
	duration : float = NumericProperty(1.0)
	
	list_of_heights = data.list_of_heights
	
	sound : Sound = ObjectProperty(None)
	
	
	def checkIsDoneAnimating(self , interval : int) :
		if self.iloveyoubox.size_hint_y == self.maximum_height:
			anim = Animation(opacity = 1 , duration = 4)
			anim.start(self.ids["header"])
			anim.start(self.ids["footer"])
			return 
		Clock.schedule_once(self.checkIsDoneAnimating, 1 /30)
	
	def checkIsDoneToNextPage(self, interval : float):
		if self.ids["header"].opacity and self.ids["footer"].opacity:
			anim = Animation(size_hint_y= 0 , duration= 3)
			anim.start(self.ids["cover"])
			
			def animation(*args):
				self.exit_button.isOkeyToNext = True
			
			anim.bind(on_complete = animation)
			
			return 
		Clock.schedule_once(self.checkIsDoneToNextPage, 1/30)
	
	def on_kv_post(self , *args):
		self.sound = SoundLoader.load(os.path.join(os.path.dirname(__file__), 'Music', 'heart_beat_love.mp3'))
	
	def on_enter(self , *args):
		animation : Animation = None
		self.exit_button.command = lambda : self.parent.changeScreen("popup image")
		
		def activity(*args):
			if self.sound:
				self.sound.play()	
				
		for hint_y , duration in self.list_of_heights:
			if animation:
				animation = animation + Animation(size_hint_y = hint_y , duration=duration )
			else:
				animation = Animation(size_hint_y = hint_y , duration=duration)
		animation.bind( on_start = activity)
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
	
	duration : float = NumericProperty(1)
	text_duration : int = 3 # 60
	
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
		Clock.schedule_once(self.animateText , math.floor(interval))
	
	def animate(self):
		self.isOpen = True
		Animation(size_hint_y = self.maximum_height, duration = self.duration).start(self.envelope_box)
		
		speed = self.text_duration  / len(self.content)
		Clock.schedule_once(self.animateText, speed)
	
	def on_leave(self, *args):
		Animation(opacity = 0 ).start(self)

# LOADING PAGE
class LoadingPage(Screen):
	
	main_event : Clock = ObjectProperty(None)
	loading_num : int = NumericProperty(0)
	loading_cunsor : Widget = ObjectProperty()
	
	def on_enter(self , *args):
		Clock.schedule_once(self.parent.loadAllScreen, 1)
		
	def checkIfDoneLoading(self ):
		self.loading_num += 1
		
		if self.loading_num == 6:
			self.loading_num += 1
			Clock.schedule_once(self.parent.gotoFirstScreen, 1 )
		
		if self.loading_num ==1:
			self.loading_cunsor.size_hint_x = 0.20
		elif self.loading_num ==2:
			self.loading_cunsor.size_hint_x = 0.40
		elif self.loading_num ==3:
			self.loading_cunsor.size_hint_x = 0.60
		elif self.loading_num ==4:
			self.loading_cunsor.size_hint_x = 0.80
		elif self.loading_num ==5:
			self.loading_cunsor.size_hint_x = 1
		else:
			pass
		
	
	
class CartonnyButton(ButtonBehavior , Image):
	pass
	
class MainWindow(ScreenManager):
	
	list_of_screens : dict = DictProperty({})
	
	def changeScreen(self, name : str):
		past_screen = self.current_screen
		self.switch_to(self.list_of_screens[name])
		self.remove_widget(past_screen)
		
	def on_kv_post(self , *args):
		self.list_of_screens["loading"] = LoadingPage(name="loading")
		self.switch_to(self.list_of_screens["loading"])
	
	def gotoFirstScreen(self, *args):
		self.changeScreen("envelope")
		
	def loadAllScreen(self , *args):
		self.list_of_screens["envelope"] = ShowEnvelopeScreen(name = "envelope")
		self.current_screen.checkIfDoneLoading()
		self.list_of_screens["i love you"] = ShowILoveYouScreen(name = "i love you")
		self.current_screen.checkIfDoneLoading()
		self.list_of_screens["timer year"] = ShowTimerYearScreen(name = "timer year")
		self.current_screen.checkIfDoneLoading()
		self.list_of_screens["popup image"] = ShowPopUpImageScreen(name = "popup image")
		self.current_screen.checkIfDoneLoading()
		self.list_of_screens["propose"] = ShowProposeScreen(name = "propose")
		self.current_screen.checkIfDoneLoading()
		self.list_of_screens["flowering picture"] = ShowFloweringPictureScreen(name="flowering picture")
		self.current_screen.checkIfDoneLoading()
		

class GiftApp(MDApp):
	
	def build(self):
		return Builder.load_file("main_design.kv")
		

LabelBase.register(name = "title_font", fn_regular="fonts/Love Castle Demo.ttf")
LabelBase.register(name="content_font", fn_regular="fonts/RomanticLove-Regular.ttf")
LabelBase.register(name="reg_font", fn_regular="fonts/AbrilFatface-Regular.ttf")

GiftApp().run()
