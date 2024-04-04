
"""
	Script contenant les fonctions des alarmes

"""

from datetime import datetime, timedelta
import os
from tinydb import TinyDB


# Récupérer le chemin de base de la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(BASE_DIR, "data")

# Vérifier si le dossier 'data' existe, le créer si ce n'est pas le cas
if not os.path.exists(data_dir):
	os.makedirs(data_dir)

# Construire le chemin complet vers le fichier de la base de données
db_path = os.path.join(data_dir, "timers.json")

# Créer une instance de TinyDB
db = TinyDB(db_path, indent=4)


def load_timers():
	"""
	Chargement des minuteurs depuis la base de données
		> Lors de l'ouverture de l'application timer
	
	- Récupère les minuteurs depuis la base de données.
	- Crée les minuteurs avant de les retourner.
	
	Returns:
		list: Liste des minuteurs
	"""
	
	from src.app.timer.timer import Timer
	
	# Récupère les minuteurs depuis la base de données
	data = db.all()
	
	# Si la base de données est vide, on retourne des minuteurs de base
	if not data:
		return create_timers()
	
	# Si des minuteurs existent déjà
	else:
		# Création des minuteurs
		timers = []
		for timer in data:
			timer = Timer(**timer)
			timers.append(timer)
		
		# Retourne les minuteurs
		return timers
##


#
def save_timers(timers):
	"""
	Sauvegarde des minuteurs dans la base de données
		> lors de la fermeture de la vue des timers
	
	Args:
		timers : list
			Liste des minuteurs à sauvegarder
	"""
	
	# Supprime la base de données précédente
	db.truncate()
	
	# Sauvegarde les minuteurs dans la base de données
	for timer in timers:
		timer.reset()
		db.insert(timer.__dict__)
##


#
def create_timers(nombre=3):
	# Création d'une liste de 3 timers
	from src.app.timer.timer import Timer
	
	duration = [30, 300, 1500]
	
	timers = []
	for i in range(1, nombre+1):
		timer = Timer(f"Timer {i}", "Message de notification", timer=duration[i-1])
		timers.append(timer)
	return timers
##


#
def new_date(seconds: int | float | timedelta = 10) -> datetime:
	"""
	Calcule une nouvelle date en ajoutant un nombre spécifié de secondes à l'heure actuelle ou retourne l'heure actuelle.

	Args:
		- seconds (int, float, timedelta): Le nombre de secondes
			à ajouter à l'heure actuelle pour calculer la nouvelle date.
		- now (bool): Si True, la fonction retournera l'heure actuelle.

	Returns:
		- datetime: Date future calculée.

	Exemples:
		Pour obtenir une date 20 secondes dans le futur:
			>>> new_date(seconds=20)
	
	Notes:
		- Il est possible de donner une valeur négative à cette fonction pour obtenir une date
			dans le passé, puis de soustraite la date obtenue à l'heure actuelle pour
			obtenir un timedelta négatif.
	"""
	
	current_time = datetime.now()
	
	if isinstance(seconds, float):
		microseconds = get_microseconds(seconds)
		seconds = int(seconds)
		date = current_time + timedelta(seconds=seconds, microseconds=microseconds)
		return date
	if isinstance(seconds, timedelta):
		date = current_time + seconds
		return date
	
	date = current_time + timedelta(seconds=seconds)
	return date


def get_microseconds(seconds: float) -> int:
	""" Récupère les microsecondes d'un nombre de secondes en float
	
	- Permet à la fonction new_date d'accepter les float.
	
	Args:
		seconds (float): Le nombre de secondes en float.
		
	Returns:
		int: Les microsecondes du nombre de secondes en int.
	"""
	
	# Converti les microsecondes en string
	seconds_str = str(seconds)
	microseconds = ""
	
	# Vérifie si un point se trouve bien dans le float
	if "." in seconds_str:
		point = False  # Permet de savoir si on a atteint le point
		
		for char in seconds_str:
			if point:
				microseconds += char
				continue
			
			if char == ".":
				point = True
				continue
			print(microseconds)
			
		
		# Récupère les microsecondes
		microseconds = microseconds[:6]
		
		# Retourne les microsecondes en int
		return int(microseconds)


if __name__ == '__main__':
	
	# region test date
	# Test new_date
	# date = new_date(2000000)
	# print(datetime.now(), date, sep="\n")
	
	# -- Test de création de date avec un float -- #
	
	# Création d'un float
	mon_float = 12.484568
	#
	# # Récupère les microsecondes
	# microseconds = get_microseconds(mon_float)
	#
	# # Création d'un time delta avec microsecondes
	# duration = timedelta(seconds=int(mon_float), microseconds=microseconds)
	#
	# # Résultat
	# print(f"microseconds = {microseconds}",
	#       f"duration = {duration}",
	#       sep="\n",
	#       )
	#
	# now = datetime.now()
	# new = now + timedelta(seconds=mon_float, microseconds=microseconds)
	# print(now, new, sep="\n")
	
	# Test maintenant que la méthode accepte les float
	new = new_date(mon_float)
	
	now = datetime.now()
	print(now, new, sep="\n")
	# endregion
	
	
	# region Test de sauvegarde d'un timer
	from app.timer.timer import Timer
	
	timers = create_timers()
	
	# Test de la sauvegarde
	save_timers(timers)
	#
	# Test du chargement
	timers = load_timers()
	print(timers)
	
	
	# endregion
	pass