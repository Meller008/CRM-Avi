from os import getcwd
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import re
from decimal import Decimal
import datetime
from function import my_sql
from form.templates import table


class NeedArticleOrder(QMainWindow):
    def __init__(self):
        super(NeedArticleOrder, self).__init__()
        loadUi(getcwd() + '/ui/report_need_article_order.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.start_settings()

        self.select_id = []

    def start_settings(self):
        self.tw_article.horizontalHeader().resizeSection(0, 60)
        self.tw_article.horizontalHeader().resizeSection(1, 50)
        self.tw_article.horizontalHeader().resizeSection(2, 90)
        self.tw_article.horizontalHeader().resizeSection(3, 240)
        self.tw_article.horizontalHeader().resizeSection(4, 55)
        self.tw_article.horizontalHeader().resizeSection(5, 65)
        self.tw_article.horizontalHeader().resizeSection(6, 50)
        self.tw_article.horizontalHeader().resizeSection(7, 65)

    def sql_need_article(self):
        query = """SELECT order_position.Product_Article_Parametr_Id, product_article.Article, product_article_size.Size, product_article_parametrs.Name,
                        product_article_parametrs.Client_Name, SUM(order_position.Value), product_article_warehouse.Value_In_Warehouse AS w,
                          IFNULL((SELECT SUM(pack.Value_Pieces)
                          FROM pack
                          WHERE Date_Make IS NULL AND pack.Article_Parametr_Id = order_position.Product_Article_Parametr_Id
                          GROUP BY pack.Article_Parametr_Id), 0) AS c
                      FROM order_position
                        LEFT JOIN product_article_parametrs ON order_position.Product_Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                        LEFT JOIN product_article_warehouse ON product_article_parametrs.Id = product_article_warehouse.Id_Article_Parametr
                      WHERE order_position.Order_Id IN %s GROUP BY order_position.Product_Article_Parametr_Id""" % str(tuple(self.select_id)).replace(",)", ")")
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения артикулов", sql_info.msg, QMessageBox.Ok)
            return False

        for article in sql_info:
            need_value = article[5] - article[6]
            if need_value > 0:
                self.tw_article.insertRow(self.tw_article.rowCount())
                for column in range(1, len(article)):
                    if isinstance(article[column], Decimal):
                        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(article[column]))
                    elif isinstance(article[column], datetime.date):
                        text = article[column].strftime("%d.%m.%Y")
                    else:
                        text = str(article[column])
                    item = QTableWidgetItem(text)
                    item.setData(5, article[0])
                    self.tw_article.setItem(self.tw_article.rowCount() - 1, column - 1, item)
                else:
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(need_value))
                    item = QTableWidgetItem(text)
                    item.setData(5, article[0])
                    self.tw_article.setItem(self.tw_article.rowCount() - 1, 7, item)

    def ui_view_filter_order(self):
        self.filter_order = OrderFilter(self, True, self.select_id)
        self.filter_order.setWindowModality(Qt.ApplicationModal)
        self.filter_order.show()

    def of_select_order_id(self, id):
        self.select_id = id
        self.sql_need_article()


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
                    if table_typle[0] in self.other_value:
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                item.setData(5, table_typle[0])
                self.table_widget.setItem(self.table_widget.rowCount() - 1, column - 1, item)

    def ui_double_click_table_item(self, item):  # Двойной клик по элементу
        pass

    def ui_other(self):
        # отправить выделеные заказы
        checked_id = []
        for row in range(self.table_widget.rowCount()):
            table_item = self.table_widget.item(row, 7)
            if table_item.checkState() == Qt.Checked:
                checked_id.append(table_item.data(5))

        self.main.of_select_order_id(checked_id)
        self.close()
        self.destroy()