
# -*- coding: utf-8 -*-
# Permet d'utiliser les accents dans le code

"""

    $ -- TimerView -- $

Description :
    Vue des timer

Notes :
	- Permet de gérer les timers

Fonctionnalités :
	- Création et modification des timers
	- Affichage des timers

Created :
    05:38  01/04/2024

Started :
    created.

Last updated :
	mercredi 3 avril 2024 13:58:47

Todo:
	> Sauvegarde des timers
	  - Création d'un fichier de sauvegarde
	  - Charger les timers existants lors de l'ouverture et les ajouter dans la liste
	  - passer sur les timer de la liste lors de la fermeture pour les sauvegarder
	  -
	.
	
"""

from datetime import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QVBoxLayout, QPushButton

from app.timer.timer_dialog import TimerDialog
from app.timer.timer import Timer, send_notify

from app.timer.dates import new_dates
from app.timer.timer_widget import TimerWidget


class TimerView(QWidget):
	def __init__(self):
		super().__init__()
		
		self.set_variables()
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
	
	def set_variables(self):
		""" Définition des variables de la vue """
		pass
	
	def setup_ui(self):
		""" Création des éléments de l'interface """
		
		self.hlayout = QHBoxLayout()
		self.setLayout(self.hlayout)
		
		self.vlayout = QVBoxLayout()
		self.hlayout.addLayout(self.vlayout)
		
		self.btn_new_timer = QPushButton("Nouveau Timer")
		self.vlayout.addWidget(self.btn_new_timer)
		
		self.lst_timer = QListWidget()
		self.lst_timer.setFixedWidth(350)
		self.vlayout.addWidget(self.lst_timer)
		
		# Permet de repousser les éléments sur la gauche
		# self.widget_space = QWidget()
		# self.widget_space.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
		# self.hlayout.addWidget(self.widget_space)
		
		pass
	
	def set_style(self):
		""" Modification du style des éléments """
		
		self.setStyleSheet("""
			
			QTextEdit {
				margin: 5px;
				padding: 5px;
			}
			
			QLineEdit {
			margin: 5px;
			padding: 3px;
			}
			
			QSpinBox {
			margin-top: 3px;
			margin-bottom: 3px;
			padding: 3px;
			}
			
			QLabel {
			margin-top: 5px;
			}
			
			QListWidget {
				border-radius: 10px;
			}
			
			QListWidget::item {
				border-radius: 20px;
				margin: 3px;
			}
			""")
	
	#
	def setup_connections(self):
		""" Création des connexions entre les widgets """
		self.btn_new_timer.clicked.connect(self.create_timer)
		pass
	
	#
	def set_default_values(self):
		""" Définition des valeurs par défaut """
		
		# todo Création de la liste des dates:
		#  Gérer les dates (ajouter les dates des alarmes actives dans la liste lors de leur démarrage)
		self.dates = new_dates(3, 5)
		#
		# # Timer qui servira à vérifier le déclenchement d'une notification par date pour les alarmes
		# self.timer_notify = QTimer()
		# self.timer_notify.timeout.connect(self.check_dates)
		# self.timer_notify.start(1000)  # Vérifie toutes les secondes
		
		# Timer servant à rafraîchir les timers actifs
		# et déclencher les notifications des minuteurs
		self.timer_refresh = QTimer()
		self.timer_refresh.timeout.connect(self.check_timer)
		self.timer_refresh.start(20)  # Vérifie toutes les secondes
	##
	
	#
	def check_dates(self):
		if self.dates:
			# Assurez-vous que votre liste est triée de sorte que la prochaine date soit la première
			next_date = self.dates[0]
			if datetime.now() >= next_date.replace(microsecond=0):
				# Envoie le signal pour déclencher la notification
				send_notify("Test Notify", "hello world !")
				# Supprimer la date traitée ou la mettre à jour
				self.dates.pop(0)
	
	def add_timer(self, timer):
		""" Création d'un nouveau timer !
		- Appeler par le signal du formulaire
		- Récupère le timer et le place dans son widget puis dans le list widget.
		"""
		
		self.item = QListWidgetItem()
		self.timer_widget = TimerWidget(parent=self, timer=timer)
		self.timer_widget.submit_timer.connect(self.create_timer)
		
		self.item.setSizeHint(self.timer_widget.sizeHint())
		
		self.lst_timer.addItem(self.item)
		self.lst_timer.setItemWidget(self.item, self.timer_widget)
		
	
	def create_timer(self, timer=None, widget=None):
		""" Création d'un nouveau timer """
		
		# Mode création s'il n'y a pas de timer fourni
		if not timer:
			# Ouvre la fenêtre de création et récupère le timer si l'utilisateur a validé
			dialog = TimerDialog(self)
			if dialog.exec():
				timer = dialog.get_timer()
				
				# Ajoute le timer à la liste
				self.add_timer(timer)
		
		# Mode modification s'il y a un timer fourni
		else:
			# Ouvre la fenêtre de modification et récupère le timer si l'utilisateur a validé
			dialog = TimerDialog(self, timer)
			if dialog.exec():
				# Modifie le timer existant, on a l'impression qu'il n'est pas utilisé,
				# mais il point bien vers le timer de la liste
				timer = dialog.get_timer()
				
				# Reset le timer pour mettre à jour les valeurs
				widget.reset_timer(modify=True)
	
	def check_timer(self):
		""" Passe sur les éléments de la liste pour mettre à jour les timers actifs """
		
		for widget in self.lst_timer.findChildren(TimerWidget):
			widget.update_timeleft()
		
	
	def closeEvent(self, event):
		""" Fermeture de la vue """
		# self.timer_notify.stop()
		# event.accept()
		
		# todo Sauvegarde et arrêt des timers actifs
		pass
	##
	
	#
#



