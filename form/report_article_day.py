from os import getcwd
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox, QMainWindow,  QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate
from function import my_sql
from classes import print_qt
from function import table_to_html, to_excel
from datetime import timedelta


class ReportArticleDay(QMainWindow):
    def __init__(self):
        super(ReportArticleDay, self).__init__()
        loadUi(getcwd() + '/ui/report_article_day.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_settings()

    def start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addDays(-10))
        self.de_date_to.setDate(QDate.currentDate())

        self.tableWidget.horizontalHeader().resizeSection(0, 65)
        self.tableWidget.horizontalHeader().resizeSection(1, 30)
        self.tableWidget.horizontalHeader().resizeSection(2, 60)

    def ui_calc(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)

        article_list = {}
        dat_start, dat_stop = self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()
        date_dict = {"article": None, "size": None, "param": None}

        while dat_start <= dat_stop:
            date_dict.update({dat_start: 0})

            col = self.tableWidget.columnCount()
            self.tableWidget.insertColumn(col)
            col_item = QTableWidgetItem(dat_start.strftime("%d.%m"))
            col_item.setData(5, dat_start)
            self.tableWidget.setHorizontalHeaderItem(col, col_item)
            self.tableWidget.horizontalHeader().resizeSection(col, 40)

            dat_start += timedelta(days=1)

        query = """SELECT product_article_parametrs.Id, product_article.Article, product_article_size.Size,
                            product_article_parametrs.Name, cut.Date_Cut, SUM(Pack_Value)
                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE cut.Date_Cut BETWEEN %s AND %s
                      GROUP BY product_article_parametrs.Id, cut.Date_Cut"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения артикулов в день", sql_info.msg, QMessageBox.Ok)
            return False

        for art in sql_info:
            if art[0] is None:
                continue

            if article_list.get(art[0]) is None:
                new_art = date_dict.copy()
                new_art.update({"article": art[1], "size": art[2], "param": art[3]})
                article_list.update({art[0]: new_art})

            article_list[art[0]][art[4]] = art[5]

            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)

            item = QTableWidgetItem(art[1])
            item.setData(5, art[0])
            self.tableWidget.setItem(row, 0, item)

            item = QTableWidgetItem(art[2])
            item.setData(5, art[0])
            self.tableWidget.setItem(row, 1, item)

            item = QTableWidgetItem(art[3])
            item.setData(5, art[0])
            self.tableWidget.setItem(row, 2, item)

        # перебираем строки
        for row in range(self.tableWidget.rowCount()):
            art_param = self.tableWidget.item(row, 0).data(5)

            # перебираем колонки
            for col in range(3, self.tableWidget.columnCount()):
                self.statusBar.showMessage("Строка %s колонка %s" % (row, col))
                search_date = self.tableWidget.horizontalHeaderItem(col).data(5)

                item = QTableWidgetItem(str(article_list[art_param][search_date]))
                self.tableWidget.setItem(row, col, item)

    def ui_print(self):
        head = "Покроено по дням %s-%s" % (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate))
        html = table_to_html.tab_html(self.tableWidget, table_head=head)
        self.print_class = print_qt.PrintHtml(self, html)

    def ui_export(self):
        path = QFileDialog.getSaveFileName(self, "Сохранение")
        if path[0]:
            to_excel.table_to_excel(self.tableWidget, path[0])



