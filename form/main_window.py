from os import getcwd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMdiSubWindow, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QBrush, QImage
from form import login_window, provider, comparing, staff, program_settings, notification, \
    clients, operation, other, audit, warehouse_material, warehouse_accessories
from form import article, order, cut, pay, salary, operation_list, warehouse_product, beika,\
    warehouse_rest, supply_material, supply_accessories, scan_pack, settings_access
from form import report_supply, report_cost_article, test_window, report_sibestoimost, report_rest_work,\
    report_accept_pack, pack, report_profit, report_performance_company, report_shipped_to_customer
from form import staff_traffic, report_material_consumption, report_warehouse_balance_date,\
    report_all, report_nalog, report_article_day, test_warehouse
from form import report_order, report_reject, transaction_warehouse, material_in_pack, warehouse_adjustments
from function import my_sql
from classes.my_class import User
import sys
import logging
import logging.config


class MainWindow(QMainWindow):
    def __init__(self, win_arg):
        super(MainWindow, self).__init__()
        loadUi(getcwd() + '/ui/main.ui', self)
        self.mdi.setBackground(QBrush(QImage(getcwd() + "/images/logo.png")))
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.menu_3.setEnabled(False)

        if "-FS" in win_arg:
            self.arg_FS()

        logging.config.fileConfig(getcwd() + '/setting/logger_conf.ini')
        self.logger = logging.getLogger("MainLog")

        self.show()
        self.setDisabled(True)

        self.login = login_window.LoginWindow(self)
        # self.admin_login()

    def access(self):
        for item in User().access_list(self.__class__.__name__):
            a = getattr(self, item["atr1"])
            if item["atr2"]:
                a = getattr(a, item["atr2"])

            if item["value"]:
                try:
                    val = int(item["value"])
                except:
                    val = item["value"]
                a(val)
            else:
                a()

    def view_material(self):
        self.material = supply_material.MaterialSupplyList()
        self.sub_material = QMdiSubWindow()
        self.sub_material.setWidget(self.material)
        self.mdi.addSubWindow(self.sub_material)
        self.sub_material.resize(self.material.size())
        self.sub_material.show()

    def view_material_provider(self):
        self.mat_prov = provider.ProviderMaterial()
        self.sub_provider = QMdiSubWindow()
        self.sub_provider.setWidget(self.mat_prov)
        self.mdi.addSubWindow(self.sub_provider)
        self.sub_provider.resize(self.mat_prov.size())
        self.sub_provider.show()

    def view_material_name(self):
        self.material_neme = supply_material.MaterialName()
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
        self.accessories_name = supply_accessories.AccessoriesName()
        self.sub_accsess_name = QMdiSubWindow()
        self.sub_accsess_name.setWidget(self.accessories_name)
        self.mdi.addSubWindow(self.sub_accsess_name)
        self.sub_accsess_name.resize(self.accessories_name.size())
        self.sub_accsess_name.show()

    def view_accessories_provider(self):
        self.access_prov = provider.ProviderAccessories()
        self.sub_provider_access = QMdiSubWindow()
        self.sub_provider_access.setWidget(self.access_prov)
        self.mdi.addSubWindow(self.sub_provider_access)
        self.sub_provider_access.resize(self.access_prov.size())
        self.sub_provider_access.show()

    def view_accessories(self):
        self.accessories = supply_accessories.AccessoriesSupplyList()
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

    def view_staff_card(self):
        self.staff_card = staff_traffic.StaffCardList()
        self.sub_staff_card = QMdiSubWindow()
        self.sub_staff_card.setWidget(self.staff_card)
        self.mdi.addSubWindow(self.sub_staff_card)
        self.sub_staff_card.resize(self.staff_card.size())
        self.sub_staff_card.show()

    def view_staff_traffic(self):
        self.staff_traffic = staff_traffic.StaffTraffic()
        self.sub_staff_traffic = QMdiSubWindow()
        self.sub_staff_traffic.setWidget(self.staff_traffic)
        self.mdi.addSubWindow(self.sub_staff_traffic)
        self.sub_staff_traffic.resize(self.staff_traffic.size())
        self.sub_staff_traffic.show()

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
        self.clients = clients.ClientList()
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

    def view_add_operation(self):
        self.add_operation_list = operation.OperationAddList()
        self.sub_add_operation_list = QMdiSubWindow()
        self.sub_add_operation_list.setWidget(self.add_operation_list)
        self.mdi.addSubWindow(self.sub_add_operation_list)
        self.sub_add_operation_list.resize(self.add_operation_list.size())
        self.sub_add_operation_list.show()

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

    def view_article_list(self):
        self.article_list_all = article.ArticleListAll()
        self.sub_article_list_all = QMdiSubWindow()
        self.sub_article_list_all.setWidget(self.article_list_all)
        self.mdi.addSubWindow(self.sub_article_list_all)
        self.sub_article_list_all.resize(self.article_list_all.size())
        self.sub_article_list_all.show()

    def view_article_test(self):
        self.article_test = article.ArticleTest()
        self.sub_article_test = QMdiSubWindow()
        self.sub_article_test.setWidget(self.article_test)
        self.mdi.addSubWindow(self.sub_article_test)
        self.sub_article_test.resize(self.article_test.size())
        self.sub_article_test.show()

    def view_pack_list(self):
        self.pack_list = pack.PackList()
        self.sub_pack_list = QMdiSubWindow()
        self.sub_pack_list.setWidget(self.pack_list)
        self.mdi.addSubWindow(self.sub_pack_list)
        self.sub_pack_list.resize(self.pack_list.size())
        self.sub_pack_list.show()

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

    def view_pack_operation_list(self):
        self.operation_list = operation_list.PayList(no_start_set=True)
        self.sub_operation_list = QMdiSubWindow()
        self.sub_operation_list.setWidget(self.operation_list)
        self.mdi.addSubWindow(self.sub_operation_list)
        self.sub_operation_list.resize(self.operation_list.size())
        self.sub_operation_list.show()

    def view_product_warehouse(self):
        self.product_warehouse = warehouse_product.Warehouse()
        self.sub_product_warehouse = QMdiSubWindow()
        self.sub_product_warehouse.setWidget(self.product_warehouse)
        self.mdi.addSubWindow(self.sub_product_warehouse)
        self.sub_product_warehouse.resize(self.product_warehouse.size())
        self.sub_product_warehouse.show()

    def view_product_warehouse_2(self):
        self.product_warehouse2 = warehouse_product.Warehouse2()
        self.sub_product_warehouse2 = QMdiSubWindow()
        self.sub_product_warehouse2.setWidget(self.product_warehouse2)
        self.mdi.addSubWindow(self.sub_product_warehouse2)
        self.sub_product_warehouse2.resize(self.product_warehouse2.size())
        self.sub_product_warehouse2.show()

    def view_warehouse_rest(self):
        self.rest_warehouse = warehouse_rest.WarehouseRest()
        self.sub_rest_warehouse = QMdiSubWindow()
        self.sub_rest_warehouse.setWidget(self.rest_warehouse)
        self.mdi.addSubWindow(self.sub_rest_warehouse)
        self.sub_rest_warehouse.resize(self.rest_warehouse.size())
        self.sub_rest_warehouse.show()

    def view_warehouse_material(self):
        self.material_warehouse = warehouse_material.Warehouse()
        self.sub_material_warehouse = QMdiSubWindow()
        self.sub_material_warehouse.setWidget(self.material_warehouse)
        self.mdi.addSubWindow(self.sub_material_warehouse)
        self.sub_material_warehouse.resize(self.material_warehouse.size())
        self.sub_material_warehouse.show()

    def view_warehouse_accessories(self):
        self.accessories_warehouse = warehouse_accessories.Warehouse()
        self.sub_material_accessories = QMdiSubWindow()
        self.sub_material_accessories.setWidget(self.accessories_warehouse)
        self.mdi.addSubWindow(self.sub_material_accessories)
        self.sub_material_accessories.resize(self.accessories_warehouse.size())
        self.sub_material_accessories.show()

    def view_warehouse_adjustments_material(self):
        self.adjustments_material = warehouse_adjustments.MaterialAdjustmentsList()
        self.sub_adjustments_material = QMdiSubWindow()
        self.sub_adjustments_material.setWidget(self.adjustments_material)
        self.mdi.addSubWindow(self.sub_adjustments_material)
        self.sub_adjustments_material.resize(self.adjustments_material.size())
        self.sub_adjustments_material.show()

    def view_transaction_warehouse(self):
        self.transaction_warehouse = transaction_warehouse.TransactionWarehouse()
        self.sub_transaction_warehouse = QMdiSubWindow()
        self.sub_transaction_warehouse.setWidget(self.transaction_warehouse)
        self.mdi.addSubWindow(self.sub_transaction_warehouse)
        self.sub_transaction_warehouse.resize(self.transaction_warehouse.size())
        self.sub_transaction_warehouse.show()

    def view_test_warehouse_material(self):
        self.test_warehouse_material = test_warehouse.TestWarehouseMaterial()
        self.sub_test_warehouse_material = QMdiSubWindow()
        self.sub_test_warehouse_material.setWidget(self.test_warehouse_material)
        self.mdi.addSubWindow(self.sub_test_warehouse_material)
        self.sub_test_warehouse_material.resize(self.test_warehouse_material.size())
        self.sub_test_warehouse_material.show()

    def view_test_warehouse_accessories(self):
        self.test_warehouse_accessories = test_warehouse.TestWarehouseAccessories()
        self.sub_test_warehouse_accessories = QMdiSubWindow()
        self.sub_test_warehouse_accessories.setWidget(self.test_warehouse_accessories)
        self.mdi.addSubWindow(self.sub_test_warehouse_accessories)
        self.sub_test_warehouse_accessories.resize(self.test_warehouse_accessories.size())
        self.sub_test_warehouse_accessories.show()

    def view_test_fast_warehouse(self):
        self.test_fast_warehouse = test_warehouse.TestFastWarehouse()
        self.sub_test_fast_warehouse = QMdiSubWindow()
        self.sub_test_fast_warehouse.setWidget(self.test_fast_warehouse)
        self.mdi.addSubWindow(self.sub_test_fast_warehouse)
        self.sub_test_fast_warehouse.resize(self.test_fast_warehouse.size())
        self.sub_test_fast_warehouse.show()

    def view_beika(self):
        self.beika = beika.BeikaList()
        self.sub_beika = QMdiSubWindow()
        self.sub_beika.setWidget(self.beika)
        self.mdi.addSubWindow(self.sub_beika)
        self.sub_beika.resize(self.beika.size())
        self.sub_beika.show()

    def view_supply_material(self):
        self.supply_material = supply_material.MaterialSupplyList()
        self.sub_supply_material = QMdiSubWindow()
        self.sub_supply_material.setWidget(self.supply_material)
        self.mdi.addSubWindow(self.sub_supply_material)
        self.sub_supply_material.resize(self.supply_material.size())
        self.sub_supply_material.show()

    def view_supply_accessories(self):
        self.supply_accessories = supply_accessories.AccessoriesSupplyList()
        self.sub_supply_accessories = QMdiSubWindow()
        self.sub_supply_accessories.setWidget(self.supply_accessories)
        self.mdi.addSubWindow(self.sub_supply_accessories)
        self.sub_supply_accessories.resize(self.supply_accessories.size())
        self.sub_supply_accessories.show()

    def view_scan_pack(self):
        self.scan_pack = scan_pack.ScanPack()
        self.sub_scan_pack = QMdiSubWindow()
        self.sub_scan_pack.setWidget(self.scan_pack)
        self.mdi.addSubWindow(self.sub_scan_pack)
        self.sub_scan_pack.resize(self.scan_pack.size())
        self.sub_scan_pack.show()

    def view_settings_access(self):
        self.settings_access = settings_access.Access()
        self.sub_settings_access = QMdiSubWindow()
        self.sub_settings_access.setWidget(self.settings_access)
        self.mdi.addSubWindow(self.sub_settings_access)
        self.sub_settings_access.resize(self.settings_access.size())
        self.sub_settings_access.show()

    def view_report_need_article_order(self):
        self.report_need_article = report_order.NeedArticleOrder()
        self.sub_report_need_article = QMdiSubWindow()
        self.sub_report_need_article.setWidget(self.report_need_article)
        self.mdi.addSubWindow(self.sub_report_need_article)
        self.sub_report_need_article.resize(self.report_need_article.size())
        self.sub_report_need_article.show()

    def view_report_supply(self):
        self.report_supply = report_supply.ReportSupply()
        self.sub_report_supply = QMdiSubWindow()
        self.sub_report_supply.setWidget(self.report_supply)
        self.mdi.addSubWindow(self.sub_report_supply)
        self.sub_report_supply.resize(self.report_supply.size())
        self.sub_report_supply.show()

    def view_report_cost_article(self):
        self.report_cost_article = report_cost_article.ReportCostArticle()
        self.sub_report_cost_article = QMdiSubWindow()
        self.sub_report_cost_article.setWidget(self.report_cost_article)
        self.mdi.addSubWindow(self.sub_report_cost_article)
        self.sub_report_cost_article.resize(self.report_cost_article.size())
        self.sub_report_cost_article.show()

    def view_report_sibestoimost(self):
        self.report_sibest = report_sibestoimost.ReportSibestoimost()
        self.sub_report_sibest = QMdiSubWindow()
        self.sub_report_sibest.setWidget(self.report_sibest)
        self.mdi.addSubWindow(self.sub_report_sibest)
        self.sub_report_sibest.resize(self.report_sibest.size())
        self.sub_report_sibest.show()

    def view_report_rest_for_work(self):
        self.report_rest_work = report_rest_work.ReportRestWork()
        self.sub_report_rest_work = QMdiSubWindow()
        self.sub_report_rest_work.setWidget(self.report_rest_work)
        self.mdi.addSubWindow(self.sub_report_rest_work)
        self.sub_report_rest_work.resize(self.report_rest_work.size())
        self.sub_report_rest_work.show()

    def view_report_pack_accept(self):
        self.report_pack_accept = report_accept_pack.ReportAcceptPack()
        self.sub_report_pack_accept = QMdiSubWindow()
        self.sub_report_pack_accept.setWidget(self.report_pack_accept)
        self.mdi.addSubWindow(self.sub_report_pack_accept)
        self.sub_report_pack_accept.resize(self.report_pack_accept.size())
        self.sub_report_pack_accept.show()

    def view_report_material_consumption(self):
        self.report_material_consumption = report_material_consumption.ReportMaterialConsumption()
        self.sub_report_material_consumption = QMdiSubWindow()
        self.sub_report_material_consumption.setWidget(self.report_material_consumption)
        self.mdi.addSubWindow(self.sub_report_material_consumption)
        self.sub_report_material_consumption.resize(self.report_material_consumption.size())
        self.sub_report_material_consumption.show()

    def view_report_profit(self):
        self.report_profit = report_profit.ReportProfit()
        self.sub_report_profit = QMdiSubWindow()
        self.sub_report_profit.setWidget(self.report_profit)
        self.mdi.addSubWindow(self.sub_report_profit)
        self.sub_report_profit.resize(self.report_profit.size())
        self.sub_report_profit.show()

    def view_report_performance_company(self):
        self.report_performance_company = report_performance_company.ReportPerformanceCompany()
        self.sub_report_performance_company = QMdiSubWindow()
        self.sub_report_performance_company.setWidget(self.report_performance_company)
        self.mdi.addSubWindow(self.sub_report_performance_company)
        self.sub_report_performance_company.resize(self.report_performance_company.size())
        self.sub_report_performance_company.show()

    def view_report_shipped_customer(self):
        self.report_shipped_customer = report_shipped_to_customer.ReportShippedCustomer()
        self.sub_report_shipped_customer = QMdiSubWindow()
        self.sub_report_shipped_customer.setWidget(self.report_shipped_customer)
        self.mdi.addSubWindow(self.sub_report_shipped_customer)
        self.sub_report_shipped_customer.resize(self.report_shipped_customer.size())
        self.sub_report_shipped_customer.show()

    def view_report_warehouse_balance_date(self):
        self.report_warehouse_balance_date = report_warehouse_balance_date.ReportWarehouseBalanceDate()
        self.sub_report_warehouse_balance_date = QMdiSubWindow()
        self.sub_report_warehouse_balance_date.setWidget(self.report_warehouse_balance_date)
        self.mdi.addSubWindow(self.sub_report_warehouse_balance_date)
        self.sub_report_warehouse_balance_date.resize(self.report_warehouse_balance_date.size())
        self.sub_report_warehouse_balance_date.show()

    def view_report_reject(self):
        self.report_reject = report_reject.ReportReject()
        self.sub_report_reject = QMdiSubWindow()
        self.sub_report_reject.setWidget(self.report_reject)
        self.mdi.addSubWindow(self.sub_report_reject)
        self.sub_report_reject.resize(self.report_reject.size())
        self.sub_report_reject.show()

    def view_report_all(self):
        self.report_all = report_all.ReportAll()
        self.sub_view_report_all = QMdiSubWindow()
        self.sub_view_report_all.setWidget(self.report_all)
        self.mdi.addSubWindow(self.sub_view_report_all)
        self.sub_view_report_all.resize(self.report_all.size())
        self.sub_view_report_all.show()

    def view_report_nalog(self):
        self.report_nalog = report_nalog.ReportNalog()
        self.sub_report_nalog = QMdiSubWindow()
        self.sub_report_nalog.setWidget(self.report_nalog)
        self.mdi.addSubWindow(self.sub_report_nalog)
        self.sub_report_nalog.resize(self.report_nalog.size())
        self.sub_report_nalog.show()

    def view_report_article_day(self):
        self.report_article_day = report_article_day.ReportArticleDay()
        self.sub_report_article_day = QMdiSubWindow()
        self.sub_report_article_day.setWidget(self.report_article_day)
        self.mdi.addSubWindow(self.sub_report_article_day)
        self.sub_report_article_day.resize(self.report_article_day.size())
        self.sub_report_article_day.show()

    def view_material_in_pack(self):
        self.material_in_pack = material_in_pack.MaterialInPack()
        self.sub_material_in_pack = QMdiSubWindow()
        self.sub_material_in_pack.setWidget(self.material_in_pack)
        self.mdi.addSubWindow(self.sub_material_in_pack)
        self.sub_material_in_pack.resize(self.material_in_pack.size())
        self.sub_material_in_pack.show()

    def view_test_window(self):
        self.test_window = test_window.TestWindow()
        self.sub_test_window = QMdiSubWindow()
        self.sub_test_window.setWidget(self.test_window)
        self.mdi.addSubWindow(self.sub_test_window)
        self.sub_test_window.resize(self.test_window.size())
        self.sub_test_window.show()

    def login_access(self):
        self.logger.info(u"[Пользователь {:04d}] {}".format(User().id(), "Зашел в программу"))
        self.statusBar().showMessage("Вы вошли как -= %s =-" % User().position_name())
        self.setEnabled(True)
        self.setFocus()
        self.access()

    def admin_login(self):
        self.statusBar().showMessage("Вы вошли как -= %s =-" % User().position_name())
        self.setEnabled(True)
        self.setFocus()
        self.access()

    def beika_no_finished(self):
        query = """SELECT COUNT(*) FROM beika WHERE Finished = 0"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            beika_txt = "error sql"
        else:
            beika_txt = "Не зкарыто бейки: " + str(sql_info[0][0])
        beika = QLabel(beika_txt)
        self.statusBar().addPermanentWidget(beika)

    def closeEvent(self, e):
        self.logger.info(u"[Пользователь {:04d}] {}".format(User().id(), "Вышел из программы"))
        e.accept()
        self.close()
        self.destroy()
        sys.exit()

    def arg_FS(self):
        self.setWindowState(Qt.WindowMaximized)
