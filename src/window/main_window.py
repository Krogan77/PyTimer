

""" Main window of the application """

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QVBoxLayout, QWidget, QApplication

from utils import check_work_path, dbg, save_config_backup
from window.settings_dialog import SettingsDialog
from app.timer.timer_view import TimerView

# Check application location to differentiate icons
if check_work_path():
	window_icon = "icon_work"
else:
	window_icon = "main_icon"


class InvisibleParent(QWidget):
	def __init__(self):
		super().__init__()
		
		# Set the parent as a tool so that it does not appear in the taskbar
		self.setWindowFlags(Qt.Tool)
	##
##


#
class MainWindow(QMainWindow):
	""" Main window of the application """
	
	#
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.setWindowTitle('PyTimer')
		self.setMinimumSize(450, 300)
		
		# create_log_file()
			
		self.setWindowIcon(QIcon(f"lib/icons/{window_icon}.png"))
		
		# Recovers backup and configures options
		self.settings()
		
		# Creating the system tray icon
		self.create_tray_icon()
		
		# Creating interface elements
		self.set_variables()
		self.setup_ui()
		self.set_style()
		self.setup_connections()
		self.set_default_values()
	##
	
	#
	def set_variables(self):
		""" Defining variables for the application """
		self.options_dialog = SettingsDialog(parent=self)
		
		pass
	##
	
	#
	def setup_ui(self):
		""" Creating the graphical interface """
		
		# Bar menu
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
		""" Modifying the style """

		self.central.setStyleSheet("""
					* {
					font-weight: 600;
					}
					""")
	##
	
	#
	def create_menu_bar(self):
		""" Creating the menu bar """
		
		# Bar menu
		self.menu_bar = self.menuBar()
		
		# File menu
		self.menu_file = self.menu_bar.addMenu("File")
		self.act_close = self.menu_file.addAction("Exit")
		
		# Options menu
		self.act_options = self.menu_file.addAction("Settings")
		self.act_options.setIcon(QIcon("lib/icons/opt.png"))
	##
	
	#
	def setup_connections(self):
		""" Defining connections between widgets"""
		self.act_options.triggered.connect(self.open_settings)
		
		self.act_close.triggered.connect(self.close)
		
		self.tray.activated.connect(self.toggle_window)
	##
	
	#
	def set_default_values(self):
		""" """
		pass
	##
	
	#
	def settings(self):
		""" Retrieves and applies options from the backup file. """
		from utils import check_config_backup, get_config_backup, set_stylesheet
		
		check_config_backup()
		
		# Recovers options from backup file
		self.config = get_config_backup()
		
		self.config["geoy"] += 30
		
		self.setGeometry(self.config["geox"], self.config["geoy"], self.config["geow"], self.config["geoh"])
		
		# Applying CSS styling
		set_stylesheet(self, f"lib/style/{self.config['style']}.qss")
	##
	
	#
	def open_settings(self):
		""" Opens the options window """
		self.options_dialog.show()
	##
	
	#
	def create_tray_icon(self):
		""" Creating the system icon """
		self.tray = QSystemTrayIcon()
		try:
			self.tray.setIcon(QIcon(f"lib/icons/{window_icon}.png"))
			self.tray.setVisible(True)
			
		# Trigger a notification message when the icon is not created
		except Exception:
			dbg("Unable to load system icon.")
	##
	
	#
	def toggle_window(self):
		""" Shows or hides the window """
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
	def closeEvent(self, event):
		""" Closing the application """
		
		# Closing the timer view
		self.timer_view.close()
		
		if self.config["save_pos"]:
			self.config["geox"], self.config["geoy"] = self.pos().x(), self.pos().y()
			self.config["geow"], self.config["geoh"] = self.width(), self.height()
		
		save_config_backup(self.config)
		
		# Closing the parent window
		QApplication.quit()
		
		pass
	##
##
