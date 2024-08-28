
"""
	Script containing useful application functions
"""

from datetime import datetime, timedelta
from src.app.timer.config import DB_TIMER



def load_timers():
	"""
	Loading timers from the database
		> When opening the timer application
	
	- Retrieves timers from the database.
	- Create timers before returning them.
	
	Returns:
		list: Timer list
	"""
	
	from src.app.timer.timer import Timer
	
	# Retrieves timers from database
	data = DB_TIMER.all()
	
	# If the database is empty, basic timers are returned
	if not data:
		return default_timers()
	
	# If timers already exist
	else:
		# Creating timers
		timers = []
		for timer in data:
			timer = Timer(**timer)
			timers.append(timer)
		
		# Return timers
		return timers
##


#
def save_timers(timers):
	"""
	Saving timers in the database
		> when closing the timer view
	
	Args:
		timers : list
			List of timers to save
	"""
	
	# Deletes the previous database
	DB_TIMER.truncate()
	
	# Saves timers in database
	for timer in timers:
		timer.reset()
		DB_TIMER.insert(timer.__dict__)
##


#
def default_timers():
	""" Returns a list of default timers
			> When the database contained none
	"""
	
	from src.app.timer.timer import Timer
	
	# Create a list of 3 default timers
	default_timers = [
		{"title": "Cooking",
		 "message": "The food is ready!",
		 "timer": 10 * 60,  # 10 * 60
		 "number_rings": 8,
		 "interval": 15},
		
		{"title": "Playing time",
		 "message": "The game's over!",
		 "timer": 30 * 60,  # 30 * 60
		 "number_rings": 1,
		 "interval": 60},
		
		{"title": "Working hours",
		 "message": "The break is over.",
		 "timer": 45 * 60,  # 45 * 60
		 "number_rings": 5,
		 "interval": 30}
	]
	
	# Turn them over
	return [Timer(**timer) for timer in default_timers]
##


#
def new_date(seconds: int | float | timedelta = 10) -> datetime:
	""" Calculates a new date
	
	- Adds a specified number of seconds to the current time to create the new date.

	Args:
		- seconds (int, float, timedelta): The number of seconds
			à add to the current time to calculate the new date.
		- now (bool): If True, the function will return the current time.

	Returns:
		- datetime: Calculated future date.

	Examples:
		To obtain a date 20 seconds in the future:
			>>> new_date(seconds=20)
	
	Notes:
		- This function can be given a negative value to obtain a date.
			in the past, then subtract the date obtained from the current time
			to obtain a negative timedelta.
	"""
	
	current_time = datetime.now()
	
	if isinstance(seconds, float):
		return current_time + timedelta(seconds=seconds)
	
	if isinstance(seconds, timedelta):
		return current_time + seconds

	return current_time + timedelta(seconds=seconds)
