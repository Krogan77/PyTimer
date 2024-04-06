# -*- coding: utf-8 -*-
# Permet d'utiliser les accents dans le code


""" Classe TimerDialog

Permet la création et la modification d'un mminuteur.
"""

# Imports :
from datetime import timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QSpinBox, \
	QDialogButtonBox

from app.timer.config import MAX_CHAR_NAME, MAX_CHAR_MESSAGE, MAX_RINGS, MAX_INTERVAL
from app.timer.timer import Timer
from src.utils import dbg


class TimerDialog(QDialog):
	""" Classe TimerDialog

	Permet la création et la modification d'un mminuteur.
	"""
	def __init__(self, parent=None, timer=None):
		super().__init__(parent)
		self.timer = timer
		self.parent = parent
		
		# Set le titre de la fenêtre avec le mode qui
		# sera vérifié plus tard pour savoir si on doit renvoyer le timer fourni
		self.window_title = "Création"
		self.setWindowTitle(self.window_title)
		
		# Création des éléments de l'interface
		# self.create_variables()
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
	##
	
	#
	def create_variables(self):
		""" Définition des variables """
		pass
	##
	
	#
	def setup_ui(self):
		""" Configuration de l'interface """
		
		self.hlayout = QHBoxLayout()
		self.setLayout(self.hlayout)
		
		# Layout principale
		self.vlayout = QVBoxLayout()
		self.hlayout.addLayout(self.vlayout)
		
		# Compteur de caractère du line edit
		self.lb_count_char_name = QLabel(f"{MAX_CHAR_NAME} caractères restants")
		self.vlayout.addWidget(self.lb_count_char_name)
		
		# Line edit
		self.le_name_timer = QLineEdit()
		self.le_name_timer.setPlaceholderText("Nom du minuteur")
		self.vlayout.addWidget(self.le_name_timer)
		
		# Compteur de caractères du text edit
		self.lb_count_char_message = QLabel(f"{MAX_CHAR_MESSAGE} caractères restants.")
		self.vlayout.addWidget(self.lb_count_char_message)
		
		# Text edit
		self.te_content_timer = QTextEdit()
		placeholder_text = "Message de notification"
		placeholder_text += "\nLaissez vide pour ne pas déclencher de notification"
		self.te_content_timer.setPlaceholderText(placeholder_text)
		self.vlayout.addWidget(self.te_content_timer)
		
		self.lb_times = QLabel("Durée du minuteur :")
		self.vlayout.addWidget(self.lb_times)
		
		#
		# ---   Layout SpinBox --- #
		self.hlayout_spn = QHBoxLayout()
		self.vlayout.addLayout(self.hlayout_spn)
		
		# Heures
		self.spn_hours = QSpinBox()
		self.spn_hours.setSuffix(" hours")
		self.spn_hours.setMaximum(24)
		self.hlayout_spn.addWidget(self.spn_hours)
		
		# Minutes
		self.spn_minutes = QSpinBox()
		self.spn_minutes.setSuffix(" minutes")
		self.spn_minutes.setMaximum(60)
		self.hlayout_spn.addWidget(self.spn_minutes)
		
		# Secondes
		self.spn_seconds = QSpinBox()
		self.spn_seconds.setSuffix(" seconds")
		self.spn_seconds.setMaximum(60)
		self.spn_seconds.setSingleStep(5)
		self.hlayout_spn.addWidget(self.spn_seconds)
		
		# Nombre de sonneries
		self.lb_number_rings = QLabel("Sonneries supplémentaire :")
		self.vlayout.addWidget(self.lb_number_rings)
		
		self.hlayout_number_rings = QHBoxLayout()
		self.vlayout.addLayout(self.hlayout_number_rings)
		
		# Nombre de sonneries supplémentaires
		self.spn_rings = QSpinBox()
		self.spn_rings.setSuffix(f" /{MAX_RINGS}")
		self.spn_rings.setMaximum(MAX_RINGS)
		self.hlayout_number_rings.addWidget(self.spn_rings)
		
		self.lb_times_rings = QLabel(" toutes les ")
		self.hlayout_number_rings.addWidget(self.lb_times_rings)
		
		# Temps entre les sonneries
		self.spn_interval = QSpinBox()
		self.spn_interval.setSuffix(f"s /{MAX_INTERVAL}")
		self.spn_interval.setMaximum(MAX_INTERVAL)
		self.spn_interval.setSingleStep(15)
		self.hlayout_number_rings.addWidget(self.spn_interval)
		
		# Boite de bouton de validation
		self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
		self.vlayout.addWidget(self.button_box)
	##
	
	#
	def set_style(self):
		""" Modification du style """
		
		# Aligne les labels sur la droite
		self.lb_count_char_name.setAlignment(Qt.AlignRight)
		self.lb_count_char_message.setAlignment(Qt.AlignRight)
		
		self.setStyleSheet(
			"""
				* {
					font-size: 13px;
				}
				
				QLineEdit {
					border-radius: 5px;
				}
				
				QTextEdit {
					border-radius: 5px;
					border: 2px solid black;
				}
				
				QDialogButtonBox > QPushButton {
					margin-right: 10px;
					margin-top: 8px;
					margin-bottom: 2px;
				}
				""")
	##
	
	#
	def setup_connections(self):
		""" Création des connecions entre les widgets """
		
		self.le_name_timer.textChanged.connect(lambda: self.count_char("name"))
		
		self.te_content_timer.textChanged.connect(lambda: self.count_char("message"))
		
		self.spn_seconds.valueChanged.connect(self.check_spinbox_seconds)
		
		self.spn_seconds.valueChanged.connect(lambda: self.check_spinbox("seconds"))
		
		self.spn_minutes.valueChanged.connect(lambda: self.check_spinbox("minutes"))
		
		self.spn_hours.valueChanged.connect(lambda: self.check_spinbox("hours"))
		
		self.spn_rings.valueChanged.connect(self.check_number_rings)
		
		self.spn_interval.valueChanged.connect(lambda: self.correct_value(self.spn_interval))
		self.spn_interval.valueChanged.connect(self.check_remaining)
		
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)
		pass
	##
	
	#
	def set_default_values(self):
		""" Définition des valeurs par défaut """
		
		# Si un timer est fourni
		if self.timer:
			
			# Change le mode de la fenêtre pour savoir ensuite
			# que l'on doit modifier le timer fourni et non en créer un nouveau
			self.setWindowTitle("Modification")
			
			# Ajoute les informations du timer dans les champs
			self.le_name_timer.setText(self.timer.title)
			self.te_content_timer.setPlainText(self.timer.message)
			self.spn_hours.setValue(self.timer.hours)
			self.spn_minutes.setValue(self.timer.minutes)
			self.spn_seconds.setValue(self.timer.seconds)
			self.spn_rings.setValue(self.timer.number_rings)
			self.spn_interval.setValue(self.timer.interval)
	##
	
	#
	def count_char(self, field: str):
		"""
		Calcule le nombre de caractères restants dans les champs
			> Lorsqu'ils sont modifiée.

		- Vérifie si le nombre de caractères dans les champs est correct.
		- Modification du texte et de sa couleur en fonction de la validité
			des champs à l'aide d'une fonction complémentaire.

		Args:
			field (str): Champ de texte qui doit être modifié.
		"""
		
		chars_left = 0  # Nombre de caractère restants
		max_char = 0  # Nombre de caractères maximum
		
		# Récupère le contenu dans le champ demandé
		# et set le nombre de caractères maximum
		if field == "message":
			# Contenue du text edit
			content = self.te_content_timer.toPlainText()
			max_char = MAX_CHAR_MESSAGE
			chars_left = max_char - len(content)
			
			# Augmente le max pour permettre d'autoriser un message vide pour la notification
			# Cela fera en sorte que le bouton et la couleur soit affiché correctement d'un seul coup.
			if chars_left == max_char:
				max_char += 1
		
		elif field == "name":
			# Contenue du line edit
			content = self.le_name_timer.text()
			max_char = MAX_CHAR_NAME
			chars_left = max_char - len(content)
		
		# Text de remplacement
		text = str(chars_left) + " caractères restants."
		
		# Active le bouton si le nombre de caractères est correct.
		if -1 < chars_left < max_char:
			self.modify_label_chars(True, field, text)
		else:
			self.modify_label_chars(False, field, text)
	
	##
	
	#
	def modify_label_chars(self, active: bool, field: str, text: str = ""):
		"""
		Permet de modifier les labels d'informations et d'activer le bouton de validation si les champs sont valides.
			> Lorsqu'un champ de texte est modifié.

		- Modifie le texte et la couleur du label en fonction de la validité du champ associé.
		- Active le bouton de validation du formulaire si les champs sont valides.

		Args:
			- active (bool): Si le champ est valide ou non.
			- field (str): Champ de texte qui doit être modifié.
			- text (str): Texte à afficher dans le label, contient le nombre de caractères restants.
		"""
		
		# Champ du message de notification
		if field == "message":
			
			# Modifie le texte du label avec le nombre de caractères restants
			self.lb_count_char_message.setText(text)
			
			# Si le champ est valide,
			if active:
				# active le bouton et change la couleur du texte en vert
				self.activate_btn()
				self.lb_count_char_message.setStyleSheet("QLabel {color: #00a151;}")
			else:
				# Sinon, désactive le bouton et change la couleur du texte en rouge
				self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
				self.lb_count_char_message.setStyleSheet("QLabel {color: #c5130d;}")
		
		# Champ du nom du minuteur
		# Logique identique à celle du champ message
		elif field == "name":
			self.lb_count_char_name.setText(text)
			if active:
				self.activate_btn()
				self.lb_count_char_name.setStyleSheet("QLabel {color: #00a151;}")
			else:
				self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
				self.lb_count_char_name.setStyleSheet("QLabel {color: #c5130d;}")
	
	def check_spinbox_seconds(self):
		""" Vérifie la valeur du spinbox des secondes et la modifie si elle est incorrecte
			> Lorsque le spinbox des secondes est modifié.
		
			- Force le dernier chiffre à être un multiple de 5.
		"""
		
		# Récupère la valeur du spinbox
		value = str(self.spn_seconds.value())
		
		# Sépare les nombres de la valeur
		start_value = value[1] if len(value) == 2 else ""
		end_value = value[-1]
		
		if end_value not in "05 ":
			
			# Modifie le dernier chiffre pour qu'il soit un multiple de 5.
			if end_value in "1289":
				end_value = "0"
			else:
				end_value = "5"
			
			# Modification du spin box
			self.spn_seconds.setValue(int(start_value + end_value))
	
	@staticmethod
	def correct_value(obj):
		""" Corrige la valeur du spinbox pour qu'elle soit un multiple de 15 """
		value = obj.value()
		step = obj.singleStep()
		corrected_value = (value // step) * step
		if value % step != 0:
			obj.setValue(corrected_value)
	
	#
	def check_remaining(self):
		""" Vérifie la valeur du spinbox du temps entre les sonneries
				> Lorsqu'il est modifié
		"""
		# Vérification du nombre de sonneries
		# Cela empêche d'augmenter le temps entre les sonneries si le nombre de sonneries est zéro
		self.check_number_rings()
		
		# Si le temps entre les sonneries est zéro et le nombre de sonneries est différent de zéro
		if self.spn_interval.value() == 0 and self.spn_rings.value() != 0:
			# On force le temps entre les sonneries à être de 15 secondes
			# cela empêche le temps restant d'atteindre zéro si le nombre de sonneries est différent de zéro
			self.spn_interval.setValue(15)
	##
	
	#
	def check_number_rings(self):
		"""
			Vérifie le spin box du nombre de sonneries
				> Lorsqu'il est modifié ou que le temps entre les sonneries est modifié
		"""
		
		# Vérifie si le nombre de sonneries est zéro
		if self.spn_rings.value() == 0:
			# Force le spin box du temps entre les sonneries à zéro
			self.spn_interval.setValue(0)
		else:
			# Si le nombre de sonneries est différent de zéro, le temps entre les sonneries ne peut pas l'être
			if self.spn_interval.value() == 0:
				self.spn_interval.setValue(15)
	##
	
	#
	def check_spinbox(self, spinbox: str):
		"""
		Vérification principale sur les spinbox afin d'activer le bouton de validation du formulaire.
			> Lorsqu'un spin box est modifié.

		- Réinitialisation à zéro s'ils atteignent leur maximum et augmentation des autres spinbox.
		- Activation du bouton si les champs sont valides.

		Args:
			spinbox (str): Spinbox qui doit être vérifié.
		"""
		
		# Vérifie le spinbox en question
		if spinbox == "seconds":
			# Récupère la valeur du spin box
			value = self.spn_seconds.value()
			
			# Vérifie si la valeur est supérieur à celle autorisée
			if value == 60:
				# Récupère la valeur du spin box voisin et l'incrémente.
				minutes = self.spn_minutes.value()
				minutes += 1
				
				# Réinitialise la valeur du spin box à zéro.
				self.spn_seconds.setValue(0)
				self.spn_minutes.setValue(minutes)
		
		# Même chose pour les autres spinbox
		elif spinbox == "minutes":
			value = self.spn_minutes.value()
			if value == 60:
				hours = self.spn_hours.value()
				hours += 1
				self.spn_hours.setValue(hours)
				self.spn_minutes.setValue(0)
		
		# Sans augmenter les autres spinbox pour celui la
		elif spinbox == "hours":
			value = self.spn_hours.value()
			if value == 24:
				self.spn_hours.setValue(0)
		
		# Activation du bouton de validation du formulaire
		self.activate_btn()
	
	def activate_btn(self):
		""" Effectue des vérifications et active le bouton seulement si ces dernières sont toutes passée """
		
		# Permet de savoir si une vérification à echouer, défini à true pour commencer,
		# s'il devient false avant la fin des vérifications, le bouton ne sera pas activer.
		check = True
		
		# Check line edit
		text = self.le_name_timer.text()
		if not 0 < len(text) <= MAX_CHAR_NAME:
			check = False
		
		# Check text edit
		text = self.te_content_timer.toPlainText()
		if not len(text) < MAX_CHAR_MESSAGE + 1:
			check = False
			
		# Check spinbox
		seconds = self.spn_seconds.value()
		minutes = self.spn_minutes.value()
		hours = self.spn_hours.value()
		
		# Vérifie si au moins un spinbox possède une valeur
		if not seconds and not minutes and not hours:
			check = False
		
		# Si aucune vérification n'a echouer
		if check:
			# active le bouton de validation du formulaire et retourne True.
			self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
		else:
			self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
	
	@property
	def spn_duration(self):
		""" Récupère les valeurs des spin box et constuit une durée en secondes """
		seconds = self.spn_seconds.value()
		minutes = self.spn_minutes.value()
		hours = self.spn_hours.value()
		return timedelta(hours=hours, minutes=minutes, seconds=seconds).seconds
	##
	
	#
	def accept(self):
		""" Crée un timer avec les informations du formulaire et l'envoie.
			> lors de l'appui sur le bouton et après vérification du formulaire.
		"""
		
		# Récupération des informations du formulaire
		title = self.le_name_timer.text()
		message = self.te_content_timer.toPlainText()
		duration = self.spn_duration
		number_rings = self.spn_rings.value()
		interval = self.spn_interval.value()
		
		# Si la fenêtre est en mode de création
		if self.windowTitle() == "Création":
			# On crée un timer avec les informations récupérées
			self.timer = Timer(title, message, duration, number_rings=number_rings, interval=interval)
		
		# Si la fenêtre est en mode de modification
		else:
			# On modifie le timer fourni
			self.timer.title = title
			self.timer.message = message
			self.timer.timer = self.spn_duration
			self.timer.number_rings = number_rings
			self.timer.check_number_rings()
			self.timer.interval = interval
			self.timer.check_times_between_rings()
			
		# Accepte le formulaire et le ferme
		super().accept()
	
	def reject(self):
		""" Ferme le formulaire sans rien faire """
		super().reject()
	
	def get_timer(self):
		""" Fonction permettant de récupérer le timer après la fermeture du formulaire """
		return self.timer
	##
	
	#
	def keyPressEvent(self, event):
		""" Permet de soumettre le formulaire avec la touche entrée """
		if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
			# Vérifie si le bouton est activé avant de soumettre le formulaire
			if self.button_box.button(QDialogButtonBox.Ok).isEnabled():
				self.accept()
		else:
			super().keyPressEvent(event)
	