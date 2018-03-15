from os import getcwd
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
import re
from function import my_sql
from function import table_to_html
from classes import print_qt


class ReportShippedCustomer(QMainWindow):
    def __init__(self):
        super(ReportShippedCustomer, self).__init__()
        loadUi(getcwd() + '/ui/report_shipped_to_customer.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

        self.tableWidget.horizontalHeader().resizeSection(0, 150)
        self.tableWidget.horizontalHeader().resizeSection(1, 60)
        self.tableWidget.horizontalHeader().resizeSection(2, 70)
        self.tableWidget.horizontalHeader().resizeSection(3, 70)
        self.tableWidget.horizontalHeader().resizeSection(4, 90)
        self.tableWidget.horizontalHeader().resizeSection(5, 90)
        self.tableWidget.horizontalHeader().resizeSection(6, 60)

    def ui_calc(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        query = """SELECT clients.Id, clients.Name, `order`.Number_Doc, `order`.Number_Order, `order`.Date_Shipment,
                         `order`.Sum_Off_Nds, `order`.Sum_In_Nds, SUM(order_position.Value)
                      FROM `order` LEFT JOIN order_position ON `order`.Id = order_position.Order_Id
                        LEFT JOIN clients ON `order`.Client_Id = clients.Id
                      WHERE `order`.Date_Shipment >= %s AND `order`.Date_Shipment <= %s AND `order`.Shipped = 1 GROUP BY `order`.Id ORDER BY clients.Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения отгруженных зказов", sql_info.msg, QMessageBox.Ok)
            return False

        sum_off_nds, sum_in_nds, sum_value = 0, 0, 0
        all_sum_off_nds, all_sum_in_nds, all_sum_value = 0, 0, 0
        old_client_id = None
        for order in sql_info:

            if order[0] != old_client_id:  # Если новый клиент не равен предыдущемо делаем подсчет!

                if old_client_id is None:  # Если это первая итерация то просто белем ID клиента и мдем дальше!
                    old_client_id = order[0]
                else:
                    all_sum_off_nds += sum_off_nds
                    all_sum_in_nds += sum_in_nds
                    all_sum_value += sum_value

                    self.tableWidget.insertRow(self.tableWidget.rowCount())
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sum_off_nds))
                    item = QTableWidgetItem(text)
                    item.setData(5, order[0])
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sum_in_nds))
                    item = QTableWidgetItem(text)
                    item.setData(5, order[0])
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, item)

                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sum_value))
                    item = QTableWidgetItem(text)
                    item.setData(5, order[0])
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 6, item)

                    sum_off_nds, sum_in_nds, sum_value = 0, 0, 0
                    old_client_id = order[0]

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            item = QTableWidgetItem(order[1])
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            item = QTableWidgetItem(str(order[2]))
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            item = QTableWidgetItem(str(order[3]))
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            item = QTableWidgetItem(order[4].strftime("%d.%m.%Y"))
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

            sum_off_nds += order[5]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(order[5]))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

            sum_in_nds += order[6]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(order[6]))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, item)

            sum_value += order[7]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(order[7]))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 6, item)

        else:
            # Вставляем сумму для последнего клиента
            all_sum_off_nds += sum_off_nds
            all_sum_in_nds += sum_in_nds
            all_sum_value += sum_value

            self.tableWidget.insertRow(self.tableWidget.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sum_off_nds))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sum_in_nds))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sum_value))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 6, item)

            # Вставляем итоговоую сумму
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_sum_off_nds))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_sum_in_nds))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_sum_value))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 6, item)

    def ui_print(self):
        head = "Отгружено клиенту %s-%s" % (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate))
        html = table_to_html.tab_html(self.tableWidget, table_head=head)
        self.print_class = print_qt.PrintHtml(self, html)