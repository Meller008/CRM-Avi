from os import getcwd, path, mkdir, listdir
from form.templates import tree
from form import operation, supply_material, supply_accessories, print_label
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QMainWindow, QInputDialog, QTableWidgetItem, QShortcut, QListWidgetItem, QLineEdit, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5 import QtCore
from function import my_sql, table_to_html
from classes.my_class import User
from classes import print_qt

test_window_class = loadUiType(getcwd() + '/ui/test.ui')[0]


class TestWindow(QMainWindow, test_window_class):
    def __init__(self):
        super(TestWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.comboBox.insertItem(0, "Выбрать", -1)
        self.comboBox.setCurrentIndex(0)

        self.tableWidget.setCurrentCell(10, 0)

    def ui_t1(self):
        for i in range(300, 100, -1):
            self.tableWidget.resize(50, i)

    def ui_c2(self):
        print("123")


class TableItem(QTableWidgetItem):

    def __init__(self, title, parent):
        super().__init__(title, parent)

    # def mouseMoveEvent(self, e):
    #
    #     if e.buttons() != Qt.RightButton:
    #         return
    #
    #     mimeData = QMimeData()
    #
    #     drag = QDrag(self)
    #     drag.setMimeData(mimeData)
    #     drag.setHotSpot(e.pos() - self.rect().topLeft())
    #
    #     dropAction = drag.exec_(Qt.MoveAction)
    #
    #
    # def mousePressEvent(self, e):
    #
    #     QPushButton.mousePressEvent(self, e)
    #
    #     if e.button() == Qt.LeftButton:
    #         print('press')