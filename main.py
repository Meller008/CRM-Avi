from PyQt5.QtWidgets import QApplication
import sys
import form.main_window
from classes import my_class

app = QApplication(sys.argv)
main = form.main_window.MainWindow()
sys.exit(app.exec_())
