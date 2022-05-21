'''
Code of How to create Stopwatch
'''
	
# Program to Show how to create a switch
# import kivy module
import kivy
		
# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App
	
# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')

# The Builder is responsible for creating
# a Parser for parsing a kv file
from kivy.lang import Builder

# The Properties classes are used
# when you create an EventDispatcher.
from kivy.properties import NumericProperty

# BoxLayout arranges children in a vertical or horizontal box.
# or help to put the children at the desired location.
from kivy.uix.boxlayout import BoxLayout

# he Clock object allows you to
# schedule a function call in the future
from kivy.clock import Clock


# Create the .kv file and load it by using Builder
Builder.load_string('''

<MainWidget>:

	# Assigning the alignment to buttons
	BoxLayout:
		orientation: 'vertical'

		# Create Button
		
		Button:
			text: 'start'
			on_press: root.start()
			
		Button:
			text: 'stop'
			on_press: root.stop()
			
		Button:
			text: 'Reset'
			on_press: root.number = 0

	# Create the Label
	Label:
		text: str(round(root.number))
		text_size: self.size
		halign: 'center'
		valign: 'middle'
''')

# Create the Layout class
class MainWidget(BoxLayout):
	
	number = NumericProperty()
	
	def __init__(self, **kwargs):

		# The super() builtin
		# returns a proxy object that
		# allows you to refer parent class by 'super'.
		super(MainWidget, self).__init__(**kwargs)

		# Create the clock and increment the time by .1 ie 1 second.
		Clock.schedule_interval(self.increment_time, .1)

		self.increment_time(0)

	# To increase the time / count
	def increment_time(self, interval):
		self.number += .1

	# To start the count
	def start(self):
		
		Clock.unschedule(self.increment_time)
		Clock.schedule_interval(self.increment_time, .1)

	# To stop the count / time
	def stop(self):
		Clock.unschedule(self.increment_time)

# Create the App class
class TimeApp(App):
	def build(self):
		return MainWidget()

# Run the App
TimeApp().run()
