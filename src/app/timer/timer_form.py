
# -*- coding: utf-8 -*-
# Permet d'utiliser les accents dans le code

"""
		## Formulaire de création de timer ##

Created :
	dimanche 31 mars 2024 8:45:49
Started :

Last updated :
	lundi 1 avril 2024 12:28:49
	
"""
from datetime import timedelta

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QHBoxLayout, QSpinBox, QPushButton, QLabel

from app.timer.timer import Timer

from app.timer.config import MAX_CHAR_NAME, MAX_CHAR_MESSAGE


class TimerForm(QWidget):
	
	submitted = Signal(Timer)
	
	def __init__(self):
		super().__init__()
		
		self.set_variables()
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
	
	def set_variables(self):
		""" Définition des variables """
		pass
	##
	
	def setup_ui(self):
		""" Configuration de l'interface du widget """
		
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
		self.le_name_timer.setPlaceholderText("Nom du timer")
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
		
		#
		# ---   Layout SpinBox --- #
		self.hlayout_spn = QHBoxLayout()
		self.vlayout.addLayout(self.hlayout_spn)
		
		# Heures
		self.spn_hours = QSpinBox()
		self.spn_hours.setSuffix(" Hours")
		self.spn_hours.setMaximum(24)
		self.hlayout_spn.addWidget(self.spn_hours)
		
		# Minutes
		self.spn_minutes = QSpinBox()
		self.spn_minutes.setSuffix(" minutes")
		self.spn_minutes.setMaximum(60)
		self.hlayout_spn.addWidget(self.spn_minutes)
		
		# Secondes
		self.spn_seconds = QSpinBox()
		self.spn_seconds.setSuffix(" Seconds")
		self.spn_seconds.setMaximum(60)
		self.spn_seconds.setSingleStep(5)
		self.hlayout_spn.addWidget(self.spn_seconds)
		
		# Bouton de création de timer
		self.btn_new = QPushButton("New Timer")
		self.btn_new.setEnabled(False)
		self.vlayout.addWidget(self.btn_new)
		
		self.lb_result = QLabel("")
		self.vlayout.addWidget(self.lb_result)
	
	#
	def set_style(self):
		"""  """
		self.vlayout.setContentsMargins(0, 0, 0, 0)
		self.vlayout.setSpacing(0)
		self.vlayout.addStretch(1)  # Ajoute un espace extensible à la fin du layout vertical
		
		self.hlayout.addStretch(1)
		
		self.lb_count_char_name.setAlignment(Qt.AlignRight)
		self.lb_count_char_message.setAlignment(Qt.AlignRight)
		
		self.setStyleSheet("""
			
			QLineEdit {
				border-radius: 5px;
			}
			
			QTextEdit {
				border-radius: 10px;
			}
			
			""")
	
	#
	def setup_connections(self):
		"""  """
		self.le_name_timer.textChanged.connect(lambda: self.count_char("name"))
		self.le_name_timer.returnPressed.connect(self.submit_form)
		
		self.te_content_timer.textChanged.connect(lambda: self.count_char("message"))
		
		self.spn_seconds.valueChanged.connect(self.check_spinbox_seconds)
		
		self.spn_seconds.valueChanged.connect(lambda: self.check_spinbox("seconds"))
		
		self.spn_minutes.valueChanged.connect(lambda: self.check_spinbox("minutes"))
		
		self.spn_hours.valueChanged.connect(lambda: self.check_spinbox("hours"))
		
		self.btn_new.clicked.connect(self.submit_form)
		pass
	
	#
	def set_default_values(self):
		""" Définition des valeurs par défaut """
		pass
	
	#
	def count_char(self, field: str):
		"""
		Calcule le nombre de caractères restants dans les champs
			> Lorsqu'ils sont modifiée.
		
		- Vérifie si le nombre de caractères dans les champs est correct.
		- Modification du texte et de sa couleur en fonction dela validité des champs.
		
		Args:
			field (str): Champ de texte qui doit être modifié.
		"""
		
		chars_left = 0  # Nombre de caractère restants
		max_char = 0    # Nombre de caractères maximum
		
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
		Permet de modifier les labels d'informations
			> Lorsqu'un champ de texte est modifié.
			
		- Modifie le texte et la couleur du label en fonction de la validité du champ associé.
		- Active le bouton de validation du formulaire si les champs sont valides.
		
		Args:
			active (bool): Si le champ est valide ou non.
			field (str): Champ de texte qui doit être modifié.
			text (str): Texte à afficher dans le label, contient le nombre de caractères restants.
		"""
		
		if field == "message":
			self.lb_count_char_message.setText(text)
			if active:
				self.activate_btn()
				self.lb_count_char_message.setStyleSheet("QLabel {color: #00a151;}")
			else:
				self.btn_new.setEnabled(False)
				self.lb_count_char_message.setStyleSheet("QLabel {color: #c5130d;}")
		
		elif field == "name":
			self.lb_count_char_name.setText(text)
			if active:
				self.activate_btn()
				self.lb_count_char_name.setStyleSheet("QLabel {color: #00a151;}")
			else:
				self.btn_new.setEnabled(False)
				self.lb_count_char_name.setStyleSheet("QLabel {color: #c5130d;}")
	
	def check_spinbox_seconds(self):
		""" Vérifie que le spinbox des secondes ne sorte pas de son pas de cinq """
		
		# Récupère la valeur du spinbox sous forme de str.
		value = str(self.spn_seconds.value())
		
		# Sépare les nombres de la valeur
		start_value = value[1] if len(value) == 2 else ""
		end_value = value[-1]
		
		if end_value not in "05 ":
			
			# Modifie le dernier chiffre de la valeur
			if end_value in "1289":
				end_value = "0"
			else:
				end_value = "5"
			
			# Modifie la valeur du spin box
			self.spn_seconds.setValue(int(start_value + end_value))
	
	def check_spinbox(self, spinbox: str):
		"""
		Vérification principale sur les spinbox
			> Lorsqu'un spin box est modifié.
			
		- Réinitialisation à zéro s'ils atteignent leur maximum et augmentation des autres spinbox
		- Activation du bouton de validation du formulaire
		
		Args:
			spinbox (str): Spinbox qui doit être vérifié.
		"""
		
		# Vérifie le spinbox en question
		if spinbox == "seconds":
			# Récupère la valeur du spin box
			value = self.spn_seconds.value()
			
			# Vérifie si la valeur est supérieur à celle autorisée
			if value == 60:
				# Récupère la valeur du spin box voisin et l'augmente de 1
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
		
		elif spinbox == "hours":
			# Pas d'augmentation du voisin ici
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
		s = self.spn_seconds.value()
		m = self.spn_minutes.value()
		h = self.spn_hours.value()
		
		# Vérifie si au moins un spinbox possède une valeur
		if not s and not m and not h:
			check = False
		
		# Si aucune vérification n'a echouer
		if check:
			# active le bouton de validation du formulaire et retourne True.
			self.btn_new.setEnabled(True)
		else:
			self.btn_new.setEnabled(False)
	##
	
	@property
	def duration(self):
		""" Récupère les valeurs des spin box et constuit une durée en secondes """
		s = self.spn_seconds.value()
		m = self.spn_minutes.value()
		h = self.spn_hours.value()
		
		return timedelta(hours=h, minutes=m, seconds=s).seconds
	##
	
	#
	def submit_form(self):
		""" Crée un timer avec els informations du formulaire et l'envoie
		- Cela est fait lors de l'appui sur le bouton avec un formulaire valide
		"""
		
		# Préparation des données à émettre
		title = self.le_name_timer.text()
		message = self.te_content_timer.toPlainText()
		duration = self.duration
		timer = Timer(title, message, duration)
		
		# Émettez le signal avec le timer
		self.submitted.emit(timer)
	##
	
	#
	def keyPressEvent(self, event):
		""" Permet de soumettre le formulaire avec la touche entrée """
		if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
			self.submit_form()
		else:
			super().keyPressEvent(event)