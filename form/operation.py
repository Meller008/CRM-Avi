from os import getcwd, path, mkdir, listdir, startfile
from shutil import copy
from form import accessories_provider, staff
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QListWidgetItem, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QVariant
from function import my_sql

operation_class = loadUiType(getcwd() + '/ui/operation.ui')[0]


class OperationList(QMainWindow, operation_class):
    def __init__(self):
        super(OperationList, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
