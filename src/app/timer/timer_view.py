
# -*- coding: utf-8 -*-
# Permet d'utiliser les accents dans le code

"""

    $ -- TimerView -- $

Description :
    Vue des timers

Notes :
	- Permet de gérer les timers

Fonctionnalités :
	- Création et modification des timers
	- Affichage des timers
	


Todo Doc.
#

Todo:
	> Sauvegarde des timers
	- Création d'un fichier de sauvegardeet d'une liste
	- Charger les timers existants lors de l'ouverture et les ajouter dans la liste
	- passer sur les timer de la liste lors de la fermeture pour les sauvegarder
	-
	> Ajout de temps restant
	-
	> Multiple notifications pour un seul timer
	.
	
"""



from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QPushButton

from app.timer.timer_dialog import TimerDialog

from app.timer.timer_widget import TimerWidget


class TimerView(QWidget):
	""" Gestion de la vue des timers """
	def __init__(self):
		super().__init__()
		
		# Création des éléments de l'interface
		self.set_variables()
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
	##
	
	#
	def set_variables(self):
		""" Définition des variables de la vue """
		pass
	##
	
	#
	def setup_ui(self):
		""" Création des éléments de l'interface """
		
		self.vlayout = QVBoxLayout()
		self.setLayout(self.vlayout)
		
		# Bouton de création de timer
		self.btn_new_timer = QPushButton("Nouveau")
		self.btn_new_timer.setFixedWidth(150)
		self.vlayout.addWidget(self.btn_new_timer)
		
		# Liste des timers
		self.lst_timer = QListWidget()
		self.lst_timer.setMinimumWidth(400)
		self.vlayout.addWidget(self.lst_timer)
	##
	
	#
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
	##
	
	#
	def set_default_values(self):
		""" Définition des valeurs par défaut """
		
		# todo chargement des timers existants
		
		# Timer servant à rafraîchir les timers actifs
		# et déclencher les notifications des minuteurs
		self.timer_refresh = QTimer()
		self.timer_refresh.timeout.connect(self.check_timer)
		self.timer_refresh.start(20)  # Vérifie toutes les 20 ms
	##
	
	#
	def add_timer(self, timer):
		"""
		Création d'un nouveau timer !
			> Déclenchée par le signal du formulaire
		
		- Récupère le timer fourni par le formulaire.
		- Crée le widget pour le timer pour l'insérer dans la liste.
		- Connecte le signal du bouton de modification vers la méthode correspondante.
		- Place le timer dans son widget et l'ajoute à la liste.
		
		:param timer: Timer
		"""
		
		# Création du widget
		self.item = QListWidgetItem()
		self.timer_widget = TimerWidget(parent=self, timer=timer)
		
		# Connexion du signal de modification
		self.timer_widget.submit_timer.connect(self.create_timer)
		
		# Ajout du widget à la liste
		self.item.setSizeHint(self.timer_widget.sizeHint())
		self.lst_timer.addItem(self.item)
		self.lst_timer.setItemWidget(self.item, self.timer_widget)
		
	
	def create_timer(self, timer=None, widget=None):
		""" Création d'un nouveau timer
			> Déclenchée par le bouton de création de la vue
			> ainsi que le bouton de modification des timers
			
			- Si aucun timer n'est fourni, on ouvre le formulaire de création.
			- Si un timer est fourni par le bouton de modification, on ouvre le formulaire
			  en fournissant les informations du timer.
			- Ajoute ou modifie le timer existant dans la liste si l'utilisateur a validé le formulaire.
		"""
		
		# Mode création s'il n'y a pas de timer fourni
		if not timer:
			
			# Ouvre la fenêtre de création et récupère le timer si l'utilisateur a validé
			dialog = TimerDialog(self)
			if dialog.exec():
				timer = dialog.get_timer()
				
				# Ajoute le timer à la liste
				self.add_timer(timer)
		
		# Mode modification
		else:
			
			# Ouvre la fenêtre de modification et récupère le timer si l'utilisateur a validé
			dialog = TimerDialog(self, timer)
			if dialog.exec():
				
				# Modifie le timer existant,
				timer = dialog.get_timer()
				# on a l'impression qu'il n'est pas utilisé, mais il pointe bien vers le timer de la liste
				
				# Reset le timer pour mettre à jour les valeurs
				widget.reset_timer(check_duration=True)
	
	def check_timer(self):
		""" Mis à jour des timers actifs
			> Déclenchée par le timer de rafraîchissement
			
			- Parcours tous les widgets de la liste pour mettre à jour le temps restant.
			- Toute la logique se fait dans les widgets de timers et dans les timers eux-mêmes.
		"""
		
		# Parcours des widgets pour mettre à jour les timers
		for widget in self.lst_timer.findChildren(TimerWidget):
			widget.update_timeleft()
		
	
	def closeEvent(self, event):
		""" Fermeture de la vue """
		
		# todo Arrêt et sauvegarde des timers actifs
		pass
	##
	
	#
#