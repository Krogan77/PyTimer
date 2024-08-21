
""" Utils.py / Contient les fonctions utilitaires du projet. """

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

# Chemin du dossier du projet
CUR_DIR = Path(__file__).resolve().parent.parent

lib_dir = CUR_DIR / "lib"
lib_dir.mkdir(exist_ok=True)

# Crée le dossier data s'il n'existe pas
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
	""" Récupère la base de données. """
	file = data_dir / "data.json"
	if not file.exists():
		file.touch()
	db = TinyDB(file, indent=4)
	return db


# Configuration de base attendue dans le fichier config-backup
# qui est utilisée si elle n'existe pas déjà.
base_config = {
	"style": "Combinear",
	"save_pos": False,
	"geox": 100,
	"geoy": 100,
	"geow": 0,
	"geoh": 288,
}


def check_config_backup():
	""" **Permet de vérifier le fichier de configuration.**

	- Crée le fichier de config s'il n'existe pas.
	- Vérifie que le fichier de config contient les clés attendues en le comparant à la config de base.
	- Ajoute et sauvegarde les clés manquantes au fichier pour l'application.

	:returns:"""
	import json
	
	# Crée le fichier de config_backup s'il n'existe pas
	if not config_backup_file.exists():
		with open(config_backup_file, "w") as f:
			json.dump(base_config, f, indent=4)
	
	# Vérifie que le fichier de config_backup contient les clés attendues
	with open(config_backup_file) as f:
		config = json.load(f)
		for key in base_config.keys():
			if key not in config:
				config[key] = base_config[key]
				save_config_backup(config)


def get_config_backup():
	""" Charge et Retourne les options du fichier config_backup """
	import json
	try:
		with open(config_backup_file) as f:
			return json.load(f)
	except IOError as e:
		print(f"Error reading config file: {e}")
		return base_config


def save_config_backup(config: dict):
	""" Sauvegarde les options dans le fichier config_backup """
	import json
	try:
		with open(config_backup_file, "w") as f:
			json.dump(config, f, indent=4)
	except IOError as e:
		print(f"Error writing config file: {e}")


def set_stylesheet(frame, style_sheet):
	""" Charger le contenu de la feuille de style depuis le fichier """
	qss_path = Path(style_sheet)
	if qss_path.exists():
		with open(qss_path) as f:
			style = f.read()
			frame.setStyleSheet(style)


def create_log_file():
	""" Fonction permettant de créer un nouveau fichier de log lors de
		l'ouverture de l'application pour séparer les suivis d'utilisations
	"""
	
	# Empêche la création d'un fichier de log si cela n'est pas configurer
	if not LOG:
		return
	
	# Vérifie si le dossier de log existe
	log_dir = Path(CUR_DIR / "log")
	print(log_dir)
	if not log_dir.exists():
		log_dir.mkdir(exist_ok=True)
	
	# Crée un nouveau fichier de log avec la date
	from datetime import datetime
	_date = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
	log_file = "log_" + _date + ".log"
	log_path = Path(log_dir / log_file).resolve()
	log_path.touch()
	
	config_log(log_path, logging.DEBUG)
	
	dbg("log file created at : " + _date)


def config_log(filepath, level, date: bool = False):
	""" Configure le fichier de log """
	
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


def clamp(value: int | float, min_value: int | float, max_value: int | float) -> int | float:
	return min(max(value, min_value), max_value)


def dbg(*args, sep=" ", end="\n"):
	
	""" Affiche les arguments si le mode debug est activé

	- Est utilisé pour centraliser l'activation/désactivation de tous les debugs du programme
	
	:param args: Arguments à afficher
	:param sep: Séparateur entre les arguments
	:param end: Fin de ligne
	"""
	
	# Affiche un message dans la console si le mode debug est activé
	if CONSOLE_DEBUG:
		print(*args, sep=sep, end=end)
	
	# Écrit un message dans le fichier de log si le mode debug est activé
	if LOG:
		formated_args = sep.join([str(arg) for arg in args])
		LOG(formated_args)
