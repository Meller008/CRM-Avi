from os import getcwd
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog, QPushButton
from PyQt5.QtCore import Qt, QDate, QDateTime, QObject, QSize
from PyQt5.QtGui import QIcon, QBrush, QColor


class WorkerListWindow(QDialog):
    def __init__(self):
        super(WorkerListWindow, self).__init__()
        loadUi(getcwd() + '/ui/new/worker_list.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.pb_add.setIcon(QIcon(getcwd() + "/images/new.png"))
        self.pb_add.setIconSize(QSize(25, 25))

        self.pb_change.setIcon(QIcon(getcwd() + "/images/change.png"))
        self.pb_change.setIconSize(QSize(25, 25))

        self.pb_del.setIcon(QIcon(getcwd() + "/images/del.png"))
        self.pb_del.setIconSize(QSize(25, 25))
