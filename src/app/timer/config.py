
"""
	Contains global application variables (timer view)
"""


import os
from tinydb import TinyDB


# Retrieve database base path
BASE_DIR_TIMER = os.path.dirname(os.path.abspath(__file__))
data_dir_timer = os.path.join(BASE_DIR_TIMER, "data")

# Check if the 'data' folder exists, and create it if it doesn't
if not os.path.exists(data_dir_timer):
	os.makedirs(data_dir_timer)

# Build full path to database file
db_path = os.path.join(data_dir_timer, "timers.json")

# Creating a TinyDB instance
DB_TIMER = TinyDB(db_path, indent=4)

MAX_CHAR_NAME = 18
MAX_CHAR_MESSAGE = 80

MAX_RINGS = 20
MAX_INTERVAL = 300
