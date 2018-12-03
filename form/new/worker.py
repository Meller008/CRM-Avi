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

        self.pb_add_list.setIcon(QIcon(getcwd() + "/images/add_list.png"))
        self.pb_add_list.setIconSize(QSize(30, 30))

        self.pb_edit_list.setIcon(QIcon(getcwd() + "/images/edit_list.png"))
        self.pb_edit_list.setIconSize(QSize(30, 30))

        self.pb_del_list.setIcon(QIcon(getcwd() + "/images/del_list.png"))
        self.pb_del_list.setIconSize(QSize(30, 30))

        self.pb_add_doc.setIcon(QIcon(getcwd() + "/images/new_doc.png"))
        self.pb_add_doc.setIconSize(QSize(30, 30))

        self.pb_change_doc.setIcon(QIcon(getcwd() + "/images/edit_doc.png"))
        self.pb_change_doc.setIconSize(QSize(30, 30))

        self.pb_del_doc.setIcon(QIcon(getcwd() + "/images/del_doc.png"))
        self.pb_del_doc.setIconSize(QSize(30, 30))

        self.pb_copy_doc.setIcon(QIcon(getcwd() + "/images/copy_doc.png"))
        self.pb_copy_doc.setIconSize(QSize(30, 30))

        self.pb_filter.setIcon(QIcon(getcwd() + "/images/filter.png"))
        self.pb_filter.setIconSize(QSize(30, 30))

        self.pb_menu.setIcon(QIcon(getcwd() + "/images/menu.png"))
        self.pb_menu.setIconSize(QSize(30, 30))


