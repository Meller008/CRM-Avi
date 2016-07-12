from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from function import my_sql

table_list_class = loadUiType(getcwd() + '/ui/templates ui/table.ui')[0]


class TableList(QMainWindow, table_list_class):
    def __init__(self, main_class=0, dc_select=False):
        super(TableList, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.main = main_class
        self.dc_select = dc_select
        self.set_settings()
        self.set_table_header()

    def set_settings(self):
        self.setWindowTitle("Список")  # Имя окна
        self.setS
        self.toolBar.setStyleSheet("background-color: rgb(126, 176, 127);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Клиент", 100), ("Пункт разгрузки", 150), ("Дата заказа", 80), ("Дата отгрузки", 80), ("Номер док.", 50), ("Стоймость", 80),
                                  ("Примечание", 200))


    def set_table_header(self):
        i = 0
        self.table_widget.clear()
        for headet_item in self.table_header_name:
            self.table_widget.insertColumn(i)
            self.table_widget.setHorizontalHeaderItem(i, QTableWidgetItem(headet_item[0]))
            self.table_widget.horizontalHeader().resizeSection(i, int(headet_item[1]))
            i += 1