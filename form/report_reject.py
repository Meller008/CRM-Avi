from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QBrush, QColor
import re
from function import my_sql
from function import table_to_html, to_excel
from classes import print_qt


report_reject_class = loadUiType(getcwd() + '/ui/report_reject.ui')[0]


class ReportReject(QMainWindow, report_reject_class):
    def __init__(self):
        super(ReportReject, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

        self.tableWidget.horizontalHeader().resizeSection(0, 150)
        self.tableWidget.horizontalHeader().resizeSection(1, 70)
        self.tableWidget.horizontalHeader().resizeSection(2, 70)
        self.tableWidget.horizontalHeader().resizeSection(3, 70)
        self.tableWidget.horizontalHeader().resizeSection(4, 70)
        self.tableWidget.horizontalHeader().resizeSection(5, 70)

    def ui_calc(self):

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        query = """SELECT product_article_parametrs.Id, CONCAT(product_article.Article, '(', product_article_size.Size, ')[', product_article_parametrs.Name, ']'),
                      SUM(pack.Value_Pieces + pack.Value_Damage), SUM(pack.Value_Damage), (SUM(pack.Value_Damage) * 100 / SUM(pack.Value_Pieces + pack.Value_Damage))
                      FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE pack.Value_Damage != 0 AND cut.Date_Cut >= %s AND cut.Date_Cut <= %s
                      GROUP BY product_article_parametrs.Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения брака", sql_info.msg, QMessageBox.Ok)
            return False

        all_value, all_value_damage = 0, 0

        for article in sql_info:

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            item = QTableWidgetItem(article[1])
            item.setData(5, article[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            all_value += article[2]
            item = QTableWidgetItem(str(article[2]))
            item.setData(5, article[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            all_value_damage += article[3]
            item = QTableWidgetItem(str(article[3]))
            item.setData(5, article[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            item = QTableWidgetItem(str(round(article[4], 4)))
            item.setData(5, article[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

        else:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            item = QTableWidgetItem(str(all_value))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            item = QTableWidgetItem(str(all_value_damage))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            avg = all_value_damage * 100 / all_value
            item = QTableWidgetItem(str(round(avg, 4)))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

