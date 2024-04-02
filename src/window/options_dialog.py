""" Fenêtre de configuration de l'application """

# ----  IMPORTS  ---- #

from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QVBoxLayout, QLabel, QPushButton, QCheckBox, QHBoxLayout

from utils import set_stylesheet, base_config

debug_on = True


class OptionDialog(QDialog):
	""" Fenêtre de configuration de l'application """
	
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.setWindowIcon(QIcon("lib/icons/opt.png"))
		self.setWindowTitle('Options')
		self.setModal(True)  # Rend la fenêtre modale (bloque le reste de l'application)
		
		# Récupère la fenêtre principale
		self.main_window = self.parent()
		
		self.setup_ui()
		self.setup_connections()
		self.set_default_values()
	
	def setup_ui(self):
		""" Configure l'interface graphique """
		# Create layout and add widgets
		self.layout = QVBoxLayout(self)
		
		self.lb_style = QLabel("Style:")
		self.layout.addWidget(self.lb_style)
		
		self.cbb_style = QComboBox()
		self.layout.addWidget(self.cbb_style)
		
		self.lb_sep = QLabel("    --------------------------------    ")
		self.layout.addWidget(self.lb_sep)
		
		# Option mémoriser la position et la taille de la fenêtre
		self.label_option_position = QLabel("Window position:")
		self.layout.addWidget(self.label_option_position)
		
		self.option_position_layout = QHBoxLayout()
		self.layout.addLayout(self.option_position_layout)
		
		self.cb_option_position = QCheckBox("Remember")
		self.cb_option_position.setToolTip("If checked, the window position is saved.")
		self.option_position_layout.addWidget(self.cb_option_position)
		
		self.btn_reset_pos = QPushButton("Reset")
		self.option_position_layout.addWidget(self.btn_reset_pos)
	
	def setup_connections(self):
		""" Connecte les signaux aux slots """
		self.cbb_style.textActivated.connect(self.set_style)
		
		self.cb_option_position.clicked.connect(self.set_option_position)
		
		self.btn_reset_pos.clicked.connect(self.reset_position)
	
	def set_default_values(self):
		""" Défini les valeurs par défaut des widgets """
		# Récupère les noms des fichiers qss pour les placer dans le cbb
		qss_dir = Path("lib/style").resolve()
		qss_files = [file.stem for file in qss_dir.iterdir() if file.suffix == ".qss"]
		self.cbb_style.addItem("Default")
		self.cbb_style.addItems(qss_files)
		self.cbb_style.setCurrentText(self.main_window.config['style'])
		
		# Active l'option de position en fonction de la config
		self.cb_option_position.setChecked(self.main_window.config['save_pos'])
	
	def set_option_position(self):
		""" Modifie l'option de sauvegarde de la position de la fenêtre """
		self.main_window.config["save_pos"] = self.cb_option_position.isChecked()
	
	def reset_position(self):
		""" Réinitialise la position de la fenêtre """
		# Doit redonner à la fenêtre et à la config les positions trouvées dans la config de base
		self.main_window.setGeometry(base_config["geox"], base_config["geoy"], base_config["geow"], base_config["geoh"])
		
		print("Position reseted", debug_on)
	
	def set_style(self):
		""" Applique le style sélectionné """
		style = self.cbb_style.currentText()
		if style == "Default":
			self.main_window.config['style'] = style
			self.main_window.setStyleSheet("")
			return
		self.main_window.config['style'] = style
		set_stylesheet(self.main_window, f"lib/style/{style}.qss")
	
	def closeEvent(self, arg__1):
		""" Ferme la fenêtre et sauvegarde la config """
		print("\n  🔧 Option closed\n", debug_on)

#

#