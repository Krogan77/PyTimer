
""" Settings window for application """


# ----  IMPORTS ---- #

from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QVBoxLayout, QLabel, QPushButton, QCheckBox, QHBoxLayout

from utils import set_stylesheet, base_config


class SettingsDialog(QDialog):
	""" Application configuration window """
	
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.setWindowIcon(QIcon("lib/icons/opt.png"))
		self.setWindowTitle('Settings')
		self.setModal(True) # Makes the window modal (blocks the rest of the application)
		
		# Recovers the main window
		self.main_window = self.parent()
		
		self.setup_ui()
		self.setup_connections()
		self.set_default_values()
	
	def setup_ui(self):
		""" Configures the graphical interface """
		# Create layout and add widgets
		self.layout = QVBoxLayout(self)
		
		self.lb_style = QLabel("Style:")
		self.layout.addWidget(self.lb_style)
		
		self.cbb_style = QComboBox()
		self.layout.addWidget(self.cbb_style)
		
		self.lb_sep = QLabel("    --------------------------------    ")
		self.layout.addWidget(self.lb_sep)
		
		# Save window position and size option
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
		""" Connects signals to slots """
		self.cbb_style.textActivated.connect(self.set_style)
		
		self.cb_option_position.clicked.connect(self.set_option_position)
		
		self.btn_reset_pos.clicked.connect(self.reset_position)
	
	def set_default_values(self):
		""" Set default values for widgets. """
		# Gets qss file names and places them in the cbb
		qss_dir = Path("lib/style").resolve()
		qss_files = [file.stem for file in qss_dir.iterdir() if file.suffix == ".qss"]
		self.cbb_style.addItem("Default")
		self.cbb_style.addItems(qss_files)
		self.cbb_style.setCurrentText(self.main_window.config['style'])
		
		# Activates position option according to config
		self.cb_option_position.setChecked(self.main_window.config['save_pos'])
	
	def set_option_position(self):
		""" Modifies the option to save the position of the window. """
		self.main_window.config["save_pos"] = self.cb_option_position.isChecked()
	
	def reset_position(self):
		""" Resets the position of the window. """
		# Must restore window and config to positions found in base config
		self.main_window.setGeometry(base_config["geox"], base_config["geoy"], base_config["geow"], base_config["geoh"])
	
	def set_style(self):
		""" """
		style = self.cbb_style.currentText()
		if style == "Default":
			self.main_window.config['style'] = style
			self.main_window.setStyleSheet("")
			return
		self.main_window.config['style'] = style
		set_stylesheet(self.main_window, f"lib/style/{style}.qss")
