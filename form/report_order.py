from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog, QProgressDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QBrush, QColor
import re
from decimal import Decimal
import datetime
import openpyxl
from openpyxl.styles import Border, Side, Font, Alignment, PatternFill
from openpyxl.worksheet.pagebreak import Break
from copy import copy
from function import my_sql, to_excel
from form.templates import table, list
from form import clients, article
import num2t4ru

need_article = loadUiType(getcwd() + '/ui/report_need_article_order.ui')[0]


class NeedArticleOrder(QMainWindow, need_article):
    def __init__(self):
        super(NeedArticleOrder, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

    def ui_view_filter_order(self):
        self.filter_order = OrderFilter(self, True)
        self.filter_order.setWindowModality(Qt.ApplicationModal)
        self.filter_order.show()


class OrderFilter(table.TableList):
    def set_settings(self):

        self.setWindowTitle("Заказы")  # Имя окна
        self.resize(900, 270)

        self.pb_copy.deleteLater()
        self.pb_add.deleteLater()
        self.pb_change.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_filter.deleteLater()
        self.pb_other.setText("Принять")
        self.pb_export.deleteLater()
        self.pb_update.deleteLater()

        self.toolBar.setStyleSheet("background-color: rgb(126, 176, 127);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Клиент", 120), ("Пункт разгрузки", 170), ("Дата заказ.", 75), ("Дата отгр.", 70), ("№ док.", 50), ("Стоймость", 105),
                                  ("Примечание", 230), (" ", 40))

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT `order`.Id, clients.Name, clients_actual_address.Name, `order`.Date_Order, `order`.Date_Shipment, `order`.Number_Doc,
                                    SUM(order_position.Value * order_position.Price), `order`.Note, ''
                                      FROM `order` LEFT JOIN clients ON `order`.Client_Id = clients.Id
                                        LEFT JOIN clients_actual_address ON `order`.Clients_Adress_Id = clients_actual_address.Id
                                        LEFT JOIN order_position ON `order`.Id = order_position.Order_Id WHERE `order`.Shipped = 0
                                      GROUP BY `order`.Id ORDER BY `order`.Date_Order DESC"""

        self.query_table_dell = ""

    def set_table_info(self):
        self.table_items = my_sql.sql_select(self.query_table_select)
        if "mysql.connector.errors" in str(type(self.table_items)):
                QMessageBox.critical(self, "Ошибка sql получение таблицы", self.table_items.msg, QMessageBox.Ok)
                return False

        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        if not self.table_items:
            return False

        for table_typle in self.table_items:
            self.table_widget.insertRow(self.table_widget.rowCount())
            for column in range(1, len(table_typle)):
                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(table_typle[column]))
                elif isinstance(table_typle[column], datetime.date):
                    text = table_typle[column].strftime("%d.%m.%Y")
                else:
                    text = str(table_typle[column])
                item = QTableWidgetItem(text)
                if column == 8:
                    item.setCheckState(Qt.Unchecked)
                item.setData(5, table_typle[0])
                self.table_widget.setItem(self.table_widget.rowCount() - 1, column - 1, item)

    def ui_double_click_table_item(self, item):  # Двойной клик по элементу
        pass

    def ui_other(self):
        # отправить выделеные заказы
        for row in range(self.table_widget.rowCount()):
            table_item = self.table_widget.item(row, 7)
            if table_item.checkState() == Qt.Checked:
                print(table_item.data(5))