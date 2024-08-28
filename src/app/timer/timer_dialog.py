
""" TimerDialog class
Allows you to create and modify a timer.
"""

# Imports :
from datetime import timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QSpinBox, \
	QDialogButtonBox

from app.timer.config import MAX_CHAR_NAME, MAX_CHAR_MESSAGE, MAX_RINGS, MAX_INTERVAL
from app.timer.timer import Timer


class TimerDialog(QDialog):
	""" TimerDialog class

	Allows you to create and modify a machine.
	"""
	def __init__(self, parent=None, timer=None):
		super().__init__(parent)
		
		self.resize(300, 300)
		
		self.timer = timer
		self.parent = parent
		
		# Set the window title with the mode that
		# will be checked later to see if we need to create a new one or modify the supplied timer.
		self.window_title = "Creation"
		self.setWindowTitle(self.window_title)
		
		# Creating interface elements
		# self.create_variables()
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
	##
	
	#
	def create_variables(self):
		""" Variable definition
		"""
		pass
	##
	
	#
	def setup_ui(self):
		""" Interface configuration
		"""
		
		self.hlayout = QHBoxLayout()
		self.setLayout(self.hlayout)
		
		# Main layout
		self.vlayout = QVBoxLayout()
		self.hlayout.addLayout(self.vlayout)
		
		# Line edit character counter
		self.lb_count_char_name = QLabel(f"{MAX_CHAR_NAME} remaining characters")
		self.vlayout.addWidget(self.lb_count_char_name)
		
		# Line edit
		self.le_name_timer = QLineEdit()
		self.le_name_timer.setPlaceholderText("Timer name")
		self.vlayout.addWidget(self.le_name_timer)
		
		# Text edit character counter
		self.lb_count_char_message = QLabel(f"{MAX_CHAR_MESSAGE} remaining characters.")
		self.vlayout.addWidget(self.lb_count_char_message)
		
		# Text edit
		self.te_content_timer = QTextEdit()
		placeholder_text = "Notification message"
		placeholder_text += "\nLeave empty to avoid triggering notifications"
		self.te_content_timer.setPlaceholderText(placeholder_text)
		self.vlayout.addWidget(self.te_content_timer)
		
		self.lb_times = QLabel("Timer duration :")
		self.vlayout.addWidget(self.lb_times)
		
		#
		# ---   Layout SpinBox --- #
		self.hlayout_spn = QHBoxLayout()
		self.vlayout.addLayout(self.hlayout_spn)
		
		# Hours
		self.spn_hours = QSpinBox()
		self.spn_hours.setSuffix(" hours")
		self.spn_hours.setMaximum(24)
		self.hlayout_spn.addWidget(self.spn_hours)
		
		# Minutes
		self.spn_minutes = QSpinBox()
		self.spn_minutes.setSuffix(" minutes")
		self.spn_minutes.setMaximum(60)
		self.hlayout_spn.addWidget(self.spn_minutes)
		
		# Seconds
		self.spn_seconds = QSpinBox()
		self.spn_seconds.setSuffix(" seconds")
		self.spn_seconds.setMaximum(60)
		self.spn_seconds.setSingleStep(5)
		self.hlayout_spn.addWidget(self.spn_seconds)
		
		# Number of rings
		self.lb_number_rings = QLabel("Additional ringtones :")
		self.vlayout.addWidget(self.lb_number_rings)
		
		self.hlayout_number_rings = QHBoxLayout()
		self.vlayout.addLayout(self.hlayout_number_rings)
		
		# Number of additional rings
		self.spn_rings = QSpinBox()
		self.spn_rings.setSuffix(f" /{MAX_RINGS}")
		self.spn_rings.setMaximum(MAX_RINGS)
		self.hlayout_number_rings.addWidget(self.spn_rings)
		
		self.lb_times_rings = QLabel(" all ")
		self.hlayout_number_rings.addWidget(self.lb_times_rings)
		
		# Time between rings
		self.spn_interval = QSpinBox()
		self.spn_interval.setSuffix(f"s /{MAX_INTERVAL}")
		self.spn_interval.setMaximum(MAX_INTERVAL)
		self.spn_interval.setSingleStep(15)
		self.hlayout_number_rings.addWidget(self.spn_interval)
		
		# Validation button box
		self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
		self.vlayout.addWidget(self.button_box)
	##
	
	#
	def set_style(self):
		""" Style modification
		"""
		
		# Align labels on the right
		self.lb_count_char_name.setAlignment(Qt.AlignRight)
		self.lb_count_char_message.setAlignment(Qt.AlignRight)
		
		self.setStyleSheet(
			"""
				* {
					font-size: 13px;
				}
				
				QLineEdit {
					border-radius: 5px;
				}
				
				QTextEdit {
					border-radius: 5px;
					border: 1px solid black;
					min-height: 65px;
				}
				
				QDialogButtonBox > QPushButton {
					margin-right: 10px;
					margin-top: 8px;
					margin-bottom: 2px;
				}
				""")
	##
	
	#
	def setup_connections(self):
		""" Creating connections between widgets
		"""
		
		self.le_name_timer.textChanged.connect(lambda: self.count_char("name"))
		
		self.te_content_timer.textChanged.connect(lambda: self.count_char("message"))
		
		self.spn_seconds.valueChanged.connect(self.check_spinbox_seconds)
		
		self.spn_seconds.valueChanged.connect(lambda: self.check_spinbox("seconds"))
		
		self.spn_minutes.valueChanged.connect(lambda: self.check_spinbox("minutes"))
		
		self.spn_hours.valueChanged.connect(lambda: self.check_spinbox("hours"))
		
		self.spn_rings.valueChanged.connect(self.check_number_rings)
		
		self.spn_interval.valueChanged.connect(lambda: self.correct_value(self.spn_interval))
		self.spn_interval.valueChanged.connect(self.check_remaining)
		
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)
		pass
	##
	
	#
	def set_default_values(self):
		""" Setting default values
		"""
		
		# If a timer is supplied
		if self.timer:
			
			# Change the window mode to
			# the supplied timer must be modified, not a new one created
			self.setWindowTitle("Modification")
			
			# Adds timer information to the fields
			self.le_name_timer.setText(self.timer.title)
			self.te_content_timer.setPlainText(self.timer.message)
			self.spn_hours.setValue(self.timer.hours)
			self.spn_minutes.setValue(self.timer.minutes)
			self.spn_seconds.setValue(self.timer.seconds)
			self.spn_rings.setValue(self.timer.number_rings)
			self.spn_interval.setValue(self.timer.interval)
	##
	
	#
	def count_char(self, field: str):
		"""
		Calculates the number of characters remaining in the fields
			> When modified.

		- Checks if the number of characters in the fields is correct.
		- Text and color change according to validity
			fields using a complementary function.

		Args:
			field (str): Text field to be modified.
		"""
		
		chars_left = 0 # Number of characters remaining
		max_char = 0 # Maximum number of characters
		
		# Retrieves content from the requested field
		# and set the maximum number of characters
		if field == "message":
			# Text edit content
			content = self.te_content_timer.toPlainText()
			max_char = MAX_CHAR_MESSAGE
			chars_left = max_char - len(content)
			
			# Increase max to allow an empty message to be notified
			# This will ensure that the button and color are displayed correctly all at once.
			if chars_left == max_char:
				max_char += 1
		
		elif field == "name":
			# Line edit content
			content = self.le_name_timer.text()
			max_char = MAX_CHAR_NAME
			chars_left = max_char - len(content)
		
		# Replacement text
		text = str(chars_left) + " remaining characters."
		
		# Activates the button if the number of characters is correct.
		if -1 < chars_left < max_char:
			self.modify_label_chars(True, field, text)
		else:
			self.modify_label_chars(False, field, text)
	
	##
	
	#
	def modify_label_chars(self, active: bool, field: str, text: str = ""):
		"""
		Allows you to modify information labels and activate the validation button if fields are valid.
			> When a text field is modified.

		- Modifies label text and color according to the validity of the associated field.
		- Activates form validation button if fields are valid.

		Args:
			- active (bool): Whether the field is valid or not.
			- field (str): Text field to be modified.
			- text (str): Text to be displayed in the label, contains the number of remaining characters.
		"""
		
		# Notification message field
		if field == "message":
			
			# Modifies the label text with the remaining number of characters
			self.lb_count_char_message.setText(text)
			
			# If the field is valid,
			if active:
				# activates the button and changes the text color to green
				self.activate_btn()
				self.lb_count_char_message.setStyleSheet("QLabel {color: #00a151;}")
			else:
				# Otherwise, disable the button and change the text color to red
				self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
				self.lb_count_char_message.setStyleSheet("QLabel {color: #c5130d;}")
		
		# Timer name field
		# Logic identical to that of the message field
		elif field == "name":
			self.lb_count_char_name.setText(text)
			if active:
				self.activate_btn()
				self.lb_count_char_name.setStyleSheet("QLabel {color: #00a151;}")
			else:
				self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
				self.lb_count_char_name.setStyleSheet("QLabel {color: #c5130d;}")
	
	def check_spinbox_seconds(self):
		""" Checks the seconds spinbox value and modifies it if incorrect
			> When the seconds spinbox is modified.
		
			- Force the last digit to be a multiple of 5.
		"""
		
		# Retrieves spinbox value
		value = str(self.spn_seconds.value())
		
		# Separates the numbers from the value
		start_value = value[1] if len(value) == 2 else ""
		end_value = value[-1]
		
		if end_value not in "05 ":
			
			# Changes the last digit to a multiple of 5.
			if end_value in "1289":
				end_value = "0"
			else:
				end_value = "5"
			
			# Spin box modification
			self.spn_seconds.setValue(int(start_value + end_value))
	
	@staticmethod
	def correct_value(obj):
		""" Corrects spinbox value to a multiple of 15
		"""
		value = obj.value()
		step = obj.singleStep()
		corrected_value = (value // step) * step
		if value % step != 0:
			obj.setValue(corrected_value)
	
	#
	def check_remaining(self):
		""" Checks the spinbox value of the time between rings
				> When modified
		"""
		# Checking the number of rings
		# This prevents increasing the time between rings if the number of rings is zero.
		self.check_number_rings()
		
		# If the time between rings is zero and the number of rings is non-zero
		if self.spn_interval.value() == 0 and self.spn_rings.value() != 0:
			# We force the time between rings to be 15 seconds.
			# prevents the remaining time from reaching zero if the number of rings is non-zero
			self.spn_interval.setValue(15)
	##
	
	#
	def check_number_rings(self):
		"""
			Checks the number of rings spin box
				> When it is modified or the time between rings is changed
		"""
		
		# Checks if the number of rings is zero
		if self.spn_rings.value() == 0:
			# Force spin box time between rings to zero
			self.spn_interval.setValue(0)
		else:
			# If the number of rings is not zero, the time between rings cannot be zero.
			if self.spn_interval.value() == 0:
				self.spn_interval.setValue(15)
	##
	
	#
	def check_spinbox(self, spinbox: str):
		"""
		Main check on spinboxes to activate the form validation button.
			> When a spin box is modified.

		- Reset to zero if they reach their maximum and increase the other spinboxes.
		- Activate button if fields are valid.

		Args:
			spinbox (str): Spinbox to be checked.
		"""
		
		# Check the spinbox in question
		if spinbox == "seconds":
			# Retrieves spin box value
			value = self.spn_seconds.value()
			
			# Checks if the value is greater than the authorized value
			if value == 60:
				# Retrieves the value of the neighboring spin box and increments it.
				minutes = self.spn_minutes.value()
				minutes += 1
				
				# Resets spin box value to zero.
				self.spn_seconds.setValue(0)
				self.spn_minutes.setValue(minutes)
		
		# Same for the other spinboxes
		elif spinbox == "minutes":
			value = self.spn_minutes.value()
			if value == 60:
				hours = self.spn_hours.value()
				hours += 1
				self.spn_hours.setValue(hours)
				self.spn_minutes.setValue(0)
		
		# Without increasing the other spinboxes for this one
		elif spinbox == "hours":
			value = self.spn_hours.value()
			if value == 24:
				self.spn_hours.setValue(0)
		
		# Activate form validation button
		self.activate_btn()
	
	def activate_btn(self):
		""" Performs checks and activates button only if all checks are passed
		"""
		
		# Finds out if a check has failed, set to true to start,
		# if it becomes false before the end of the checks, the button will not be activated.
		check = True
		
		# Check line edit
		text = self.le_name_timer.text()
		if not 0 < len(text) <= MAX_CHAR_NAME:
			check = False
		
		# Check text edit
		text = self.te_content_timer.toPlainText()
		if not len(text) < MAX_CHAR_MESSAGE + 1:
			check = False
			
		# Check spinbox
		seconds = self.spn_seconds.value()
		minutes = self.spn_minutes.value()
		hours = self.spn_hours.value()
		
		# Checks whether at least one spinbox has a
		if not seconds and not minutes and not hours:
			check = False
		
		# If no verification failed
		if check:
			# activates the form validation button and returns True.
			self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
		else:
			self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
	
	@property
	def spn_duration(self):
		""" Retrieves spin box values and builds a duration in seconds
		"""
		seconds = self.spn_seconds.value()
		minutes = self.spn_minutes.value()
		hours = self.spn_hours.value()
		return timedelta(hours=hours, minutes=minutes, seconds=seconds).seconds
	##
	
	#
	def accept(self):
		""" Creates a timer with the form information and sends it.
			> when the button is pressed and the form is checked.
		"""
		
		# Retrieving information from the form
		title = self.le_name_timer.text()
		message = self.te_content_timer.toPlainText()
		duration = self.spn_duration
		number_rings = self.spn_rings.value()
		interval = self.spn_interval.value()
		
		# If the window is in creation mode
		if self.windowTitle() == "Creation":
			# We create a timer with the recovered information
			self.timer = Timer(title, message, duration, number_rings=number_rings, interval=interval)
		
		# If the window is in edit mode
		else:
			# Modify the supplied timer
			self.timer.title = title
			self.timer.message = message
			self.timer.timer = self.spn_duration
			self.timer.number_rings = number_rings
			self.timer.check_number_rings()
			self.timer.interval = interval
			self.timer.check_times_between_rings()
			
		# Accept the form and close it
		super().accept()
	
	def reject(self):
		""" Close the form without doing anything
		"""
		super().reject()
	
	def get_timer(self):
		""" Function to retrieve the timer after closing the form
		"""
		return self.timer
	##
	
	#
	def keyPressEvent(self, event):
		""" Press the enter key to submit the form
		"""
		if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
			# Checks if the button is enabled before submitting the form
			if self.button_box.button(QDialogButtonBox.Ok).isEnabled():
				self.accept()
		else:
			super().keyPressEvent(event)
	
