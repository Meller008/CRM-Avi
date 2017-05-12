from os import getcwd
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QTableWidgetItem, QLineEdit, QSizePolicy, QWidget
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5.QtCore import Qt, QDate
from function import my_sql
from form import provider, comparing, staff
from form.templates import table, list
from decimal import Decimal
import re


staff_card = loadUiType(getcwd() + '/ui/staff_card.ui')[0]


class StaffCardList(table.TableList):
    def set_settings(self):

        self.filter = None

        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.pb_filter.deleteLater()

        self.setWindowTitle("Настройка карт")  # Имя окна
        self.resize(350, 270)
        self.toolBar.setStyleSheet("background-color: rgb(129, 66, 255);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Фамилия", 100), ("Имя", 100), ("Карта", 100))

        self.query_table_all = """SELECT staff_worker_kard.Worker_Id, staff_worker_info.Last_Name, staff_worker_info.First_Name, staff_worker_kard.Card_Id
                                      FROM staff_worker_kard
                                      LEFT JOIN staff_worker_info ON staff_worker_kard.Worker_Id = staff_worker_info.Id"""

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT staff_worker_kard.Worker_Id, staff_worker_info.Last_Name, staff_worker_info.First_Name, staff_worker_kard.Card_Id
                                      FROM staff_worker_kard
                                      LEFT JOIN staff_worker_info ON staff_worker_kard.Worker_Id = staff_worker_info.Id"""

        self.query_table_dell = "DELETE FROM staff_worker_kard WHERE Worker_Id = %s"

    def ui_add_table_item(self):  # Добавить предмет
        self.new_card = ChangeCard(self)
        self.new_card.setModal(True)
        self.new_card.show()

    def ui_change_table_item(self, id=False):  # изменить элемент
        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите операцию который хотите изменить", QMessageBox.Ok)
                return False

        self.change_card = ChangeCard(self, item_id)
        self.change_card.setWindowModality(Qt.ApplicationModal)
        self.change_card.show()


class ChangeCard(QDialog, staff_card):
    def __init__(self, main, id=None):
        super(ChangeCard, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.main = main
        self.id = id
        self.set_start_settings()

    def set_start_settings(self):
        if self.id:
            query = """SELECT CONCAT(Last_Name, ' ', First_Name), staff_worker_kard.Card_Id FROM staff_worker_info
                          LEFT JOIN staff_worker_kard ON staff_worker_info.Id = staff_worker_kard.Worker_Id
                          WHERE Id = %s"""
            sql_info = my_sql.sql_select(query, (self.id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql сохр. карты", sql_info.msg, QMessageBox.Ok)
                    return False
            self.le_worker.setWhatsThis(str(self.id))
            self.le_worker.setText(sql_info[0][0])
            self.le_card.setText(sql_info[0][1])

    def ui_view_worker(self):
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_acc(self):
        if self.id:
            query = "UPDATE staff_worker_kard SET Worker_Id = %s, Card_Id = %s WHERE Worker_Id = %s"
            sql_info = my_sql.sql_change(query, (self.le_worker.whatsThis(), self.le_card.text(), self.id))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql сохр. карты", sql_info.msg, QMessageBox.Ok)
                    return False
        else:
            query = "INSERT INTO staff_worker_kard (Worker_Id, Card_Id) VALUES (%s, %s)"
            sql_info = my_sql.sql_change(query, (self.le_worker.whatsThis(), self.le_card.text()))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql сохр. карты", sql_info.msg, QMessageBox.Ok)
                    return False

        self.main.ui_update()
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()

    def of_list_worker(self, item):
        self.le_worker.setWhatsThis(str(item[0]))
        self.le_worker.setText(item[1])