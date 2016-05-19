from os import getcwd
from PyQt5.QtWidgets import QMainWindow, QMdiSubWindow
from PyQt5.uic import loadUiType
from form import login_window, material_provider, material, comparing, accessories_provider, accesspries
from classes import my_class
from PyQt5.QtGui import QIcon
import sys

main_class, main_base_class = loadUiType(getcwd() + '/ui/main.ui')


class MainWindow(QMainWindow, main_class):
    def __init__(self, *args):

        self.user = my_class.User
        super(MainWindow, self).__init__(*args)
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
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
        self.sub_material = QMdiSubWindow()
        self.sub_material.setWidget(self.material)
        self.mdi.addSubWindow(self.sub_material)
        self.sub_material.resize(self.material.size())
        self.sub_material.show()

    def view_material_provider(self):
        self.mat_prov = material_provider.MaterialProvider()
        self.sub_provider = QMdiSubWindow()
        self.sub_provider.setWidget(self.mat_prov)
        self.mdi.addSubWindow(self.sub_provider)
        self.sub_provider.resize(self.mat_prov.size())
        self.sub_provider.show()

    def view_material_name(self):
        self.material_neme = material_provider.MaterialName()
        self.sub_mater_name = QMdiSubWindow()
        self.sub_mater_name.setWidget(self.material_neme)
        self.mdi.addSubWindow(self.sub_mater_name)
        self.sub_mater_name.resize(self.material_neme.size())
        self.sub_mater_name.show()

    def view_comparing_name(self):
        self.comparing_name = comparing.ComparingName()
        self.sub_comp_name = QMdiSubWindow()
        self.sub_comp_name.setWidget(self.comparing_name)
        self.mdi.addSubWindow(self.sub_comp_name)
        self.sub_comp_name.resize(self.comparing_name.size())
        self.sub_comp_name.show()

    def view_accessories_name(self):
        self.accessoriesl_neme = accessories_provider.AccessoriesName()
        self.sub_accsess_name = QMdiSubWindow()
        self.sub_accsess_name.setWidget(self.accessoriesl_neme)
        self.mdi.addSubWindow(self.sub_accsess_name)
        self.sub_accsess_name.resize(self.accessoriesl_neme.size())
        self.sub_accsess_name.show()

    def view_accessories_provider(self):
        self.access_prov = accessories_provider.AccessoriesProvider()
        self.sub_provider_access = QMdiSubWindow()
        self.sub_provider_access.setWidget(self.access_prov)
        self.mdi.addSubWindow(self.sub_provider_access)
        self.sub_provider_access.resize(self.access_prov.size())
        self.sub_provider_access.show()

    def view_accessories(self):
        self.accessories = accesspries.Accessories()
        self.accessories.set_settings()
        self.sub_accessories = QMdiSubWindow()
        self.sub_accessories.setWidget(self.accessories)
        self.mdi.addSubWindow(self.sub_accessories)
        self.sub_accessories.resize(self.accessories.size())
        self.sub_accessories.show()

    def login_access(self):
        self.statusBar().showMessage("Вы вошли как -= %s =-" % self.user.privilege)
        self.setEnabled(True)
        self.set_privilege()
        self.setFocus()

    def closeEvent(self, e):
        e.accept()
        sys.exit()
