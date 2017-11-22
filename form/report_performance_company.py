from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QBrush, QColor
import re
from function import my_sql
from function import table_to_html, to_excel
from classes import print_qt


report_performance_company_class = loadUiType(getcwd() + '/ui/report_performance_company.ui')[0]


class ReportPerformanceCompany(QMainWindow, report_performance_company_class):
    def __init__(self):
        super(ReportPerformanceCompany, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

    def ui_calc(self):
        date = (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate())

        query = """SELECT COUNT(cut.Id) FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s"""
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения кол-ва кроев", sql_info.msg, QMessageBox.Ok)
            return False
        
        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0]))
        self.le_cut.setText(text)

        query = """SELECT COUNT(pack.Id) FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s"""
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения кол-ва пачек", sql_info.msg, QMessageBox.Ok)
            return False

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0]))
        self.le_pack.setText(text)

        query = """SELECT COUNT(pack_operation.Id) FROM pack_operation
                      LEFT JOIN pack ON pack_operation.Pack_Id = pack.Id LEFT JOIN cut ON pack.Cut_Id = cut.Id WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s"""
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения кол-ва операций", sql_info.msg, QMessageBox.Ok)
            return False

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0]))
        self.le_operation.setText(text)

        query = """SELECT SUM(pack.Value_Pieces) FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s"""
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения кол-ва изделий", sql_info.msg, QMessageBox.Ok)
            return False

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0]))
        self.le_product.setText(text)

        query = """SELECT s1 + s2 + s3 FROM
                  (SELECT SUM(transaction_records_material.Balance * material_supplyposition.Price) AS s1
                  FROM transaction_records_material LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                  LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                  WHERE transaction_records_material.Cut_Material_Id IN (SELECT cut.Id FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)) t
                    JOIN
                  (SELECT SUM(transaction_records_accessories.Balance * accessories_supplyposition.Price) AS s2
                    FROM transaction_records_accessories
                      LEFT JOIN accessories_balance ON transaction_records_accessories.Supply_Balance_Id = accessories_balance.Id
                      LEFT JOIN accessories_supplyposition ON accessories_balance.accessories_SupplyPositionId = accessories_supplyposition.Id
                    WHERE transaction_records_accessories.Pack_Accessories_Id IN (SELECT pack_accessories.Id
                                                                                    FROM pack_accessories LEFT JOIN pack ON pack_accessories.Pack_Id = pack.Id
                                                                                      LEFT JOIN cut ON pack.Cut_Id = cut.Id
                                                                                    WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)) t2
                    JOIN
                  (SELECT SUM(pack_operation.Price * pack_operation.Value) AS s3 FROM pack_operation
                    LEFT JOIN pack ON pack_operation.Pack_Id = pack.Id LEFT JOIN cut ON pack.Cut_Id = cut.Id WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s) t3
                """
        sql_info = my_sql.sql_select(query, date*3)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения общей суммы", sql_info.msg, QMessageBox.Ok)
            return False

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0][0], 2)))
        self.le_sum.setText(text)