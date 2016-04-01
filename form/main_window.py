from os import getcwd
from PyQt5.QtWidgets import QMainWindow, QMdiSubWindow
from PyQt5.uic import loadUiType
from form import login_window, material_provider, material
from classes import my_class

main_class, main_base_class = loadUiType(getcwd() + '/ui/main.ui')


class MainWindow(QMainWindow, main_class):
    def __init__(self, *args):

        self.user = my_class.User
        super(MainWindow, self).__init__(*args)
        self.setupUi(self)
        self.show()
        self.setDisabled(True)
        self.login = login_window.LoginWindow(self, self.user)
        self.login.show()

    def set_privilege(self):
        if self.user.privilege == "швея":
            self.ma_material.setDisabled(True)
            self.ma_material_provider.setDisabled(True)

    def view_material(self):
        self.material = material.Material()
        self.mdi.addSubWindow(self.material)
        self.material.show()

    def view_material_provider(self):
        self.mat_prov = material_provider.MaterialProvider()
        self.mdi.addSubWindow(self.mat_prov)
        self.mat_prov.show()

    def login_access(self):
        self.statusBar().showMessage("Вы вошли как -= %s =-" % self.user.privilege)
        self.setEnabled(True)
        self.set_privilege()
        self.setFocus()
