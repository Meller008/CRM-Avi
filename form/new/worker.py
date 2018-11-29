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


        self.pb_add_2.setIcon(QIcon(getcwd() + "/images/new2.png"))
        self.pb_add_2.setIconSize(QSize(25, 25))

        self.pb_change_2.setIcon(QIcon(getcwd() + "/images/change2.png"))
        self.pb_change_2.setIconSize(QSize(25, 25))

        self.pb_del_2.setIcon(QIcon(getcwd() + "/images/del2.png"))
        self.pb_del_2.setIconSize(QSize(25, 25))


        self.pb_add_3.setIcon(QIcon(getcwd() + "/images/new3.png"))
        self.pb_add_3.setIconSize(QSize(25, 25))

        self.pb_change_3.setIcon(QIcon(getcwd() + "/images/change3.png"))
        self.pb_change_3.setIconSize(QSize(25, 25))

        self.pb_del_3.setIcon(QIcon(getcwd() + "/images/del3.png"))
        self.pb_del_3.setIconSize(QSize(25, 25))
    
    def b1(self):
        self.pb_add.setIconSize(QSize(15, 15))
        self.pb_change.setIconSize(QSize(15, 15))
        self.pb_del.setIconSize(QSize(15, 15))
        self.pb_add_2.setIconSize(QSize(15, 15))
        self.pb_change_2.setIconSize(QSize(15, 15))
        self.pb_del_2.setIconSize(QSize(15, 15))
        self.pb_add_3.setIconSize(QSize(15, 15))
        self.pb_change_3.setIconSize(QSize(15, 15))
        self.pb_del_3.setIconSize(QSize(15, 15))
        
    def b2(self):
        self.pb_add.setIconSize(QSize(25, 25))
        self.pb_change.setIconSize(QSize(25, 25))
        self.pb_del.setIconSize(QSize(25, 25))
        self.pb_add_2.setIconSize(QSize(25, 25))
        self.pb_change_2.setIconSize(QSize(25, 25))
        self.pb_del_2.setIconSize(QSize(25, 25))
        self.pb_add_3.setIconSize(QSize(25, 25))
        self.pb_change_3.setIconSize(QSize(25, 25))
        self.pb_del_3.setIconSize(QSize(25, 25))
        
    def b3(self):
        self.pb_add.setIconSize(QSize(32, 32))
        self.pb_change.setIconSize(QSize(32, 32))
        self.pb_del.setIconSize(QSize(32, 32))
        self.pb_add_2.setIconSize(QSize(32, 32))
        self.pb_change_2.setIconSize(QSize(32, 32))
        self.pb_del_2.setIconSize(QSize(32, 32))
        self.pb_add_3.setIconSize(QSize(32, 32))
        self.pb_change_3.setIconSize(QSize(32, 32))
        self.pb_del_3.setIconSize(QSize(32, 32))
        
    def b4(self):
        self.pb_add.setIconSize(QSize(40, 40))
        self.pb_change.setIconSize(QSize(40, 40))
        self.pb_del.setIconSize(QSize(40, 40))
        self.pb_add_2.setIconSize(QSize(40, 40))
        self.pb_change_2.setIconSize(QSize(40, 40))
        self.pb_del_2.setIconSize(QSize(40, 40))
        self.pb_add_3.setIconSize(QSize(40, 40))
        self.pb_change_3.setIconSize(QSize(40, 40))
        self.pb_del_3.setIconSize(QSize(40, 40))