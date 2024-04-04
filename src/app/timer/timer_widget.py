
# -*- coding: utf-8 -*-
# Permet d'utiliser les accents dans le code


""" Classe TimerWidget

Description :
    Permet d'afficher un timer.
    
"""

# Todo Doc.


from PySide6.QtCore import QSize, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from src.utils import dbg

font_weight = "font-weight: 750;"


class TimerWidget(QWidget):
	submit_timer = Signal(object, object)
	
	def __init__(self, timer=None, parent=None):
		super().__init__()
		self.timer = timer
		self.parent = parent
		
		
		# Création des éléments de l'interface
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
		
	##
		
	def setup_ui(self):
		""" Configuration de l'interface """
		
		self.hlayout = QHBoxLayout()
		self.setLayout(self.hlayout)
		
		# Bouton start
		self.btn_play = QPushButton()
		self.btn_play.setIcon(QIcon("lib/icons/icon_play"))
		self.hlayout.addWidget(self.btn_play)
		
		self.vlayout = QVBoxLayout()
		self.hlayout.addLayout(self.vlayout)
		
		# Infos timer
		self.lb_title = QLabel(self.timer.title)
		self.vlayout.addWidget(self.lb_title)
		
		self.lb_duration = QLabel(self.timer.duration)
		self.vlayout.addWidget(self.lb_duration)
		
		self.vlayout_time = QVBoxLayout()
		self.hlayout.addLayout(self.vlayout_time)
		
		self.lb_timeleft = QLabel(str(self.timer.timeleft))
		self.vlayout_time.addWidget(self.lb_timeleft)
		
		self.lb_end_date = QLabel(str(self.timer.end_date))
		self.vlayout_time.addWidget(self.lb_end_date)
		
		# Boutons reset et modifier
		self.btn_reset = QPushButton()
		self.btn_reset.setIcon(QIcon("lib/icons/icon_reset"))
		self.hlayout.addWidget(self.btn_reset)
		
		self.btn_modify = QPushButton()
		self.btn_modify.setIcon(QIcon("lib/icons/icon_modify"))
		self.hlayout.addWidget(self.btn_modify)
	
	#
	def set_style(self):
		""" Modification du style """
		
		self.setStyleSheet("""
			* {
				font-weight: 600;
				padding: 0px;
				margin: 0px;
			}
			
			QLabel {
				text-align: center;
				font-size: 13px;
				margin-left: 8px;
			}
			
			QPushButton {
				border: none;
				border-radius: 10px;
				min-width: 0px;
				min-height: 0px;
				padding: 10px;
				margin-bottom: 3px;
				margin-right: 5px;
				margin-left: 3px;
			}
			""")
		
		self.lb_title.setStyleSheet(f"QLabel {{{font_weight}}}")
		self.lb_timeleft.setStyleSheet(f"QLabel {{{font_weight}}}")
		
		# Modification de la taille des boutons
		icon_size = 24
		button_size = 38
		
		self.btn_play.setIconSize(QSize(icon_size, icon_size))
		self.btn_play.setFixedSize(QSize(button_size, button_size))
		
		self.btn_reset.setIconSize(QSize(icon_size, icon_size))
		self.btn_reset.setFixedSize(QSize(button_size, button_size))
		
		self.btn_modify.setIconSize(QSize(icon_size, icon_size))
		self.btn_modify.setFixedSize(QSize(button_size, button_size))
	
	#
	def setup_connections(self):
		""" Création des connecions entre les widgets """
		
		self.btn_play.clicked.connect(self.start_timer)
		
		self.btn_reset.clicked.connect(self.reset_timer)
		
		self.btn_modify.clicked.connect(self.modify_timer)
	##
	
	#
	def set_default_values(self):
		""" Définition des valeurs par défaut """
		self.check_color = False
		pass
	##
	
	#
	@Slot()
	def modify_timer(self):
		""" Envoi le signal du bouton de modification """
		self.submit_timer.emit(self.timer, self)
	##
	
	#
	def start_timer(self):
		""" Démarre, arrête ou reset le timer
		
		- Si le timer est inactif, il sera lancé
		
		- S'il est en cours, il sera stopper et pourra être relancé.
		
		- S'il est en cours et terminé, il sera stoppé et réinitialisé.
		"""
		
		if self.timer.end:
			if self.timer.running:
				# Si le timer est en cours, mais terminé, on le stop
				self.timer.stop_timer()
				self.btn_play.setIcon(QIcon("lib/icons/icon_reset"))
				return
			
			# Si le timer est terminé, et déjà stoppé, on le reset
			self.reset_timer()
			return
		
		# Si le timer est inactif ou en pause, on le démarre
		self.timer.start_timer()
		
		# Affichage de la date de fin
		self.lb_end_date.setText(str(self.timer.end_date))
		
		# Modification du style du bouton et de la durée restante
		self.set_style_btn_start()
		self.lb_timeleft.setStyleSheet(f"QLabel {{color: green;{font_weight}}}")
		
		# todo Démarrage des timers:
		#  vérifier si le timer est actif, modifier le bouton reset en conséquence
		#  afin qu'il devienne un bouton pour ajouter du temps ou redevenienne un bouton reset
		#  - Modifier l'icône du bouton et ajouter un if-else pour gérer la logique du nouveau bouton reset
		#  devra modifier l’affichage en soustrayant le temps qui a été rajouté a la durée restante pour qu’elle
		#  reste négative
		#  :
		#  Ce qui veut dire que pour reset le timer il faudra le mettre en pause pour avoir accès au bouton reset
		#  et le bouton start sera aussi un bouton reset lorsque le timer sera terminé ET en pause.
	
	#
	def update_timeleft(self):
		""" Mise à jour de l'affichage du temps restant si le timer est en cours """
		
		# Modification de la durée restante
		if self.timer.running:
			self.lb_timeleft.setText(str(self.timer.set_timeleft(_format=True)))
			
			# Vérifie si la date de fin est atteinte et modifie la couleur du texte
			if self.timer.end and not self.check_color:
				self.lb_timeleft.setStyleSheet(f"QLabel {{color: red;{font_weight}}}")
				# Empêche de refaire ce check à chaque mise à jour de l'affichage
				self.check_color = True
	##
	
	#
	def reset_timer(self, check_duration=False):
		""" Réinitialisation du timer
		
		- Si la durée par défaut a été modifiée, on réinitialise le timer.
		- Si elle n'a pas été modifiée, on laisse le timer tourner.
		"""
		
		# Vérifie si la durée par défaut a été modifiée
		if check_duration:
			if self.lb_duration.text() == self.timer.duration:
				self.lb_title.setText(self.timer.title)
				return
		
		# Réinitialise le timer
		self.timer.reset()
		
		# Mis à jour de l'affichage
		self.lb_title.setText(self.timer.title)  # titre
		self.lb_duration.setText(self.timer.duration)  # durée par défaut
		self.lb_timeleft.setText(str(self.timer.timeleft))  # durée restante avec millisec
		self.lb_end_date.setText(str(self.timer.end_date))  # Date de fin
		
		# Modification du style du bouton play et de la durée restante
		self.btn_play.setIcon(QIcon("lib/icons/icon_play"))
		self.lb_timeleft.setStyleSheet(f"QLabel {{color: white;{font_weight}}}")
		self.check_color = False
	##
	
	#
	def set_style_btn_start(self):
		""" Modification du style du bouton start """
		
		# Si le timer est en cours, icon stop
		if self.timer.running:
			self.btn_play.setIcon(QIcon("lib/icons/icon_break"))
			
		# Si le timer est terminée ou en pause, bouton start
		else:
			self.btn_play.setIcon(QIcon("lib/icons/icon_play"))
	##
#
	