from os import getcwd
from PyQt5.QtWidgets import QMainWindow, QMdiSubWindow
from PyQt5.uic import loadUiType
from form import login_window, material_provider, material, comparing, accessories_provider,\
    accesspries, staff, program_settings, notification, clients, operation, other, audit
from form import article, order, cut, pay, salary
from classes import my_class
from classes.my_class import User
from PyQt5.QtGui import QIcon, QBrush, QImage
import sys

main_class, main_base_class = loadUiType(getcwd() + '/ui/main.ui')


class MainWindow(QMainWindow, main_class):
    def __init__(self, *args):

        super(MainWindow, self).__init__(*args)
        self.setupUi(self)
        self.mdi.setBackground(QBrush(QImage(getcwd() + "/images/logo.png")))
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.show()
        self.setDisabled(True)
        self.login = login_window.LoginWindow(self)

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

    def view_settings_road(self):
        self.sett_road = program_settings.SettingsRoad()
        self.sub_sett_road = QMdiSubWindow()
        self.sub_sett_road.setWidget(self.sett_road)
        self.mdi.addSubWindow(self.sub_sett_road)
        self.sub_sett_road.resize(self.sett_road.size())
        self.sub_sett_road.show()

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
        
    def view_product(self):
        self.article_list = article.ArticleList()
        self.sub_article_list = QMdiSubWindow()
        self.sub_article_list.setWidget(self.article_list)
        self.mdi.addSubWindow(self.sub_article_list)
        self.sub_article_list.resize(self.article_list.size())
        self.sub_article_list.show()
        
    def view_order_list(self):
        self.order_list = order.OrderList()
        self.sub_order_list = QMdiSubWindow()
        self.sub_order_list.setWidget(self.order_list)
        self.mdi.addSubWindow(self.sub_order_list)
        self.sub_order_list.resize(self.order_list.size())
        self.sub_order_list.show()

    def view_cut_mission_list(self):
        self.cut_mission_list = cut.CutListMission()
        self.sub_cut_mission_list = QMdiSubWindow()
        self.sub_cut_mission_list.setWidget(self.cut_mission_list)
        self.mdi.addSubWindow(self.sub_cut_mission_list)
        self.sub_cut_mission_list.resize(self.cut_mission_list.size())
        self.sub_cut_mission_list.show()

    def view_cut_list(self):
        self.cut_list = cut.CutList()
        self.sub_cut_list = QMdiSubWindow()
        self.sub_cut_list.setWidget(self.cut_list)
        self.mdi.addSubWindow(self.sub_cut_list)
        self.sub_cut_list.resize(self.cut_list.size())
        self.sub_cut_list.show()

    def view_pay_plus_minus(self):
        self.pay_plus_minus = pay.PayList()
        self.sub_pay_plus_minus = QMdiSubWindow()
        self.sub_pay_plus_minus.setWidget(self.pay_plus_minus)
        self.mdi.addSubWindow(self.sub_pay_plus_minus)
        self.sub_pay_plus_minus.resize(self.pay_plus_minus.size())
        self.sub_pay_plus_minus.show()

    def view_other_order_edi(self):
        self.input_order_edi = other.OrderEDI()
        self.sub_input_order_edi = QMdiSubWindow()
        self.sub_input_order_edi.setWidget(self.input_order_edi)
        self.mdi.addSubWindow(self.sub_input_order_edi)
        self.sub_input_order_edi.resize(self.input_order_edi.size())
        self.sub_input_order_edi.show()

    def view_audit_verification(self):
        self.audit_verification = audit.AuditVerification()
        self.sub_audit_verification = QMdiSubWindow()
        self.sub_audit_verification.setWidget(self.audit_verification)
        self.mdi.addSubWindow(self.sub_audit_verification)
        self.sub_audit_verification.resize(self.audit_verification.size())
        self.sub_audit_verification.show()

    def view_salary_work(self):
        self.salary_list = salary.SalaryList()
        self.sub_salary_list = QMdiSubWindow()
        self.sub_salary_list.setWidget(self.salary_list)
        self.mdi.addSubWindow(self.sub_salary_list)
        self.sub_salary_list.resize(self.salary_list.size())
        self.sub_salary_list.show()
        
    def login_access(self):
        self.statusBar().showMessage("Вы вошли как -= %s =-" % User().position_name())
        self.setEnabled(True)
        self.setFocus()

    def closeEvent(self, e):
        e.accept()
        sys.exit()
