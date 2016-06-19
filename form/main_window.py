from os import getcwd
from PyQt5.QtWidgets import QMainWindow, QMdiSubWindow
from PyQt5.uic import loadUiType
from form import login_window, material_provider, material, comparing, accessories_provider, accesspries, staff, program_settings, notification, clients, operation
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

    def view_staff_country(self):
        self.staff_country = staff.Country()
        self.sub_staff_country = QMdiSubWindow()
        self.sub_staff_country.setWidget(self.staff_country)
        self.mdi.addSubWindow(self.sub_staff_country)
        self.sub_staff_country.resize(self.staff_country.size())
        self.sub_staff_country.show()

    def view_staff_position(self):
        self.staff_position = staff.StaffPosition()
        self.sub_staff_position = QMdiSubWindow()
        self.sub_staff_position.setWidget(self.staff_position)
        self.mdi.addSubWindow(self.sub_staff_position)
        self.sub_staff_position.resize(self.staff_position.size())
        self.sub_staff_position.show()

    def view_staff_list(self):
        self.staff_list = staff.Staff()
        self.sub_staff_list = QMdiSubWindow()
        self.sub_staff_list.setWidget(self.staff_list)
        self.mdi.addSubWindow(self.sub_staff_list)
        self.sub_staff_list.resize(self.staff_list.size())
        self.sub_staff_list.show()

    def view_staff_calendar(self):
        self.staff_calendar = notification.WorkCalendar()
        self.sub_staff_calendar = QMdiSubWindow()
        self.sub_staff_calendar.setWidget(self.staff_calendar)
        self.mdi.addSubWindow(self.sub_staff_calendar)
        self.sub_staff_calendar.resize(self.staff_calendar.size())
        self.sub_staff_calendar.show()

    def view_settings_path(self):
        self.sett_path = program_settings.SettingsPath()
        self.sub_sett_path = QMdiSubWindow()
        self.sub_sett_path.setWidget(self.sett_path)
        self.mdi.addSubWindow(self.sub_sett_path)
        self.sub_sett_path.resize(self.sett_path.size())
        self.sub_sett_path.show()

    def view_clients(self):
        self.clients = clients.ClientsList()
        self.sub_clients = QMdiSubWindow()
        self.sub_clients.setWidget(self.clients)
        self.mdi.addSubWindow(self.sub_clients)
        self.sub_clients.resize(self.clients.size())
        self.sub_clients.show()
        
    def view_operation(self):
        self.operation_list = operation.OperationList()
        self.sub_operation_list = QMdiSubWindow()
        self.sub_operation_list.setWidget(self.operation_list)
        self.mdi.addSubWindow(self.sub_operation_list)
        self.sub_operation_list.resize(self.operation_list.size())
        self.sub_operation_list.show()
        
    def login_access(self):
        self.statusBar().showMessage("Вы вошли как -= %s =-" % self.user.privilege)
        self.setEnabled(True)
        self.set_privilege()
        self.setFocus()

    def closeEvent(self, e):
        e.accept()
        sys.exit()
