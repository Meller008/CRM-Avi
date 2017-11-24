from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
import re
from function import my_sql


report_warehouse_balance_date_class = loadUiType(getcwd() + '/ui/report_warehouse_balance_date.ui')[0]


class ReportWarehouseBalanceDate(QMainWindow, report_warehouse_balance_date_class):
    def __init__(self):
        super(ReportWarehouseBalanceDate, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.de_date_to.setDate(QDate.currentDate())

    def ui_calc(self):
        if self.tabWidget.currentIndex() == 0:
            query = """SELECT SUM(trm.Balance), SUM(trm.Balance * material_supplyposition.Price) AS sum_m
                          FROM transaction_records_material AS trm LEFT JOIN material_balance ON trm.Supply_Balance_Id = material_balance.Id
                            LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                          WHERE trm.Date < %s"""
            sql_info = my_sql.sql_select(query, (self.de_date_to.date().toPyDate(), ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения остатков ткани", sql_info.msg, QMessageBox.Ok)
                return False
            self.le_material_balance.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0])))
            self.le_material_sum.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][1])))

            query = """SELECT SUM(tra.Balance), SUM(tra.Balance * accessories_supplyposition.Price) AS sum_m
                          FROM transaction_records_accessories AS tra LEFT JOIN accessories_balance ON tra.Supply_Balance_Id = accessories_balance.Id
                            LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                          WHERE tra.Date < %s"""
            sql_info = my_sql.sql_select(query, (self.de_date_to.date().toPyDate(), ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения остатков фурнитуры", sql_info.msg, QMessageBox.Ok)
                return False

            self.le_accessories_balance.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0])))
            self.le_accessories_sum.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][1])))

        elif self.tabWidget.currentIndex() == 1:
            pass