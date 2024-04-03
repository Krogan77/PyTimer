
# -*- coding: utf-8 -*-
# Permet d'utiliser les accents dans le code


""" Classe TimerWidget

Description :
    Permet d'afficher un timer.
    
"""

from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from utils import dbg

font_weight = "font-weight: 750;"


class TimerWidget(QWidget):
	submit_timer = Signal(object, object)
	
	def __init__(self, timer=None, parent=None):
		super().__init__()
		self.timer = timer
		self.parent = parent
		
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
		
	##
		
	def setup_ui(self):
		""" Configuration de l'interface """
		
		self.hlayout = QHBoxLayout()
		self.setLayout(self.hlayout)
		
		self.btn_play = QPushButton()
		self.btn_play.setIcon(QIcon("lib/icons/icon_play"))
		self.hlayout.addWidget(self.btn_play)
		
		self.vlayout = QVBoxLayout()
		self.hlayout.addLayout(self.vlayout)
		
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
	
	#
	def set_default_values(self):
		""" Définition des valeurs par défaut """
		self.check_color = False
		pass
	
	def start_timer(self):
		""" Démarre, arrête ou reset le timer
		
		- Si le timer est inactif, il sera lancé
		
		- Si le timer est en cours, il sera stopper
		
		- Si le timer est terminé :
			Il sera juste stoppé pour commencer, mais gardera son état dépassé (terminée),
			et lors du prochain appui sur le bouton, il sera réinitialisé.
		"""
		
		if self.timer.end:
			
			# Si le timer est en cours, on le stop et rien d'autre
			if self.timer.running:
				# stop le timer seulement pour le premier appui sur le bouton
				self.timer.stop_timer()
				self.btn_play.setIcon(QIcon("lib/icons/icon_reset"))
				return
			
			# Ensuite, reset le timer
			self.reset_timer()
			return
		
		self.timer.start_timer()
		self.lb_end_date.setText(str(self.timer.end_date))
		
		self.set_style_btn_start()
		self.lb_timeleft.setStyleSheet(f"QLabel {{color: green;{font_weight}}}")
		
		# todo Démarrage des timers:
		#  vérifier si le timer est actif, modifier le bouton reset en conséquence
		#  afin qu'il devienne un bouton pour ajouter du temps ou redevenienne un bouton reset
		#  - Modifier l'icône du bouton et ajouter un if-else pour gérer la logique du nouveau bouton reset
		#  devra modifier l’affichage en soustrayant le temps qui a été rajouté a la durée restante pour qu’elle reste négative
		#  :
		#  Ce qui veut dire que pour reset le timer il faudra le mettre en pause pour avoir accès au bouton reset
		#  et le bouton start sera aussi un bouton reset lorsque le timer sera terminé ET en pause.
	
	
	def update_timeleft(self):
		""" Mise à jour de l'affichage du temps restant si le timer est en cours """
		if self.timer.running:
			self.lb_timeleft.setText(str(self.timer.set_timeleft(_format=True)))
			
			# Modifie la couleur de la durée restante s'ils sont dépassé,
			# seulement sur les timers actifs
			# et une seule fois lorsque le check n'a pas encore été fait
			if self.timer.end and not self.check_color:
				self.lb_timeleft.setStyleSheet(f"QLabel {{color: red;{font_weight}}}")
				self.check_color = True
	
	def reset_timer(self, modify=False):
		""" Réinitialise le timer
		
		- Si le timer est reset après modification, on vérifie si la durée par défaut a été modifiée
		  avant de réinitialiser la durée restante.
		  Si la durée par défaut a été modifiée, on doit absolument modifier la durée restante.
		  Si elle n'a pas été modifiée, on ne doit pas stopper le timer.
		"""
		if modify:
			if self.lb_duration.text() == self.timer.duration:
				self.lb_title.setText(self.timer.title)
				return
		
		# Réinitialise le timer
		self.timer.reset()
		
		# Réinitialise les valeurs
		self.lb_title.setText(self.timer.title)  # titre
		self.lb_duration.setText(self.timer.duration)  # durée par défaut
		self.lb_timeleft.setText(str(self.timer.timeleft))  # durée restante avec millisec
		self.lb_end_date.setText(str(self.timer.end_date))  # Date de fin
		
		# Modifie le style
		self.btn_play.setIcon(QIcon("lib/icons/icon_play"))
		self.lb_timeleft.setStyleSheet(f"QLabel {{color: white;{font_weight}}}")
		self.check_color = False
	
	def modify_timer(self):
		""" Envoi le signal pour la modification """
		self.submit_timer.emit(self.timer, self)
	
	def set_style_btn_start(self):
		""" Modification du style du bouton start """
		
		# Si le timer est en cours, icon stop
		if self.timer.running:
			self.btn_play.setIcon(QIcon("lib/icons/icon_break"))
			
		# Si le timer est terminée ou en pause, bouton start
		else:
			self.btn_play.setIcon(QIcon("lib/icons/icon_play"))
		




	
		
	
	#
	