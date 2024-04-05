# -*- coding: utf-8 -*-
# Permet d'utiliser les accents dans le code

"""
	Contient les variables globales de l'application (vue timer)

"""


import os
from tinydb import TinyDB


# Récupérer le chemin de base de la base de données
BASE_DIR_TIMER = os.path.dirname(os.path.abspath(__file__))
data_dir_timer = os.path.join(BASE_DIR_TIMER, "data")

# Vérifier si le dossier 'data' existe, le créer si ce n'est pas le cas
if not os.path.exists(data_dir_timer):
	os.makedirs(data_dir_timer)

# Construire le chemin complet vers le fichier de la base de données
db_path = os.path.join(data_dir_timer, "timers.json")

# Créer une instance de TinyDB
DB_TIMER = TinyDB(db_path, indent=4)


MAX_CHAR_NAME = 18
MAX_CHAR_MESSAGE = 80

MAX_RINGS = 20
MAX_INTERVAL = 300
