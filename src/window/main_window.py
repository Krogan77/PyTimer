

""" Fenêtre principale de l'application """
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QVBoxLayout, QWidget, QApplication

from utils import check_work_path, dbg, save_config_backup
from window.settings_dialog import SettingsDialog
from app.timer.timer_view import TimerView

# Vérifie l'emplacement de l'application pour différencier les icônes
if check_work_path():
	window_icon = "icon_work"
else:
	window_icon = "main_icon"


class InvisibleParent(QWidget):
	def __init__(self):
		super().__init__()
		
		# Mettre le parent en tant qu'outil pour qu'il n'apparaisse pas dans la barre des tâches
		self.setWindowFlags(Qt.Tool)
	##
##


#
class MainWindow(QMainWindow):
	""" Fenêtre principale de l'application """
	
	#
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.setWindowTitle('PyTimer')
		self.setMinimumSize(450, 288)
		
		# create_log_file()
			
		self.setWindowIcon(QIcon(f"lib/icons/{window_icon}.png"))
		
		# Récupère la sauvegarde et configure les options
		self.set_options()
		
		# Création de l'icône de la barre système
		self.create_tray_icon()
		
		# Création des éléments de l'interface
		self.set_variables()
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
	##
	
	#
	def set_variables(self):
		""" Définition des variables de l'application """
		self.options_dialog = SettingsDialog(parent=self)
		
		pass
	##
	
	#
	def setup_ui(self):
		""" Création de l'interface graphique """
		
		# Menu Bar
		self.create_menu_bar()
		
		self.central = QWidget()
		self.setCentralWidget(self.central)
		
		self.layout = QVBoxLayout()
		self.central.setLayout(self.layout)
		
		self.timer_view = TimerView(main_window=self)
		self.layout.addWidget(self.timer_view)
		
		pass
	##
	
	#
	def set_style(self):
		""" Modification du style """

		self.central.setStyleSheet("""
					* {
					font-weight: 600;
					}
					""")
	##
	
	#
	def create_menu_bar(self):
		""" Création de la barre de menu """
		
		# Menu Bar
		self.menu_bar = self.menuBar()
		
		# Menu File
		self.menu_file = self.menu_bar.addMenu("File")
		self.act_close = self.menu_file.addAction("Exit")
		
		# Menu Options
		self.act_options = self.menu_file.addAction("Options")
		self.act_options.setIcon(QIcon("lib/icons/opt.png"))
	##
	
	#
	def setup_connections(self):
		""" Définition des connexions entre les widgets """
		self.act_options.triggered.connect(self.open_options)
		
		self.act_close.triggered.connect(self.close)
		
		self.tray.activated.connect(self.toggle_window)
	##
	
	#
	def set_default_values(self):
		""" Définition des valeurs par défaut des widgets """
		pass
	##
	
	#
	def set_options(self):
		""" Récupère et applique les options depuis le fichier de sauvegarde """
		from utils import check_config_backup, get_config_backup, set_stylesheet
		
		check_config_backup()
		
		# Récupère les options depuis le fichier de sauvegarde
		self.config = get_config_backup()
		
		self.config["geoy"] += 30
		
		self.setGeometry(self.config["geox"], self.config["geoy"], self.config["geow"], self.config["geoh"])
		
		# Application du style CSS
		set_stylesheet(self, f"lib/style/{self.config['style']}.qss")
	##
	
	#
	def open_options(self):
		""" Ouvre la fenêtre des options """
		self.options_dialog.show()
	##
	
	#
	def create_tray_icon(self):
		""" Création de l'icône système """
		self.tray = QSystemTrayIcon()
		try:
			self.tray.setIcon(QIcon(f"lib/icons/{window_icon}.png"))
			self.tray.setVisible(True)
			
			# Déclenche un message de notification lors de la création de l'icône
			# self.tray.showMessage("MyApp is running!", "Click to open window\nRight click for menu")
		except Exception:
			dbg("Impossible de charger l'icône système.")
	##
	
	#
	def toggle_window(self):
		""" Affiche ou cache la fenêtre """
		if self.isVisible():
			self.setVisible(False)
		else:
			self.setVisible(True)
			self.activateWindow()
			
		if self.isMinimized():
			self.setVisible(True)
			self.activateWindow()
	##
	
	#
	# def changeEvent(self, event):
	# 	if event.type() == QEvent.WindowStateChange:
	# 		if self.isMinimized():
	# 			self.setVisible(False)
	# 			event.ignore()  # Ignore l'événement de minimisation
	# 		else:
	# 			super().changeEvent(event)
	##
	
	#
	def closeEvent(self, event):
		""" Fermeture de l'application """
		
		# Fermeture de la vue des timers
		self.timer_view.close()
		
		if self.config["save_pos"]:
			self.config["geox"], self.config["geoy"] = self.pos().x(), self.pos().y()
			self.config["geow"], self.config["geoh"] = self.width(), self.height()
		
		save_config_backup(self.config)
		
		
		# Fermeture de la fenêtre parente
		QApplication.quit()
		
		pass
	##
##