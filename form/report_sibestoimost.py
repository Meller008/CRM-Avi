from os import getcwd, path, mkdir, listdir
from form.templates import tree
from form import operation, supply_material, supply_accessories, print_label, article
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QMainWindow, QInputDialog, QTableWidgetItem, QShortcut, QListWidgetItem, QLineEdit, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt, QObject
from function import my_sql, table_to_html
from classes.my_class import User
from classes import print_qt

sibest_class = loadUiType(getcwd() + '/ui/report_sibestoimost.ui')[0]


class ReportSibestoimost(QMainWindow, sibest_class):
    def __init__(self):
        super(ReportSibestoimost, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

    def ui_calc(self):
        pass

    def ui_view_art(self):
        but_name = QObject.sender(self).objectName()

        self.article_list = article.ArticleList(self, True)
        self.article_list.setWindowModality(Qt.ApplicationModal)
        self.article_list.show()

    def of_tree_select_article(self, article):
        self.article_list.close()
        self.article_list.destroy()

