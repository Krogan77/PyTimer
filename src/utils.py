
""" Utils.py / Contains the project's utility functions. """

from tinydb import TinyDB

from pathlib import Path
import logging

from settings import CONSOLE_DEBUG, LOG


# Project folder path
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Retrieves project path in string format
PROJECT_PATH = str(Path(PROJECT_DIR))

# Retrieves the project name at the end of the path after the last slash
PROJECT_NAME = PROJECT_PATH[PROJECT_PATH.rfind("\\") + 1:]

# Project folder path
CUR_DIR = Path(__file__).resolve().parent.parent

lib_dir = CUR_DIR / "lib"
lib_dir.mkdir(exist_ok=True)

# Creates a data folder if it doesn't exist
data_dir = CUR_DIR / "data"
data_dir.mkdir(exist_ok=True)
config_backup_file = data_dir / "config_backup.json"


def check_work_path():
	""" Check application location to differentiate icons.
	> When the application is launched

	- It checks that you are on the application's working site.
	"""
	# Expected path with project name at end
	work_path = f"C:\\Users\\yoann\\code\\PycharmProjects\\Project-Perso\\{PROJECT_NAME}"
	
	# Returns True if the expected path is equal to the working project path
	return work_path == PROJECT_PATH


def get_db():
	""" Recovers the database. """
	file = data_dir / "data.json"
	if not file.exists():
		file.touch()
	db = TinyDB(file, indent=4)
	return db


# Basic configuration expected in config-backup file
# which is used if it doesn't already exist.
base_config = {
	"style": "Combinear",
	"save_pos": False,
	"geox": 100,
	"geoy": 100,
	"geow": 0,
	"geoh": 288,
}


def check_config_backup():
	""" **Checks the configuration file.**.

	- Creates the config file if it doesn't exist.
	- Checks that the config file contains the expected keys by comparing it with the base config.
	- Adds and saves missing keys to the file for the application.

	:returns:"""
	import json
	
	# Creates config_backup file if none exists
	if not config_backup_file.exists():
		with open(config_backup_file, "w") as f:
			json.dump(base_config, f, indent=4)
	
	# Checks that the config_backup file contains the expected keys
	with open(config_backup_file) as f:
		config = json.load(f)
		for key in base_config.keys():
			if key not in config:
				config[key] = base_config[key]
				save_config_backup(config)


def get_config_backup():
	""" Loads and returns options from the config_backup file """
	import json
	try:
		with open(config_backup_file) as f:
			return json.load(f)
	except IOError as e:
		print(f"Error reading config file: {e}")
		return base_config


def save_config_backup(config: dict):
	""" Saves options in config_backup file """
	import json
	try:
		with open(config_backup_file, "w") as f:
			json.dump(config, f, indent=4)
	except IOError as e:
		print(f"Error writing config file: {e}")


def set_stylesheet(frame, style_sheet):
	""" Load stylesheet content from file """
	qss_path = Path(style_sheet)
	if qss_path.exists():
		with open(qss_path) as f:
			style = f.read()
			frame.setStyleSheet(style)


def create_log_file():
	""" Function for creating a new log file when
		opening the application to separate usage tracking
	"""
	
	# Prevents the creation of a log file if not configured
	if not LOG:
		return
	
	# Checks if the log folder exists
	log_dir = Path(CUR_DIR / "log")
	print(log_dir)
	if not log_dir.exists():
		log_dir.mkdir(exist_ok=True)
	
	# Creates a new log file with the date
	from datetime import datetime
	_date = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
	log_file = "log_" + _date + ".log"
	log_path = Path(log_dir / log_file).resolve()
	log_path.touch()
	
	config_log(log_path, logging.DEBUG)
	
	dbg("log file created at : " + _date)


def config_log(filepath, level, date: bool = False):
	""" Configures the log file """
	
	if date:
		form = f"{"-" * 30}" + "\n%(asctime)s : %(levelname)s : \n%(message)s\n"
	else:
		form = " %(levelname)s : %(message)s\n" + f"{'-' * 30}"
	
	logging.basicConfig(
		level=level,
		filename=filepath,
		filemode="w",
		encoding="utf-8",
		format=form,
	)


def dbg(*args, sep=" ", end="\n"):
	
	""" Displays arguments if debug mode is enabled

	- Used to centralize activation/deactivation of all program debugs
	
	:param args: Arguments to display
	:param sep: Separator between arguments
	:param end: End of line
	"""
	
	# Displays a message in the console if debug mode is enabled
	if CONSOLE_DEBUG:
		print(*args, sep=sep, end=end)
	
	# Write a message in the log file if debug mode is enabled
	if LOG:
		formated_args = sep.join([str(arg) for arg in args])
		LOG(formated_args)
