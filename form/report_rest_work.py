from os import getcwd
from form import article
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QMainWindow,  QTableWidgetItem, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, QDate, QCoreApplication
from function import my_sql, table_to_html
from classes import cut, print_qt
from decimal import Decimal

rest_work_class = loadUiType(getcwd() + '/ui/report_rest_work.ui')[0]
rest_one_work_class = loadUiType(getcwd() + '/ui/report_rest_one_work.ui')[0]


class ReportRestWork(QMainWindow, rest_work_class):
    def __init__(self):
        super(ReportRestWork, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_settings()

    def start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

        self.tw_work.horizontalHeader().resizeSection(0, 110)
        self.tw_work.horizontalHeader().resizeSection(1, 110)
        self.tw_work.horizontalHeader().resizeSection(2, 70)
        self.tw_work.horizontalHeader().resizeSection(3, 70)
        self.tw_work.horizontalHeader().resizeSection(4, 70)

    def ui_calc(self):
        query = """SELECT staff_worker_info.Id, staff_worker_info.Last_Name,
                        min((cut.Weight_Rest * 100) / (cut.Weight_Rest + (SELECT SUM(Weight) FROM pack WHERE pack.Cut_Id = cut.Id))),
                        avg((cut.Weight_Rest * 100) / (cut.Weight_Rest + (SELECT SUM(Weight) FROM pack WHERE pack.Cut_Id = cut.Id))),
                        max((cut.Weight_Rest * 100) / (cut.Weight_Rest + (SELECT SUM(Weight) FROM pack WHERE pack.Cut_Id = cut.Id)))
                      FROM cut LEFT JOIN staff_worker_info ON cut.Worker_Id = staff_worker_info.Id
                      WHERE cut.Date_Cut >= %s AND  cut.Date_Cut <= %s
                      GROUP BY cut.Worker_Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate)))
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение значение обрези", sql_info.msg, QMessageBox.Ok)
                return False

        self.tw_work.clearContents()
        self.tw_work.setRowCount(0)

        if not sql_info:
            return False

        list_awg = []

        for table_typle in sql_info:
            self.tw_work.insertRow(self.tw_work.rowCount())
            list_awg.append(table_typle[3])
            for column in range(1, len(table_typle)):
                if isinstance(table_typle[column], Decimal):
                    text = str(round(float(table_typle[column]), 4))
                else:
                    text = str(table_typle[column])
                item = QTableWidgetItem(text)
                item.setData(5, table_typle[0])
                self.tw_work.setItem(self.tw_work.rowCount() - 1, column - 1, item)

        query = """SELECT min((cut.Weight_Rest * 100) / (cut.Weight_Rest + (SELECT SUM(Weight) FROM pack WHERE pack.Cut_Id = cut.Id))),
                        avg((cut.Weight_Rest * 100) / (cut.Weight_Rest + (SELECT SUM(Weight) FROM pack WHERE pack.Cut_Id = cut.Id))),
                        max((cut.Weight_Rest * 100) / (cut.Weight_Rest + (SELECT SUM(Weight) FROM pack WHERE pack.Cut_Id = cut.Id)))
                      FROM cut WHERE cut.Date_Cut >= %s AND  cut.Date_Cut <= %s"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate)))
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение значение обрези", sql_info.msg, QMessageBox.Ok)
                return False

        if not sql_info:
            return False

        self.le_min.setText(str(round(sql_info[0][0], 4)))
        self.le_awg.setText(str(round(sql_info[0][1], 4)))
        self.le_max.setText(str(round(sql_info[0][2], 4)))

    def ui_double_click(self, row):
        self.work = RestOneWork(self.tw_work.item(row, 0).data(5), self.de_date_from.date(), self.de_date_to.date())
        self.work.setModal(True)
        self.work.show()

        if not self.work.exec_():
            return False

    def ui_print(self):
        head = "Средняя обрезь %s-%s" % (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate))

        up_html = """
          <table>
          <tr>
          <th>Минимальное</th><th>Среднее</th><th>Максимальное</th>
          </tr>
          <tr>
          <td>#min#</td><td>#avg#</td><td>#max#</td>
          </tr>
          </table>"""

        up_html = up_html.replace("#min#", str(self.le_min.text()))
        up_html = up_html.replace("#avg#", str(self.le_awg.text()))
        up_html = up_html.replace("#max#", str(self.le_max.text()))

        html = table_to_html.tab_html(self.tw_work, table_head=head, up_template=up_html)
        self.print_class = print_qt.PrintHtml(self, html)


class RestOneWork(QDialog, rest_one_work_class):
    def __init__(self, work_id, date_from, date_to):
        super(RestOneWork, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_settings()
        self.set_sql_info(work_id, date_from, date_to)

    def start_settings(self):
        self.tableWidget.horizontalHeader().resizeSection(0, 60)
        self.tableWidget.horizontalHeader().resizeSection(1, 60)
        self.tableWidget.horizontalHeader().resizeSection(2, 70)

    def set_sql_info(self, work_id, date_from, date_to):
        query = """SELECT cut.Id , pack.Number,
                        (cut.Weight_Rest * 100) / (cut.Weight_Rest + (SELECT SUM(Weight) FROM pack WHERE pack.Cut_Id = cut.Id))
                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                      WHERE cut.Date_Cut >= %s AND  cut.Date_Cut <= %s AND cut.Worker_Id = %s"""
        sql_info = my_sql.sql_select(query, (date_from.toString(Qt.ISODate), date_to.toString(Qt.ISODate), work_id))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение значение обрези", sql_info.msg, QMessageBox.Ok)
            return False

        for table_typle in sql_info:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for column in range(len(table_typle)):
                if isinstance(table_typle[column], Decimal):
                    text = str(round(float(table_typle[column]), 4))
                else:
                    text = str(table_typle[column])
                item = QTableWidgetItem(text)
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, column, item)
