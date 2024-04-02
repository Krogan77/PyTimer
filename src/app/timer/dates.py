
"""
	Script contenant les fonctions des alarmes

"""

from datetime import datetime, timedelta


def new_date(
		seconds: int | float | timedelta = 10,
		now: bool = False)\
		-> datetime:
	
	"""
	Calcule une nouvelle date en ajoutant un nombre spécifié de secondes à l'heure actuelle ou retourne l'heure actuelle.

	Args:
	    - seconds (int, float, timedelta): Le nombre de secondes
	        à ajouter à l'heure actuelle pour calculer la nouvelle date.
		- now (bool): Si True, la fonction retournera l'heure actuelle.

	Returns:
	    - datetime: L'heure actuelle si 'now' est True, sinon une date future calculée.

	Exemples:
	    Pour obtenir l'heure actuelle:
	        >>> new_date(now=True)

	    Pour obtenir une date 20 secondes dans le futur:
	        >>> new_date(seconds=20, now=False)
	
	Notes:
		- Il est possible de donner une valeur négative à cette fonction pour obtenir une date
			dans le passé, puis de soustraite la date obtenue à l'heure actuelle pour
			obtenir un timedelta négatif.
	"""
	
	current_time = datetime.now()
	if now:
		return current_time
	
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


def new_dates(nbr: int = 3, interval: int = 15) -> list:
	"""
	Génère une liste de dates futures, chacune espacée d'un intervalle de temps donné.

	Args:
	    nbr (int): Le nombre de dates à générer.
	    interval (int): L'intervalle en secondes entre chaque date générée.

	Returns:
	    list: Une liste d'objets datetime. Si 'now' est True, la liste contiendra l'heure actuelle répétée 'nbr' fois.
	          Sinon, elle contiendra une série de dates futures espacées par l'intervalle spécifié.

	Exemples:
	    Pour obtenir une liste de l'heure actuelle répétée 3 fois:
	        >>> new_dates(nbr=3, now=True)

	    Pour générer une liste de 3 dates, chacune espacée de 15 secondes:
	        >>> new_dates(nbr=3, interval=15, now=False)
	"""
	dates = []
	for i in range(nbr):
		date = new_date(interval * (i+1))
		dates.append(date)
	
	return dates


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
	
	# Test new_date
	# date = new_date(2000000)
	# print(datetime.now(), date, sep="\n")
	
	
	# Test new_dates
	# dates = new_dates(5, 20)
	# for date in dates:
	# 	print(date.strftime("%H %M %S"))
	
	
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
	
	pass