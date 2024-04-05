
# -*- coding: utf-8 -*-
# Permet d'utiliser les accents dans le code

"""
    $ -- Timer -- $

Classe représentant un minuteur.

"""


import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from plyer import notification

from app.timer.utils import new_date
from app.timer.config import MAX_CHAR_NAME, MAX_CHAR_MESSAGE
from src.utils import dbg


@dataclass
class Timer:
	
	# Attributs définis par l'utilisateur
	
	title: str  # Titre du timer
	message: str  # Message de notification
	
	timer: int  # Temps par défaut en secondes
	
	#
	# Autres attributs
	
	_timeleft: int | timedelta = 0  # Temps restant en secondes et microsecondes
	
	number_rings: int = 0  # Nombre de sonneries
	_number_rings: int = 0  # Nombre de sonneries restantes
	
	interval: int = 0  # Temps par défaut entre chaque sonnerie
	_interval: int = 0  # Temps actuellement utilisé entre chaque sonnerie
	
	# Date de fin du timer
	_end_date: Optional[datetime] = None
	
	# Date utilisée pour la prochaine notification lorsque le timer après que le timer a dépassé sa date de fin.
	notif_date: Optional[datetime] = None
	
	# État du timer
	running: bool = False
	remaining: bool = False
	# Permet de vérifier si le timer est terminée
	end: bool = False
	
	#
	def __post_init__(self):
		""" Initialisation """
		
		# Vérifie que le titre et le message sont valides.
		self.check_message_lenght()
		
		# Défini la durée restante par défaut
		self._timeleft = self.timer
		
		self.check_number_rings()
		self.check_times_between_rings()
	
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
		""" Affichage des informationde l'objet """
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
			# S'il est incorect, on définit les infos de l'erreur
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
	def check_number_rings(self):
		""" Vérifie que le nombre de sonneries est valide """
		if self.number_rings > self._number_rings:
			self._number_rings = self.number_rings
	##
	
	def check_times_between_rings(self):
		""" Permet de reset le temps entre les sonneries """
		if self.interval != self._interval:
			self._interval = self.interval
	##
	
	#
	def start_timer(self):
		""" Démarrage du timer """
		if self.end:
			return
		
		# Vérifie que le timer n'est pas déjà en cours
		if self.running:
			self.stop_timer()
			return
		
		# Défini la date de fin
		self._end_date = new_date(self._timeleft)
		self.notif_date = self._end_date
		
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
		""" Mis à jour du timer
		
		- Calcul et renvoie du temps restant
		- Déclenche des notifications lorsque le timer dépasse les dates prévues.
		
		Args:
			- format (bool): Permet de renvoyer le temps restant formaté si True.
		"""
		
		# S'assure que le timer est actif, on ne fait rien sinon
		if self.running:
			now = datetime.now()  # Récupère la date actuelle
			
			# Calcul le temps restant en utilisant la date de fin réelle pour l'affichage
			self._timeleft = self._end_date - now
			
			# Calcul du temps restant avant la prochaine sonnerie
			timeleft_notif = self.notif_date - now
			
			# Si la date de fin est dépassée, déclenche une notification
			if timeleft_notif.total_seconds() < 0:
				self.remaining = True
				# Calcul des secondes écoulées depuis la date de fin
				# avec formatage pour l'affichage dans la notification
				seconds = format_duration((now - self._end_date).seconds)
				
				# S'il reste des sonneries supplémentaires à déclencher
				if self._number_rings:
					
					# Récupère le message de notification pour pouvoir le modifier localement
					message = self.message
					
					# Si le nombre de sonneries par défaut est différent du nombre de sonneries restantes
					if self.number_rings != self._number_rings:
						
						# On modifie le message de notification pour afficher le temps écoulée depuis la date de fin
						message += f"\n - {seconds} !"
					
					# Déclenche la notification
					send_notify(self.title, message)
					
					# Ajoute du temps supplémentaire pour la prochaine notif
					self.notif_date += timedelta(seconds=self._interval)
					
					self._number_rings -= 1  # Nombre de sonneries restantes -1
					return
				
				# Dernière sonnerie lorsque le nombre de sonneries est à zéro
				if not self.end:
					
					# Si ce n'est pas la première sonnerie,
					# car le nombre par défaut n'est pas zéro
					if self.number_rings:
						# Modification du message de notification pour afficher le temps écoulée
						message = self.message + f"\n - {seconds} !"
					else:
						# Sinon, on garde le message par défaut
						message = self.message
					
					# Déclenche la notification
					send_notify(self.title, message)
					self.end = True
		
		# Dans tous les cas, on renvoie le temps restant avec formatage si demandé
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
		self.notif_date = None
		self.remaining = False
		self.end = False
		self.check_number_rings()
		self.check_times_between_rings()
	##
##


#
def format_duration(delta: int | float | timedelta, _format=True) -> str | tuple:
	""" Formate la durée en heures, minutes et secondes

	:param delta: Durée en secondes
	:param _format: Format de sortie
	:return: Durée formatée en heures, minutes et secondes
	"""
	result = "- " if isinstance(delta, timedelta) and delta.total_seconds() < 0 else ""
	
	# Prendre la valeur absolue de la durée en secondes
	total_seconds = abs(delta.total_seconds()) if isinstance(delta, timedelta) else abs(delta)
	
	# Calcul des heures, minutes et secondes
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	
	# Si le format n'est pas demandé, renvoie les valeurs brutes
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
	timer = Timer(title="gtrxd",
	              message="notification",
	              timer=16058,
	              number_rings=3,
	              interval=10,
	              )
	
	dbg(timer)
	
	# Test de la création de date de fin
	timer.start_timer()
	dbg("Création de la date de fin :", timer, sep="\n")
	timer._end_date += timedelta(seconds=30)
	dbg("Repoussement de la date de fin :", timer, sep="\n")

	
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
	