
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
	lundi 1 avril 2024 12:28:20
"""


import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from app.timer.config import MAX_CHAR_NAME, MAX_CHAR_MESSAGE
from app.timer.dates import new_date
from utils import format_duration, send_notify


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
	def timeleft(self):
		""" Attribut du temps restant """
		return format_duration(self._timeleft)
	
	@property
	def end_date(self):
		""" Attribut de la date de fin """
		return self._end_date.strftime("%H:%M:%S") if self._end_date else None
	##
	
	#
	def __str__(self):
		""" Affichage des information """
		display = f"Timer(\n\ttitle='{self.title}', " + "\n"
		display += f"\tmessage='{self.message}', " + "\n"
		display += f"\ttimer={self.timer}, " + "\n"
		display += f"\tduration={self.duration}, " + "\n"
		display += f"\ttimeleft={self._timeleft}, " + "\n"
		display += f"\tend_date={self._end_date}, " + "\n"
		display += f"\trunning={self.running}" + "\n)\n"
		
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
		""" Démarre le timer
		- Vérifie que le timer n'est pas déjà en cours.
		- Utilise les secondes restantes et la fonction new_date pour définir la date de fin du timer.
		- Passer l'attribut running à True.
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
		
		return self._end_date
	##
	
	#
	def stop_timer(self, reset: bool = False):
		""" Arrête le timer
		
		- capable de réinitialiser le timer.
		
		Args:
			- reset (bool): Permet de réinitialiser le timer à sa durée par défaut.
		"""
		
		# Vérifie que le timer est actif
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
		""" Calcule le temps restant du timer
		- Soustrais l'heure actuelle à la date de fin du timer pour obtenir le temps restant en timedelta.
		
		Args:
			- format (bool): Permet de formater le temps restant en heures, minutes et secondes.
		"""
		
		# Vérifie que le timer est actif
		if not self.running:
			# Si le formatage est demandée
			if _format:
				# Formate le temps restant
				return self.timeleft
			else:
				# Retourne le timedelta
				return self._timeleft
		
		# Calcule le temps restant
		self._timeleft = self._end_date - datetime.now()
		
		# Si le minuteur est terminée, déclenche la notification
		if self._timeleft.total_seconds() < 0:
			if not self.end:
				send_notify(self.title, self.message)
				self.end = True
		
		# Si le formatage est demandée
		if _format:
			# Formate le temps restant
			return self.timeleft
		else:
			# Retourne le timedelta
			return self._timeleft
	##
	
	#
	def reset(self):
		""" Permet de reset le timer à sa durée par défaut """
		if self.running:
			self.stop_timer()
		self._timeleft = self.timer
		self.end = False
	##


#
if __name__ == '__main__':
	
	# 24 caractères : feuizhto
	# 120 caractères : fderzgifgezrgfyerzgyuzegqxf,o'zygfxsquiy'xgtqou'zygtniux'gytquyef'g(qcne,tuyn'grtoecxutgseu('cntgnesuy(
	
	# Test
	timer = Timer(title="gtr",
	              message="",
	              timer=16058,
	              )
	
	print(timer)
	
	# Test de la création de date de fin
	timer.start_timer()
	print("Création de la date de fin : \n", timer, "\n")
	
	
	# Test du calcul du temps restant
	
	for i in range(15):
		# # On attend quelque seconde avec time.sleep(5)
		time.sleep(1)
		# On met à jour le temps restant
		timer.set_timeleft()
		# On affiche le temps restant
		print("Test du calcul du temps restant : \n", timer._timeleft, "\n")
	
	
	# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
	# Test de création d'une date et du calcul du timedelta.

	# time_left = new_date(20) - datetime.now()
	# print(time_left, type(time_left), "\n")
	# print(new_date(time_left))
	# >
	

	# -- -- -- -- -- -- -- -- -- -- -- -- -- --
	# Test de calcul avec un timedelta négatif

	# time_left = new_date(-20) - datetime.now()
	# print(time_left, type(time_left), "\n")
	#
	# # conversion en secondes
	# print(time_left.total_seconds())
	
	#
	pass
		