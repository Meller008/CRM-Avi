from os import getcwd
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUiType
import form.login_window

main_class, main_base_class = loadUiType(getcwd() + '/ui/main.ui')


class MainWindow(QMainWindow, main_class):
    def __init__(self, *args):

        super(MainWindow, self).__init__(*args)
        self.setupUi(self)
        self.show()
        self.setDisabled(True)
        self.login = form.login_window.LoginWindow(self)
        self.login.show()

    def view_add_material(self):
        pass

    def login_access(self):
        self.setEnabled(True)
        self.setFocus()
