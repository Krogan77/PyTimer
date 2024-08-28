

""" Entry point for the application """

from PySide6.QtWidgets import QApplication

from window.main_window import MainWindow, InvisibleParent


if __name__ == '__main__':
	app = QApplication()
	
	invisible_parent = InvisibleParent()
	window = MainWindow(invisible_parent)
	window.show()
	
	app.exec()
