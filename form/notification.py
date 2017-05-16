from os import getcwd
from PyQt5.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5.uic import loadUiType
from form import staff
from PyQt5.QtGui import QIcon, QTextCharFormat, QColor, QBrush
from PyQt5.QtCore import Qt, QDate
from function import my_sql

work_notif_calendar_class, work_notif_calendar_base_class = loadUiType(getcwd() + '/ui/work_notification_calendar.ui')


class WorkCalendar(QDialog, work_notif_calendar_class):
    def __init__(self):
        super(WorkCalendar, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.calendar.setGridVisible(True)
        self.tableWidget.horizontalHeader().resizeSection(0, 30)
        self.tableWidget.horizontalHeader().resizeSection(1, 170)
        self.tableWidget.horizontalHeader().resizeSection(2, 85)
        self.tableWidget.horizontalHeader().resizeSection(3, 70)
        self.tableWidget.sortItems(3)
        self.set_info()

    def update_calendar(self):
        self.set_info()

    def set_info(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        to_date = QDate.currentDate()
        notif_date = (to_date.addDays(15).toString(Qt.ISODate), to_date.addDays(-15).toString(Qt.ISODate))
        query = "SELECT staff_worker_info.Id, CONCAT(staff_worker_info.Last_Name, ' ', staff_worker_info.First_Name),'Патент', staff_worker_patent.Date_Ending " \
                "FROM staff_worker_patent LEFT JOIN staff_worker_info ON staff_worker_patent.Worker_Info_Id = staff_worker_info.Id" \
                " WHERE Date_Ending <= %s AND Date_Ending >= %s AND staff_worker_info.Leave = 0"
        notif_1 = my_sql.sql_select(query, notif_date)
        if "mysql.connector.errors" in str(type(notif_1)):
            QMessageBox.critical(self, "Ошибка sql", notif_1.msg, QMessageBox.Ok)
            return False
        self.paint_date(notif_1, (85, 255, 127))
        self.set_table(notif_1, (85, 255, 127))

        query = "SELECT staff_worker_info.Id, CONCAT(staff_worker_info.Last_Name, ' ', staff_worker_info.First_Name), 'Регистрация', staff_worker_registraton.Date_Validity_To " \
                "FROM staff_worker_registraton LEFT JOIN staff_worker_info ON staff_worker_registraton.Worker_Info_id = staff_worker_info.Id" \
                " WHERE Date_Validity_To <= %s AND Date_Validity_To >= %s AND staff_worker_info.Leave = 0"
        notif_1 = my_sql.sql_select(query, notif_date)
        if "mysql.connector.errors" in str(type(notif_1)):
            QMessageBox.critical(self, "Ошибка sql", notif_1.msg, QMessageBox.Ok)
            return False
        self.paint_date(notif_1, (255, 85, 255))
        self.set_table(notif_1, (255, 85, 255))

        query = "SELECT staff_worker_info.Id, CONCAT(staff_worker_info.Last_Name, ' ', staff_worker_info.First_Name), 'Миграционка', staff_worker_migration.Date_Validity_To " \
                "FROM staff_worker_migration LEFT JOIN staff_worker_info ON staff_worker_migration.Worker_Info_Id = staff_worker_info.Id " \
                "WHERE Date_Validity_To <= %s AND Date_Validity_To >= %s AND staff_worker_info.Leave = 0"
        notif_1 = my_sql.sql_select(query, notif_date)
        if "mysql.connector.errors" in str(type(notif_1)):
            QMessageBox.critical(self, "Ошибка sql", notif_1.msg, QMessageBox.Ok)
            return False
        self.paint_date(notif_1, (255, 255, 127))
        self.set_table(notif_1, (255, 255, 127))

        query = "SELECT staff_worker_info.Id, CONCAT(staff_worker_info.Last_Name, ' ', staff_worker_info.First_Name), 'Личное', staff_worker_notification.Date " \
                "FROM staff_worker_notification LEFT JOIN staff_worker_info ON staff_worker_notification.Worker_Info_Id = staff_worker_info.Id " \
                "WHERE Date <= %s AND Date >= %s"
        notif_1 = my_sql.sql_select(query, notif_date)
        if "mysql.connector.errors" in str(type(notif_1)):
            QMessageBox.critical(self, "Ошибка sql", notif_1.msg, QMessageBox.Ok)
            return False
        self.paint_date(notif_1, (0, 255, 255))
        self.set_table(notif_1, (0, 255, 255))

        query = "SELECT staff_worker_info.Id, CONCAT(staff_worker_info.Last_Name, ' ', staff_worker_info.First_Name), 'ДР', staff_worker_info.Date_Birth " \
                "FROM staff_worker_info WHERE Date_Birth <= %s AND Date_Birth >= %s"
        notif_1 = my_sql.sql_select(query, notif_date)
        if "mysql.connector.errors" in str(type(notif_1)):
            QMessageBox.critical(self, "Ошибка sql", notif_1.msg, QMessageBox.Ok)
            return False
        self.paint_date(notif_1, (255, 167, 167))
        self.set_table(notif_1, (255, 167, 167))

    def paint_date(self, date, color):
        color = QColor(color[0], color[1], color[2], 255)
        brush = QBrush()
        brush.setColor(color)
        fomat = QTextCharFormat()
        fomat.setBackground(brush)
        for d in date:
            notif_date = d[3]
            self.calendar.setDateTextFormat(notif_date, fomat)

    def set_table(self, date, color):
        brush = QBrush(QColor(color[0], color[1], color[2], 255))
        for row in range(len(date)):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for col in range(4):
                item = QTableWidgetItem(str(date[row][col]))
                a = str(date[row][col])
                item.setBackground(brush)
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, col, item)

    def change_date(self, select_date):
        a = -1
        b = -1

        self.tableWidget.clearSelection()
        for row in range(self.tableWidget.rowCount()):
            date_item = self.tableWidget.item(row, 3)
            if select_date.toString(Qt.ISODate) == date_item.text():
                if a == -1:
                    a = row
                    b = row - 1
                b += 1

        if a != -1 and b != -1:
            self.tableWidget.setRangeSelected(QTableWidgetSelectionRange(a, 0, b, 3), True)
            self.tabWidget.setCurrentIndex(1)

    def double_click_notification(self, row):
        id = self.tableWidget.item(row, 0).text()
        self.one_staff = staff.OneStaff(self, True)
        self.one_staff.set_add_settings()
        if self.one_staff.insert_info(id):
            self.one_staff.setWindowModality(Qt.ApplicationModal)
            self.one_staff.show()
