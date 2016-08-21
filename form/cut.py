from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate

from function import my_sql
from form.templates import table, list
from form import clients, article

cut_list_class = loadUiType(getcwd() + '/ui/cut_list.ui')[0]
new_cut_mission_class = loadUiType(getcwd() + '/ui/cut_new_mission.ui')[0]


class CutList(QMainWindow, cut_list_class):
    def __init__(self):
        super(CutList, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

    def ui_new_cut_mission(self):
        self.new_cut_mission = NewCutMission()
        self.new_cut_mission.setModal(True)
        self.new_cut_mission.show()


class NewCutMission(QDialog, new_cut_mission_class):
    def __init__(self):
        super(NewCutMission, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()
        self.set_order_sql()

    def set_start_settings(self):
        self.tw_order.horizontalHeader().resizeSection(0, 120)
        self.tw_order.horizontalHeader().resizeSection(1, 240)
        self.tw_order.horizontalHeader().resizeSection(2, 80)
        self.tw_order.horizontalHeader().resizeSection(3, 80)
        self.tw_order.horizontalHeader().resizeSection(4, 60)
        self.tw_order.horizontalHeader().resizeSection(5, 200)

    def set_order_sql(self):
        query = """SELECT `order`.Id, clients.Name, clients_actual_address.Name, `order`.Date_Order, `order`.Date_Shipment, `order`.Number_Doc,
                    `order`.Note FROM `order` LEFT JOIN clients ON `order`.Client_Id = clients.Id
                    LEFT JOIN clients_actual_address ON `order`.Clients_Adress_Id = clients_actual_address.Id
                    LEFT JOIN order_position ON `order`.Id = order_position.Order_Id WHERE `order`.cut_mission = 0 GROUP BY `order`.Id"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение таблицы заказов", sql_info.msg, QMessageBox.Ok)
                return False

        for order in sql_info:
            row = self.tw_order.rowCount()
            self.tw_order.insertRow(row)
            for col in range(1, len(order)):
                table_item = QTableWidgetItem(str(order[col]))
                table_item.setData(5, order[0])
                if col == 1:
                    table_item.setCheckState(Qt.Unchecked)
                self.tw_order.setItem(row, col-1, table_item)

    def ui_order_select_comlete(self):
        pass

