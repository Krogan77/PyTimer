
""" TimerWidget class
File containing the TimerWidget class for displaying a timer in the list.
"""


from PySide6.QtCore import QSize, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

font_weight = "font-weight: 750;"

icon_play = "src/app/timer/icons/icon_play"
icon_break = "src/app/timer/icons/icon_break"
icon_reset = "src/app/timer/icons/icon_reset"
icon_modify = "src/app/timer/icons/icon_modify"


class TimerWidget(QWidget):
	""" TimerWidget class
	Displays a timer.
	"""
	
	# Signal to send the timer to be modified
	submit_timer = Signal(object, object)
	
	def __init__(self, timer=None, parent=None, main_window=None):
		super().__init__()
		self.timer = timer
		self.parent = parent
		self.main_window = main_window
		
		# Creating interface elements
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
		
	##
		
	def setup_ui(self):
		""" Interface configuration
		"""
		
		self.hlayout = QHBoxLayout()
		self.setLayout(self.hlayout)
		
		# Start button
		self.btn_play = QPushButton()
		self.btn_play.setIcon(QIcon(icon_play))
		self.hlayout.addWidget(self.btn_play)
		
		self.vlayout = QVBoxLayout()
		self.hlayout.addLayout(self.vlayout)
		
		# Timer info
		self.lb_title = QLabel(self.timer.title)
		self.vlayout.addWidget(self.lb_title)
		
		self.lb_duration = QLabel(f"⌚ {self.timer.duration}")
		self.vlayout.addWidget(self.lb_duration)
		
		self.vlayout_time = QVBoxLayout()
		self.hlayout.addLayout(self.vlayout_time)
		
		self.lb_timeleft = QLabel(f"⌛ {str(self.timer.timeleft)}")
		self.vlayout_time.addWidget(self.lb_timeleft)
		
		self.lb_end_date = QLabel(f"🔔 {str(self.timer.end_date)}")
		self.vlayout_time.addWidget(self.lb_end_date)
		
		# Reset and modify buttons
		self.btn_reset = QPushButton()
		self.btn_reset.setIcon(QIcon(icon_reset))
		self.hlayout.addWidget(self.btn_reset)
		
		self.btn_modify = QPushButton()
		self.btn_modify.setIcon(QIcon(icon_modify))
		self.hlayout.addWidget(self.btn_modify)
	
	#
	def set_style(self):
		""" Style modification
		"""
		
		self.setStyleSheet("""
			* {
				font-weight: 600;
				padding: 0px;
				margin: 0px;
			}
			
			QLabel {
				text-align: center;
				font-size: 13px;
				margin-left: 8px;
			}
			
			QPushButton {
				border: none;
				border-radius: 10px;
				min-width: 0px;
				min-height: 0px;
				padding: 10px;
				margin-bottom: 3px;
				margin-right: 5px;
				margin-left: 3px;
			}
			""")
		
		self.lb_title.setStyleSheet(f"QLabel {{{font_weight}}}")
		self.lb_timeleft.setStyleSheet(f"QLabel {{{font_weight}}}")
		
		# Change button size
		icon_size = 24
		button_size = 38
		
		self.btn_play.setIconSize(QSize(icon_size, icon_size))
		self.btn_play.setFixedSize(QSize(button_size, button_size))
		
		self.btn_reset.setIconSize(QSize(icon_size, icon_size))
		self.btn_reset.setFixedSize(QSize(button_size, button_size))
		
		self.btn_modify.setIconSize(QSize(icon_size, icon_size))
		self.btn_modify.setFixedSize(QSize(button_size, button_size))
	
	#
	def setup_connections(self):
		""" Creating connections between widgets
		"""
		
		self.btn_play.clicked.connect(self.start_timer)
		
		self.btn_reset.clicked.connect(self.reset_timer)
		
		self.btn_modify.clicked.connect(self.modify_timer)
	##
	
	#
	def set_default_values(self):
		""" Setting default values
		"""
		self.check_color = False
		pass
	##
	
	#
	@Slot()
	def modify_timer(self):
		""" Sends signal from change button
		"""
		self.submit_timer.emit(self.timer, self)
	##
	
	#
	def start_timer(self):
		""" Starts, stops or resets the timer
		
		- If the timer is inactive, it will be started.
		
		- If in progress, it will be stopped and can be restarted.
		
		- If it is running and finished, it will be stopped and reset.
		"""
		
		if self.timer.remaining:
			if self.timer.running:
				# If the timer is running but has passed its end date, it is stopped.
				self.timer.stop_timer()
				self.btn_play.setIcon(QIcon("lib/icons/icon_reset"))
				return
			
			# If the timer has ended and already stopped, it is reset.
			self.reset_timer()
			return
		
		# If the timer is inactive or paused, start it.
		self.timer.start_timer()
		
		# End date display
		self.lb_end_date.setText(f"🔔{str(self.timer.end_date)}")
		
		# Change button style and remaining time
		self.set_style_btn_start()
		self.lb_timeleft.setStyleSheet(f"QLabel {{color: green;{font_weight}}}")
	##
	
	#
	def update_timeleft(self):
		""" Update remaining time display if timer is running
		"""
		
		# Change remaining time
		if self.timer.running:
			self.lb_timeleft.setText(f"⌛ {str(self.timer.set_timeleft(_format=True))}")
			
			# Checks if the end date has been reached and changes the text color
			if self.timer.remaining and not self.check_color:
				self.lb_timeleft.setStyleSheet(f"QLabel {{color: red;{font_weight}}}")
				# Prevents this check from being repeated each time the display is updated
				self.check_color = True
	##
	
	#
	def reset_timer(self, check_duration=False):
		""" Timer reset
		
		- If the default time has been changed, the timer is reset.
		- If it has not been modified, we leave the timer running.
		"""
		
		# Checks whether the default duration has been modified
		if check_duration:
			if self.lb_duration.text() == "⌚ " + self.timer.duration:
				self.lb_title.setText(self.timer.title)
				return
		
		# Reset timer
		self.timer.reset()
		
		# Display update
		self.lb_title.setText(self.timer.title) # title
		self.lb_duration.setText(f"⌚ {self.timer.duration}") # default duration
		self.lb_timeleft.setText(f"⌛ {str(self.timer.timeleft)}")  # remaining time with millisec
		self.lb_end_date.setText(f"🔔 {str(self.timer.end_date)}")  # End date
		
		# Modifying the style of the play button and remaining time
		self.btn_play.setIcon(QIcon(icon_play))
		style = self.main_window.config["style"]
		color = "white" if style in ["Combinear", "Diffnes", "Takezo"] else "black"
		self.lb_timeleft.setStyleSheet(f"QLabel {{color: {color};{font_weight}}}")
		self.check_color = False
	##
	
	#
	def set_style_btn_start(self):
		""" Modifying the style of the start button
		"""
		
		# If the timer is running, icon stop
		if self.timer.running:
			self.btn_play.setIcon(QIcon(icon_break))
			
		# If the timer is finished or paused, icon start
		else:
			self.btn_play.setIcon(QIcon(icon_play))
