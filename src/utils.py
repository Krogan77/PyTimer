
""" Utils.py / Contient les fonctions utilitaires du projet. """
from datetime import timedelta
from pathlib import Path
import os

from plyer import notification
from tinydb import TinyDB

# Chemin du dossier du projet
CUR_DIR = Path(__file__).resolve().parent.parent

lib_dir = CUR_DIR / "lib"
lib_dir.mkdir(exist_ok=True)

# Crée le dossier data s'il n'existe pas
data_dir = CUR_DIR / "data"
data_dir.mkdir(exist_ok=True)
config_backup_file = data_dir / "config_backup.json"


def check_work_path():
	"""
	Permet de vérifier le chemin du projet.
	> Lorsque l'application se lance

	- Cela sert à vérifier si on est sur l'emplacement de travail de l'application.
	-
	"""
	expected_path = r"C:\Users\yoann\code\PycharmProjects\2.Project\Project-Perso\PyTimer"
	# Normalisation des chemins pour s'assurer qu'ils sont comparables
	cur_dir_normalized = os.path.normcase(os.path.normpath(CUR_DIR))
	expected_path_normalized = os.path.normcase(os.path.normpath(expected_path))
	
	return cur_dir_normalized == expected_path_normalized
##

def get_db():
	""" Récupère la base de données. """
	file = data_dir / "data.json"
	if not file.exists():
		file.touch()
	db = TinyDB(file, indent=4)
	return db


# Configuration de base attendue dans le fichier de config_backup
base_config = {
	"style": "Default",
	"save_pos": False,
	"geox": 100,
	"geoy": 100,
	"geow": 0,
	"geoh": 0,
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
	import logging
	
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
	
	logging.debug("log file created at : " + _date)


def config_log(filepath, level, date: bool = False):
	""" Configure le fichier de log """
	import logging
	if date:
		form = f"{"-" * 30}" + "\n%(asctime)s : %(levelname)s : \n%(message)s\n"
	else:
		form = " %(levelname)s : %(message)s\n" + f"{"-" * 30}"
	
	logging.basicConfig(
		level=level,
		filename=filepath,
		filemode="w",
		encoding="utf-8",
		format=form,
	)


def clamp(value: int | float, min_value: int | float, max_value: int | float) -> int | float:
	return min(max(value, min_value), max_value)


def format_duration(delta: int | float | timedelta) -> str:
	""" Formate la durée en heures, minutes et secondes
	
	:param delta: Durée en secondes
	:return: Durée formatée en heures, minutes et secondes
	"""
	result = "-" if isinstance(delta, timedelta) and delta.total_seconds() < 0 else ""
	
	# Prendre la valeur absolue de la durée en secondes
	total_seconds = abs(delta.total_seconds()) if isinstance(delta, timedelta) else abs(delta)
	
	# Calcul des heures, minutes et secondes
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	
	# Conversion en string
	_hours = f"{int(hours)}h"
	_minutes = f"{int(minutes)}m"
	_seconds = f"{seconds:02}s" if isinstance(seconds, int) else f"{seconds:.2f}s"
		
	# Concaténation excluant les valeurs nulles
	if hours:
		result += f"{_hours} {_minutes} {_seconds}"
	elif minutes:
		result += f"{_minutes} {_seconds}"
	else:
		result += f"{_seconds}"
	
	return result


def send_notify(title, message):
	""" Déclenche une notification """
	notification.notify(
		title=title,
		message=message,
		app_name="PyTimer",
	)


def dbg(*args, sep=" ", end="\n"):
	
	""" Affiche les arguments si le mode debug est activé

	- Est utilisé pour centraliser l'activation/désactivation de tous les debugs du programme
	
	:param args: Arguments à afficher
	:param sep: Séparateur entre les arguments
	:param end: Fin de ligne
	"""
	
	from settings import CONSOLE_DEBUG, LOG
	
	# Affiche un message dans la console si le mode debug est activé
	if CONSOLE_DEBUG:
		print(*args, sep=sep, end=end)
	
	# Écrit un message dans le fichier de log si le mode debug est activé
	if LOG:
		formated_args = sep.join([str(arg) for arg in args])
		LOG(formated_args)



if __name__ == '__main__':
	print(CUR_DIR)
	
	print("Test de création d'un fichier de log :")
	create_log_file()
	
	dbg("Test debug log")
	dbg("Test debug log")
	
	# Test check_pass()
	print(CUR_DIR)
	print(check_work_path())
	
	#
	pass