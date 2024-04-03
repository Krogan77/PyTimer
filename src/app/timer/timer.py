
# -*- coding: utf-8 -*-
# Permet d'utiliser les accents dans le code

"""

    $ -- Timer -- $

Description :
    Classe représentant un minuteur, capable d'être mis en pause et réinitialisé

Created :
    dimanche 31 mars 2024

Started :
    lundi 1 avril 2024 05:29:12

Last updated :
	mercredi 3 avril 2024 13:58:27
"""


import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from plyer import notification

from app.timer.config import MAX_CHAR_NAME, MAX_CHAR_MESSAGE
from app.timer.dates import new_date
from utils import dbg


@dataclass
class Timer:
	
	# Attributs définis par l'utilisateur
	
	title: str  # Titre du timer
	message: str  # Message de notification
	
	timer: int  # Temps par défaut en secondes
	
	#
	# Autres attributs
	
	_timeleft: int | timedelta = 0  # Temps restant en secondes et microsecondes
	
	# Date de fin du timer
	_end_date: Optional[datetime] = None
	
	running: bool = False  # État du timer
	end: bool = False  # Permet de vérifier si le timer est terminée
	
	#
	def __post_init__(self):
		""" Initialisation """
		
		# Vérifie que le titre et le message sont valides.
		self.check_message_lenght()
		
		# Défini la durée restante par défaut
		self._timeleft = self.timer
	##
	
	@property
	def duration(self):
		""" Attribut de la durée par défaut """
		return format_duration(self.timer)
	##
	
	@property
	def hours(self):
		""" Attribut du temps en heures """
		return format_duration(self.timer, _format=False)[0]
	
	@property
	def minutes(self):
		""" Attribut du temps en minutes """
		return format_duration(self.timer, _format=False)[1]
	
	@property
	def seconds(self):
		""" Attribut du temps en secondes """
		return format_duration(self.timer, _format=False)[2]
	
	@property
	def timeleft(self):
		""" Attribut du temps restant """
		return format_duration(self._timeleft)
	
	@property
	def end_date(self):
		""" Attribut de la date de fin """
		return self._end_date.strftime("%H:%M:%S") if self._end_date else "---"
	##
	
	#
	def __str__(self):
		""" Affichage des information """
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
		""" Vérifie la longueur du titre et du message
		- Lève une erreur si un élément est incorrect.
		"""
		
		# Vérification du titre
		if not 0 < len(self.title) < MAX_CHAR_NAME+1:
			obj = "nom"
			max_char = MAX_CHAR_NAME
		
		# Vérification du message
		elif not len(self.message) < MAX_CHAR_MESSAGE+1:
			obj = "message"
			max_char = MAX_CHAR_MESSAGE
			
		else:
			# Si aucune erreur, on sort de la fonction.
			return
		
		# Si une erreur est survenue, on la lève avec les infos
		raise AttributeError(f"Le nombre de caractère du {obj} ne doit pas dépasser {max_char}.")
	##
	
	#
	def start_timer(self):
		""" Démarrage du timer
		"""
		if self.end:
			return
		
		# Vérifie que le timer n'est pas déjà en cours
		if self.running:
			self.stop_timer()
			return
		
		# Défini la date de fin
		self._end_date = new_date(self._timeleft)
		
		# Passe l'attribut running à True
		self.running = True
	##
	
	#
	def stop_timer(self, reset: bool = False):
		""" Arrête le timer
		
		- capable de réinitialiser le timer.
		
		Args:
			- reset (bool): Permet de réinitialiser le timer à sa durée par défaut.
		"""
		
		# Vérifie que le timer est bien actif
		if not self.running:
			return
		
		# Désactive le timer
		self.running = False
		
		# Réinitialise le temps restant si demandé
		if reset:
			self.reset()
	##
	
	#
	def set_timeleft(self, _format: bool = False):
		""" Calcule du temps restant du timer
		- Déclenche la notification si le timer est terminée.
		- renvoie le temps restant avec formatage si demandé pour l'affichage.
		
		Args:
			- format (bool): Permet de renvoyer le temps restant formaté.
		"""
		
		if self.running:
			# Calcule le temps restant
			self._timeleft = self._end_date - datetime.now()
			
			# Si le minuteur est terminée, déclenche la notification
			if self._timeleft.total_seconds() < 0:
				if not self.end:
					send_notify(self.title, self.message)
					self.end = True
		
		# Retourne le temps restant avec formatage si demandé
		return self.timeleft if _format else self._timeleft
	##
	
	#
	def reset(self):
		""" Réinitialisation du timer """
		
		# Arrête le timer s'il est actif.
		if self.running:
			self.stop_timer()
			
		# Reset des attributs
		self._timeleft = self.timer
		self._end_date = None
		self.end = False
	##
##


#
def format_duration(delta: int | float | timedelta, _format=True) -> str | tuple:
	""" Formate la durée en heures, minutes et secondes

	:param delta: Durée en secondes
	:param _format: Format de sortie
	:return: Durée formatée en heures, minutes et secondes
	"""
	result = "-" if isinstance(delta, timedelta) and delta.total_seconds() < 0 else ""
	
	# Prendre la valeur absolue de la durée en secondes
	total_seconds = abs(delta.total_seconds()) if isinstance(delta, timedelta) else abs(delta)
	
	# Calcul des heures, minutes et secondes
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	
	# Ajouter une logique pour permettre de renvoyer les heures, minutes et secondes
	if not _format:
		return hours, minutes, seconds
	
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
##


#
def send_notify(title, message):
	""" Déclenche une notification """
	notification.notify(
		title=title,
		message=message,
		app_name="PyTimer",
	)


#
if __name__ == '__main__':
	
	# Test
	timer = Timer(title="gtr",
	              message="",
	              timer=16058,
	              )
	
	dbg(timer)
	
	# Test de la création de date de fin
	timer.start_timer()
	dbg("Création de la date de fin :", timer, sep="\n")
	
	
	# Test du calcul du temps restant
	
	for i in range(15):
		# # On attend quelque seconde avec time.sleep(5)
		time.sleep(1)
		# On met à jour le temps restant
		timer.set_timeleft()
		# On affiche le temps restant
		dbg("Test du calcul du temps restant : \n", timer._timeleft, "\n")
	
	
	# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
	# Test de création d'une date et du calcul du timedelta.

	# time_left = new_date(20) - datetime.now()
	# dbg(time_left, type(time_left), "\n")
	# dbg(new_date(time_left))
	# >
	

	# -- -- -- -- -- -- -- -- -- -- -- -- -- --
	# Test de calcul avec un timedelta négatif

	# time_left = new_date(-20) - datetime.now()
	# dbg(time_left, type(time_left), "\n")
	#
	# # conversion en secondes
	# dbg(time_left.total_seconds())
	
	#
	pass
	