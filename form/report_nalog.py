from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon, QColor, QBrush
from function import my_sql
from function import table_to_html, to_excel
from classes import print_qt
import calendar

report_nalog_class = loadUiType(getcwd() + '/ui/report_nalog.ui')[0]


class ReportNalog(QMainWindow, report_nalog_class):
    def __init__(self):
        super(ReportNalog, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

        self.tableWidget.horizontalHeader().resizeSection(0, 90)
        self.tableWidget.horizontalHeader().resizeSection(1, 90)
        self.tableWidget.horizontalHeader().resizeSection(2, 70)
        self.tableWidget.horizontalHeader().resizeSection(3, 70)
        self.tableWidget.horizontalHeader().resizeSection(4, 50)
        self.tableWidget.horizontalHeader().resizeSection(5, 60)

    def ui_calc(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        query = """SELECT Last_Name, First_Name, Date_Recruitment, If(`Leave` = 0, NULL, Date_Leave)
                    FROM staff_worker_info
                    WHERE Date_Recruitment <= %s AND (Date_Leave >= %s OR `Leave` = 0 )"""
        sql_info = my_sql.sql_select(query, (self.de_date_to.date().toPyDate(), self.de_date_from.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения работников", sql_info.msg, QMessageBox.Ok)
            return False

        nal = int(self.le_nalog.text())
        day_mon = calendar.monthrange(self.de_date_to.date().toPyDate().year, self.de_date_to.date().toPyDate().month)[1]
        for work in sql_info:

            # проверяем какую дату брать первой
            if work[2] <= self.de_date_from.date().toPyDate():
                date_from = self.de_date_from.date().toPyDate()
            else:
                date_from = work[2]

            # проверяем какую дату брать второй
            if work[3] is None:
                date_to = self.de_date_to.date().toPyDate()
            elif work[3] >= self.de_date_to.date().toPyDate():
                date_to = self.de_date_to.date().toPyDate()
            else:
                date_to = work[3]

            day = date_to - date_from
            day = day.days + 1

            if day == day_mon:
                str_nal = str(nal)
            else:
                str_nal = str(round(nal - ((day_mon - day) * (nal / day_mon)), 2))

            if str_nal != self.le_nalog.text() or day != day_mon:
                color = QBrush(QColor(255, 255, 153, 255))
            else:
                color = QBrush(QColor(150, 255, 161, 255))

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            item = QTableWidgetItem(work[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            item = QTableWidgetItem(work[1])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            item = QTableWidgetItem(work[2].strftime("%d.%m.%Y"))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            if work[3] is None:
                text = "Не уволен"
            else:
                text = work[3].strftime("%d.%m.%Y")
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

            item = QTableWidgetItem(str(day))
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

            item = QTableWidgetItem(str_nal)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, item)

    def ui_print(self):
        head = "Налог %s - %s" % (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate))

        html = table_to_html.tab_html(self.tableWidget, table_head=head)
        self.print_class = print_qt.PrintHtml(self, html)

    def ui_export(self):
        path = QFileDialog.getSaveFileName(self, "Сохранение")
        if path[0]:
            to_excel.table_to_excel(self.tableWidget, path[0])