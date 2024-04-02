

""" Fenêtre principale de l'application """

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QVBoxLayout, QWidget

from utils import check_work_path, create_log_file, dbg
from window.options_dialog import OptionDialog
from app.timer.timer_view import TimerView


class MainWindow(QMainWindow):
	""" Fenêtre principale de l'application """
	
	def __init__(self):
		super().__init__()
		
		self.setWindowTitle('PyTimer')
		self.setMinimumSize(390, 370)
		
		# Vérifie l'emplacement de l'application pour différencier les icônes
		if check_work_path():
			self.setWindowIcon(QIcon("lib/icons/icon_work.png"))
		else:
			self.setWindowIcon(QIcon("lib/icons/main_icon.png"))
			
		create_log_file()
		
		# Récupère la sauvegarde et configure les options
		self.set_options()
		
		# Création de l'icône de la barre système
		self.create_tray_icon()
		
		self.set_variables()
		self.setup_ui()
		self.setup_connections()
		self.set_default_values()
		
		self.central.setStyleSheet("""
					* {
					font-weight: 600;
					}
					""")
	
	def set_variables(self):
		""" Définition des variables de l'application """
		self.options_dialog = OptionDialog(parent=self)
		
		pass
		
	def setup_ui(self):
		""" Création de l'interface graphique """
		
		# Menu Bar
		self.create_menu_bar()
		
		self.central = QWidget()
		self.setCentralWidget(self.central)
		
		self.layout = QVBoxLayout()
		self.central.setLayout(self.layout)
		
		self.timer_view = TimerView()
		self.layout.addWidget(self.timer_view)
		
		pass
	
	def create_menu_bar(self):
		""" Création de la barre de menu """
		
		# Menu Bar
		self.menu_bar = self.menuBar()
		
		# Menu File
		self.menu_file = self.menu_bar.addMenu("File")
		self.act_close = self.menu_file.addAction("Exit")
		
		# Menu Options
		self.act_options = self.menu_bar.addAction("Options")
		self.act_options.setIcon(QIcon("lib/icons/opt.png"))
	
	#
	def setup_connections(self):
		""" Définition des connexions entre les widgets """
		self.act_options.triggered.connect(self.open_options)
		
		self.act_close.triggered.connect(self.close)
		
		self.tray.activated.connect(self.toggle_window)
		pass
	
	#
	def set_default_values(self):
		""" Définition des valeurs par défaut des widgets """
		pass
	
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
	
	def open_options(self):
		""" Ouvre la fenêtre des options """
		self.options_dialog.show()
		
	def create_tray_icon(self):
		""" Création de l'icône système """
		self.tray = QSystemTrayIcon()
		try:
			self.tray.setIcon(QIcon("lib/icons/main_icon.png"))
			self.tray.setVisible(True)
		except Exception:
			dbg("Impossible de charger l'icône système.")
	
	def toggle_window(self):
		""" Affiche ou cache la fenêtre """
		self.hide() if self.isVisible() else self.showNormal()
	
	def btn_clicked(self):
		""" Active les notifications """
		pass
		
	
	#
	def closeEvent(self, event):
		""" Fermeture de l'application """
		
		from utils import save_config_backup
		
		if self.config["save_pos"]:
			self.config["geox"], self.config["geoy"] = self.pos().x(), self.pos().y()
			self.config["geow"], self.config["geoh"] = self.width(), self.height()
		
		save_config_backup(self.config)
		
		pass
	#

#