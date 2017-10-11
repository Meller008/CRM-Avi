from os import getcwd, path, mkdir, listdir
from form.templates import tree
from form import operation, supply_material, supply_accessories, print_label, article
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QMainWindow, QInputDialog, QTableWidgetItem, QShortcut, QListWidgetItem, QLineEdit, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt, QObject, QDate
from function import my_sql, table_to_html
from classes.my_class import User
from classes import print_qt, cut

sibest_class = loadUiType(getcwd() + '/ui/report_sibestoimost.ui')[0]


class ReportSibestoimost(QMainWindow, sibest_class):
    def __init__(self):
        super(ReportSibestoimost, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.de_date_in.setDate(QDate.currentDate().addMonths(-3))
        self.de_date_from.setDate(QDate.currentDate())

    def ui_calc(self):
        query = "SELECT cut.Id FROM cut"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения номеров кроя", sql_info.msg, QMessageBox.Ok)
            return False

        cut_list = []
        # получаем классы кроев из списка id плученных из sql
        for cut_id in sql_info:
            cut_list.append(cut.Cut(cut_id[0]))

        # Начинаем перебор кроев, в которых будем перебирать их пачки
        for cut_class in cut_list:
            cut_class.take_pack_sql()
            pack_list_class = cut_class.pack_list()

            # перебираем пачки кроя
            for pack_class in pack_list_class.values():
                self.table_widget.insertRow(self.table_widget.rowCount())

                item = QTableWidgetItem(str(cut_class.id()))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 0, item)
                item = QTableWidgetItem(str(pack_class.number_pack()))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 1, item)

    def ui_view_art(self):
        but_name = QObject.sender(self).objectName()

        self.article_list = article.ArticleList(self, True)
        self.article_list.setWindowModality(Qt.ApplicationModal)
        self.article_list.show()

    def build_sql_where(self):
        pass

    def of_tree_select_article(self, article):
        self.article_list.close()
        self.article_list.destroy()

