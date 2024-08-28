
"""
    $ -- Timer -- $
Class representing a timer.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from plyer import notification

from app.timer.utils import new_date
from app.timer.config import MAX_CHAR_NAME, MAX_CHAR_MESSAGE


@dataclass
class Timer:
	
	# User-defined attributes
	
	title: str  # Timer title
	message: str  # Notification message
	
	timer: int  # Default time in seconds
	
	#
	# Other attributes
	
	_timeleft: int | timedelta = 0  # Remaining time in seconds and microseconds
	
	number_rings: int = 0  # Number of rings
	_number_rings: int = 0  # Number of remaining rings
	
	interval: int = 0  # Default time between rings
	_interval: int = 0  # Time currently used between rings
	
	# Timer end date
	_end_date: Optional[datetime] = None
	
	# Date used for the next notification after the timer has passed its end date.
	notif_date: Optional[datetime] = None
	
	# Étimer status
	running: bool = False
	remaining: bool = False
	# Checks whether the timer has ended
	end: bool = False
	
	#
	def __post_init__(self):
		""" Initialization """
		
		# Checks that the title and message are valid.
		self.check_message_lenght()
		
		# Sets default remaining time
		self._timeleft = self.timer
		
		self.check_number_rings()
		self.check_times_between_rings()
	
	##
	
	@property
	def duration(self):
		""" Default duration attribute
		"""
		return format_duration(self.timer)
	##
	
	@property
	def hours(self):
		""" Time attribute in hours
		"""
		return format_duration(self.timer, _format=False)[0]
	
	@property
	def minutes(self):
		""" Time attribute in minutes
		"""
		return format_duration(self.timer, _format=False)[1]
	
	@property
	def seconds(self):
		""" Time attribute in seconds
		"""
		return format_duration(self.timer, _format=False)[2]
	
	@property
	def timeleft(self):
		""" Remaining time attribute
		"""
		return format_duration(self._timeleft)
	
	@property
	def end_date(self):
		""" End date attribute
		"""
		return self._end_date.strftime("%H:%M:%S") if self._end_date else "---"
	##
	
	#
	def __str__(self):
		""" Display object information
		"""
		display = f"Timer(\n\ttitle='{self.title}', \n"
		display += f"\tmessage='{self.message}', \n"
		display += f"\ttimer={self.timer}, \n"
		display += f"\tduration={self.duration}, \n"
		display += f"\ttimeleft={self._timeleft}, \n"
		display += f"\tend_date={self._end_date}, \n"
		display += f"\trunning={self.running}\n)\n"
		
		return display
	
	#
	def check_message_lenght(self):
		""" Checks title and message length
		- Raises an error if an element is incorrect.
		"""
		
		# Title check
		if not 0 < len(self.title) < MAX_CHAR_NAME+1:
			# If it is incorect, we define the error info
			obj = "nom"
			max_char = MAX_CHAR_NAME
		
		# Message verification
		elif not len(self.message) < MAX_CHAR_MESSAGE+1:
			obj = "message"
			max_char = MAX_CHAR_MESSAGE
			
		else:
			# If no error, exit the function.
			return
		
		# If an error has occurred, we remove it with the info
		raise AttributeError(f"The number of characters in {obj} must not exceed {max_char}.")
	##
	
	#
	def check_number_rings(self):
		""" Checks that the number of rings is valid
		"""
		if self.number_rings != self._number_rings:
			self._number_rings = self.number_rings
	##
	
	def check_times_between_rings(self):
		""" Resets the time between rings
		"""
		if self.interval != self._interval:
			self._interval = self.interval
	##
	
	#
	def start_timer(self):
		""" Timer start
		"""
		if self.end:
			return
		
		# Checks that the timer is not already running
		if self.running:
			self.stop_timer()
			return
		
		# Set end date
		self._end_date = new_date(self._timeleft)
		self.notif_date = self._end_date
		
		# Set running attribute to True
		self.running = True
	##
	
	#
	def stop_timer(self, reset: bool = False):
		""" Stop timer
		
		- able to reset the timer.
		
		Args:
			- reset (bool): Resets the timer to its default duration.
		"""
		
		# Checks that the timer is active
		if not self.running:
			return
		
		# Disable timer
		self.running = False
		
		# Resets remaining time if requested
		if reset:
			self.reset()
	##
	
	#
	def set_timeleft(self, _format: bool = False):
		""" Timer update
		
		- Calculating and displaying remaining time
		- Trigger notifications when timer exceeds set dates.
		
		Args:
			- format (bool): Returns the remaining time formatted if True.
		"""
		
		# Ensures that the timer is active, otherwise nothing is done
		if self.running:
			now = datetime.now() # Retrieves the current date
			
			# Calculates remaining time using actual end date for display
			self._timeleft = self._end_date - now
			
			# Calculation of time remaining before next ring
			timeleft_notif = self.notif_date - now
			
			# If the date is exceeded, triggers a notification
			if timeleft_notif.total_seconds() < 0:
				self.remaining = True
				# Calculation of seconds elapsed since end date
				# with formatting for notification display
				seconds = format_duration((now - self._end_date).seconds)
				
				# If there are still additional rings to be triggered
				if self._number_rings:
					
					# Retrieves notification message for local editing
					message = self.message
					
					# If the default number of rings is different from the number of remaining rings
					if self.number_rings != self._number_rings:
						
						# We modify the notification message to display the time elapsed since the end date.
						message += f"\n - {seconds} !"
					
					# Trigger notification
					send_notify(self.title, message)
					
					# Adds extra time for next notification
					self.notif_date += timedelta(seconds=self._interval)
					
					self._number_rings -= 1 # Number of remaining rings -1
					return
				
				# Last ring when number of rings is zero
				if not self.end:
					
					# If it's not the first ring,
					# because the default number is not zero
					if self.number_rings:
						# Change notification message to show elapsed time
						message = self.message + f"\n - {seconds} !"
					else:
						# Otherwise, we keep the default message
						message = self.message
					
					# Trigger notification
					send_notify(self.title, message)
					self.end = True
		
		# In all cases, the remaining time is returned, with formatting if requested.
		return self.timeleft if _format else self._timeleft
	##
	
	#
	def reset(self):
		""" Timer reset
		"""
		
		# Stop timer if active.
		if self.running:
			self.stop_timer()
			
		# Reset attributes
		self._timeleft = self.timer
		self._end_date = None
		self.notif_date = None
		self.remaining = False
		self.end = False
		self.check_number_rings()
		self.check_times_between_rings()
	##
##


#
def format_duration(delta: int | float | timedelta, _format=True) -> str | tuple:
	""" Formats time in hours, minutes and seconds

	:param delta: Duration in seconds
	:param _format: Output format
	:return: Time formatted in hours, minutes and seconds
	"""
	result = "- " if isinstance(delta, timedelta) and delta.total_seconds() < 0 else ""
	
	# Take the absolute value of the duration in seconds
	total_seconds = abs(delta.total_seconds()) if isinstance(delta, timedelta) else abs(delta)
	
	# Calculation of hours, minutes and seconds
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	
	# If format not requested, returns raw values
	if not _format:
		return hours, minutes, seconds
	
	# Convert to string
	_hours = f"{int(hours)}h"
	_minutes = f"{int(minutes)}m"
	_seconds = f"{seconds:02}s" if isinstance(seconds, int) else f"{seconds:.2f}s"
	
	# Concatenation excluding null values
	if hours:
		result += f"{_hours} {_minutes} {_seconds}"
	elif minutes:
		result += f"{_minutes} {_seconds}"
	else:
		result += f"{_seconds}"
	
	return result
##


#
def send_notify(title, message):
	""" Triggers a notification
	"""
	notification.notify(
		title=title,
		message=message,
		app_name="PyTimer",
	)
