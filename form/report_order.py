from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog, QProgressDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QBrush, QColor
import re
from decimal import Decimal
import datetime
import openpyxl
from openpyxl.styles import Border, Side, Font, Alignment, PatternFill
from openpyxl.worksheet.pagebreak import Break
from copy import copy
from function import my_sql, to_excel
from form.templates import table, list
from form import clients, article
import num2t4ru

need_article = loadUiType(getcwd() + '/ui/report_need_article_order.ui')[0]


class NeedArticleOrder(QMainWindow, need_article):
    def __init__(self):
        super(NeedArticleOrder, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))