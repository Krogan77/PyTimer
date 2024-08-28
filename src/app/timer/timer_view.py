
"""
    $ -- TimerView -- $
File containing timer display view
"""

# Imports

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout, \
	QAbstractItemView

from app.timer.timer_dialog import TimerDialog
from app.timer.timer_widget import TimerWidget
from app.timer.utils import load_timers, save_timers


class TimerView(QWidget):
	""" Timer view management
	"""
	def __init__(self, main_window=None):
		super().__init__()
		self.main_window = main_window
		
		# Creating interface elements
		# self.set_variables()
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
	##
	
	#
	def set_variables(self):
		""" Defining view variables
		"""
		pass
	##
	
	#
	def setup_ui(self):
		""" Creating interface elements
		"""
		
		self.vlayout = QVBoxLayout()
		self.setLayout(self.vlayout)
		
		self.hlayout = QHBoxLayout()
		self.vlayout.addLayout(self.hlayout)
		
		# Timer creation button
		self.btn_new_timer = QPushButton("New")
		self.btn_new_timer.setFixedWidth(150)
		self.hlayout.addWidget(self.btn_new_timer)
		
		# Delete timer button
		self.btn_delete_timer = QPushButton("Delete")
		self.btn_delete_timer.setEnabled(False)
		self.btn_delete_timer.setFixedWidth(150)
		self.hlayout.addWidget(self.btn_delete_timer)
		
		# Timer list
		self.lst_timer = QListWidget()
		self.lst_timer.setMinimumWidth(400)
		self.vlayout.addWidget(self.lst_timer)
		
		self.lst_timer.setDragDropMode(QAbstractItemView.InternalMove)
		self.lst_timer.setAcceptDrops(True)
		self.lst_timer.setDragEnabled(True)
		self.lst_timer.setDropIndicatorShown(True)
	##
	
	#
	def set_style(self):
		""" Modifying element styles
		"""
		
		self.setStyleSheet("""
			
			QTextEdit {
				margin: 5px;
				padding: 5px;
			}
			
			QLineEdit {
				margin: 5px;
				padding: 3px;
			}
			
			QSpinBox {
				margin-top: 3px;
				margin-bottom: 3px;
				padding: 3px;
			}
			
			QLabel {
				margin-top: 5px;
			}
			
			QListWidget {
				border-radius: 10px;
			}
			
			QListWidget::item {
				border-radius: 20px;
				margin: 3px;
			}
			""")
	
	#
	def setup_connections(self):
		""" Creating connections between widgets
		"""
		self.btn_new_timer.clicked.connect(self.create_timer)
		
		# Connect timer selection in the list to a button activation method
		self.lst_timer.currentItemChanged.connect(lambda: self.btn_delete_timer.setEnabled(True))
		self.lst_timer.itemDoubleClicked.connect(self.get_timer)
		
		# Connecting the delete button
		self.btn_delete_timer.clicked.connect(self.delete_timer)
		pass
	##
	
	#
	def set_default_values(self):
		""" Setting default values
		"""
		
		# Application QTimer used to refresh active timers
		# and trigger timer notifications
		self.timer_refresh = QTimer()
		self.timer_refresh.timeout.connect(self.check_timer)
		self.timer_refresh.start(20) # Checks every 20 ms
		
		# Adding existing timers to the list
		for timer in load_timers():
			self.add_timer(timer)
	##
	
	#
	def add_timer(self, timer):
		"""
		Create a new timer!
			> Triggered by form signal
		
		- Retrieves the timer provided by the form.
		- Creates the timer widget for insertion in the list.
		- Connects the change button signal to the corresponding method.
		- Places the timer in its widget and adds it to the list.
		
		:param timer: Timer
		"""
		
		# Widget creation
		self.item = QListWidgetItem()
		self.timer_widget = TimerWidget(parent=self, timer=timer, main_window=self.main_window)
		
		# Modification signal connection
		self.timer_widget.submit_timer.connect(self.create_timer)
		
		# Add widget to list
		self.item.setSizeHint(self.timer_widget.sizeHint())
		self.lst_timer.addItem(self.item)
		self.lst_timer.setItemWidget(self.item, self.timer_widget)
		
	
	def create_timer(self, timer=None, widget=None):
		""" Creating a new timer
			> Triggered by the view creation button
			> and the timer modification button
			
			- If no timer is supplied, the creation form is opened.
			- If a timer is provided by the edit button, open the form
			  providing timer information.
			- Adds or modifies the existing timer in the list if the user has validated the form.
		"""
		
		# Creation mode if no timer supplied
		if not timer:
			
			# Opens the creation window and retrieves the timer if the user has validated.
			dialog = TimerDialog(self)
			if dialog.exec():
				timer = dialog.get_timer()
				
				# Adds the timer to the list widget
				self.add_timer(timer)
		
		# Edit mode
		else:
			
			# Opens the editing window and retrieves the timer if the user has validated it.
			dialog = TimerDialog(self, timer)
			if dialog.exec():
				
				# Modifies the existing timer,
				timer = dialog.get_timer()
				widget.timer = timer
				
				# Reset timer to update values
				widget.reset_timer(check_duration=True)
	
	def check_timer(self):
		""" Update active timers
			> Triggered by refresh QTimer
			
			- Scroll through all the widgets in the list to update the remaining time.
			- All the updating logic is then carried out in the timer widgets and in the timers themselves.
		"""
		
		# Browse widgets to update timers
		for widget in self.lst_timer.findChildren(TimerWidget):
			widget.update_timeleft()
	
	def delete_timer(self):
		"""
		Deleting a timer
			> Triggered by the delete button
		"""
		# Get the index of the selected item
		current_row = self.lst_timer.currentRow()
		
		# If no element is selected, current_row will be -1
		if current_row != -1:
			# Remove and delete element
			timer = self.lst_timer.takeItem(current_row)
		
		# Check if there is a timer left in the list to disable the delete button
		if self.lst_timer.count() == 0:
			self.btn_delete_timer.setEnabled(False)
	##
	
	@property
	def timers(self):
		"""
		Property returning the list of timers
			> Used to save timers when closing the view
			
		- Retrieves timers from the list widget and returns them
		"""
		# Retrieves the number of timers to check that there are any and loop over the list
		count = self.lst_timer.count()
		
		# If no timer, returns an empty list
		if not count:
			return []
		
		# Creating the return list
		timers = []
		
		# Loop over each list item
		for row in range(count):
			
			# Retrieve line item and widget
			item = self.lst_timer.item(row)
			widget_timer = self.lst_timer.itemWidget(item)
			
			# Retrieves widget timer
			if widget_timer and hasattr(widget_timer, 'timer'):
				timer = widget_timer.timer
				timers.append(timer)
		
		# Returns the timer list
		return timers
	##
	
	#
	def get_timer(self, item):
		"""
			Retrieves a timer from the list
				> When double-clicked
		"""
		# Retrieve item widget
		widget_timer = self.lst_timer.itemWidget(item)
		
		# Retrieves widget timer
		if widget_timer and hasattr(widget_timer, 'timer'):
			timer = widget_timer.timer
		
			# Open the modification form
			self.create_timer(timer, widget_timer)
	##
	
	def closeEvent(self, event):
		""" Close view
		"""
		save_timers(self.timers)
		pass
