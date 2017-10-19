from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QMainWindow,  QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate
from function import my_sql
import datetime

report_accept_pack_class = loadUiType(getcwd() + '/ui/report_accept_pack.ui')[0]


class ReportAcceptPack(QMainWindow, report_accept_pack_class):
    def __init__(self):
        super(ReportAcceptPack, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_settings()

    def start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

        self.tableWidget.horizontalHeader().resizeSection(0, 65)
        self.tableWidget.horizontalHeader().resizeSection(1, 65)
        self.tableWidget.horizontalHeader().resizeSection(2, 160)
        self.tableWidget.horizontalHeader().resizeSection(3, 120)
        self.tableWidget.horizontalHeader().resizeSection(4, 70)

    def ui_calc(self):
        query = """SELECT pack.Cut_Id, pack.Number, CONCAT(product_article.Article, ' (', product_article_size.Size, ') [', product_article_parametrs.Name, ']'),
                            clients.Name, pack.Date_Make
                          FROM pack LEFT JOIN clients ON pack.Client_Id = clients.Id
                            LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                            LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                            LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                            WHERE pack.Date_Make >= %s AND pack.Date_Make <= %s"""

        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate)))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения принятых пачек", sql_info.msg, QMessageBox.Ok)
            return False

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        if not sql_info:
            return False

        for table_typle in sql_info:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for column in range(len(table_typle)):
                if isinstance(table_typle[column], datetime.date):
                    text = table_typle[column].strftime("%d.%m.%Y")
                else:
                    text = str(table_typle[column])
                item = QTableWidgetItem(text)
                item.setData(5, table_typle[0])
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, column , item)