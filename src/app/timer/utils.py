
"""
	Script contenant les fonctions des alarmes

"""

from datetime import datetime, timedelta
from src.app.timer.config import DB_TIMER



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
	data = DB_TIMER.all()
	
	# Si la base de données est vide, on retourne des minuteurs de base
	if not data:
		return default_timers()
	
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
	DB_TIMER.truncate()
	
	# Sauvegarde les minuteurs dans la base de données
	for timer in timers:
		timer.reset()
		print(timer)
		DB_TIMER.insert(timer.__dict__)
##


#
def default_timers():
	""" Retourne une liste de Timer par défaut
			> Lorsque la base de données n'en contenait aucun
	"""
	
	from src.app.timer.timer import Timer
	
	# Création d'une liste de 3 timers par défaut
	default_timers = [
		{"title": "Temps de travail",
		 "message": "La pause est terminée.",
		 "timer": 45 * 60,  # 45 * 60
		 "number_rings": 5,
		 "interval": 30},
		
		{"title": "Temps de jeu",
		 "message": "La partie est fini !",
		 "timer": 30 * 60,  # 30 * 60
		 "number_rings": 1,
		 "interval": 60},
		
		{"title": "Cuisson des pâtes",
		 "message": "Les pâtes sont cuites !",
		 "timer": 10 * 60,  # 10 * 60
		 "number_rings": 8,
		 "interval": 15}
	]
	
	# Retourne-les timers
	return [Timer(**timer) for timer in default_timers]
##


#
def new_date(seconds: int | float | timedelta = 10) -> datetime:
	""" Calcule une nouvelle date
	
	- Ajoute un nombre spécifié de secondes à l'heure actuelle pour créer la nouvelle date.

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
		return current_time + timedelta(seconds=seconds)
	
	if isinstance(seconds, timedelta):
		return current_time + seconds

	return current_time + timedelta(seconds=seconds)


if __name__ == '__main__':
	
	# region test date
	# Test new_date
	# date = new_date(2000000)
	# print(datetime.now(), date, sep="\n")
	# endregion
	
	
	# region Test de sauvegarde d'un timer
	from app.timer.timer import Timer
	
	# timers = default_timers()
	#
	# # Test de la sauvegarde
	# save_timers(timers)
	# #
	# # Test du chargement
	# timers = load_timers()
	# print(timers)
	
	

	
	
	
	# endregion
	pass









