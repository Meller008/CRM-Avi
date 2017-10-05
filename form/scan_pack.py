from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from form import pack, article
from function import my_sql
from classes.my_class import User


scan_pack = loadUiType(getcwd() + '/ui/scan_pack.ui')[0]
list_article = loadUiType(getcwd() + '/ui/scan_pack_list_article.ui')[0]


class ScanPack(QDialog, scan_pack):
    def __init__(self):
        super(ScanPack, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.scan_article = True
        self.access()

    def access(self):
        for item in User().access_list(self.__class__.__name__):
            a = getattr(self, item["atr1"])
            if item["atr2"]:
                a = getattr(a, item["atr2"])

            if item["value"]:
                if item["value"] == "True":
                    val = True
                elif item["value"] == "False":
                    val = False
                else:
                    val = item["value"]
                a(val)
            else:
                a()

    def access_search_article(self, bol):
        self.scan_article = bol

    def ui_acc_id(self):
        try:
            id_scan = int(self.le_number.text())
        except:
            return False

        query = """SELECT COUNT(Id) FROM pack WHERE Id = %s"""
        count_id = my_sql.sql_select(query, (id_scan, ))
        if "mysql.connector.errors" in str(type(count_id)):
            QMessageBox.critical(self, "Ошибка sql поиска пачки", count_id.msg, QMessageBox.Ok)
            return False

        if count_id[0][0] != 1:
            if self.scan_article:
                res = QMessageBox.information(self, "Ошибка номера", "Нет пачки с таким номером, искать артикул?", QMessageBox.Yes, QMessageBox.No)
                if res == QMessageBox.Yes:
                    self.search_article()
                self.le_number.setText("")
                return False
            else:
                QMessageBox.information(self, "Ошибка номера", "Нет пачки с таким номером", QMessageBox.Ok)
                return False

        self.le_number.setText("")
        self.pack = pack.PackBrows(pack_id=id_scan)
        self.pack.setModal(True)
        self.pack.show()

    def search_article(self):
        barcode = int(self.le_number.text())
        query = """SELECT COUNT(Barcode) FROM product_article_parametrs WHERE Barcode = %s"""
        count_id = my_sql.sql_select(query, (barcode, ))
        if "mysql.connector.errors" in str(type(count_id)):
            QMessageBox.critical(self, "Ошибка sql поиска штрихкода", barcode.msg, QMessageBox.Ok)
            return False

        self.art_list = ListArticle()
        self.art_list.search_barcode(barcode)
        self.art_list.setModal(True)
        self.art_list.show()

    def keyPressEvent(self, event):
        if event.key() == 16777221 or event.key() == 16777220:
            self.ui_acc_id()
        event.accept()


class ListArticle(QDialog, list_article):
    def __init__(self):
        super(ListArticle, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.tw_list_article.horizontalHeader().resizeSection(0, 40)
        self.tw_list_article.horizontalHeader().resizeSection(1, 70)
        self.tw_list_article.horizontalHeader().resizeSection(2, 50)
        self.tw_list_article.horizontalHeader().resizeSection(3, 70)
        self.tw_list_article.horizontalHeader().resizeSection(4, 170)

    def ui_double_click(self, item):
        art_id = item.data(5)
        self.are_win = article.Article(self, art_id, dc_select=True)
        self.are_win.setWindowModality(QtCore.Qt.ApplicationModal)
        self.are_win.show()

    def search_barcode(self, barcode):
        query = """SELECT product_article.Id, product_article.Article, product_article_size.Size, product_article_parametrs.Name, product_article_parametrs.Client_Name
                      FROM product_article_parametrs LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE Barcode = %s"""
        article_sql = my_sql.sql_select(query, (barcode, ))
        if "mysql.connector.errors" in str(type(article_sql)):
            QMessageBox.critical(self, "Ошибка sql поиска артикула по штрихкоду", article_sql.msg, QMessageBox.Ok)
            return False

        if article_sql:
            self.set_table_info(article_sql)

    def set_table_info(self, article_list):

        self.tw_list_article.clearContents()
        self.tw_list_article.setRowCount(0)

        if not article_list:
            return False

        for table_typle in article_list:
            self.tw_list_article.insertRow(self.tw_list_article.rowCount())
            for column in range(len(table_typle)):
                text = str(table_typle[column])
                item = QTableWidgetItem(text)
                item.setData(5, table_typle[0])
                self.tw_list_article.setItem(self.tw_list_article.rowCount() - 1, column, item)

    def of_tree_select_article(self, art):
        self.close()
        self.destroy()