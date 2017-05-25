from os import getcwd
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QTableWidgetItem, QLineEdit, QSizePolicy, QWidget
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QBrush, QColor, QIcon, QTextCharFormat
from PyQt5.QtCore import Qt, QDate, QDateTime
from function import my_sql
from form import provider, comparing, staff
from form.templates import table, list
from decimal import Decimal
import re


staff_card = loadUiType(getcwd() + '/ui/staff_card.ui')[0]
staff_traffic = loadUiType(getcwd() + '/ui/staff_traffic.ui')[0]
staff_traffic_data = loadUiType(getcwd() + '/ui/staff_traffic_data.ui')[0]


class StaffCardList(table.TableList):
    def set_settings(self):

        self.filter = None

        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.pb_filter.deleteLater()

        self.setWindowTitle("Настройка карт")  # Имя окна
        self.resize(350, 270)
        self.toolBar.setStyleSheet("background-color: rgb(129, 66, 255);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Фамилия", 100), ("Имя", 100), ("Карта", 100))

        self.query_table_all = """SELECT staff_worker_kard.Worker_Id, staff_worker_info.Last_Name, staff_worker_info.First_Name, staff_worker_kard.Card_Id
                                      FROM staff_worker_kard
                                      LEFT JOIN staff_worker_info ON staff_worker_kard.Worker_Id = staff_worker_info.Id"""

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT staff_worker_kard.Worker_Id, staff_worker_info.Last_Name, staff_worker_info.First_Name, staff_worker_kard.Card_Id
                                      FROM staff_worker_kard
                                      LEFT JOIN staff_worker_info ON staff_worker_kard.Worker_Id = staff_worker_info.Id"""

        self.query_table_dell = "DELETE FROM staff_worker_kard WHERE Worker_Id = %s"

    def ui_add_table_item(self):  # Добавить предмет
        self.new_card = ChangeCard(self)
        self.new_card.setModal(True)
        self.new_card.show()

    def ui_change_table_item(self, id=False):  # изменить элемент
        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите операцию который хотите изменить", QMessageBox.Ok)
                return False

        self.change_card = ChangeCard(self, item_id)
        self.change_card.setWindowModality(Qt.ApplicationModal)
        self.change_card.show()


class StaffTraffic(QDialog, staff_traffic):
    def __init__(self):
        super(StaffTraffic, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.sql_traffic = None
        self.select_data = None
        self.last_id = None

        self.set_start_settings()

    def set_start_settings(self):
        self.tw_traffic.horizontalHeader().resizeSection(0, 40)

    def set_work_traffic(self, id, update=False):
        if self.select_data is None or self.last_id != id or update \
                or self.calendarWidget.selectedDate().month() != self.select_data.month() or self.calendarWidget.selectedDate().year() != self.select_data.year():
            data = self.calendarWidget.selectedDate()
            query = """SELECT staff_worker_traffic.Id, staff_worker_traffic.Position, staff_worker_traffic.Data, staff_worker_traffic.Table_Data
                          FROM staff_worker_traffic LEFT JOIN staff_worker_info ON staff_worker_traffic.Worker_Id = staff_worker_info.Id
                          WHERE staff_worker_traffic.Worker_Id = %s AND staff_worker_traffic.Data >= %s AND staff_worker_traffic.Data <= %s
                          ORDER BY staff_worker_traffic.Data"""
            sql_param = (id, data.toString("yyyy-MM-01-00-00-00"), data.toString("yyyy-MM-%s-23-59-59" % data.daysInMonth()))
            self.sql_traffic = my_sql.sql_select(query, sql_param)
            if "mysql.connector.errors" in str(type(self.sql_traffic)):
                QMessageBox.critical(self, "Ошибка sql получения записей", self.sql_traffic.msg, QMessageBox.Ok)
                return False

            color = (79, 255, 185)
            color = QColor(color[0], color[1], color[2], 200)
            brush = QBrush()
            brush.setColor(color)
            fomat = QTextCharFormat()
            fomat.setBackground(brush)
            for data in self.sql_traffic:
                self.calendarWidget.setDateTextFormat(data[2], fomat)

        if self.calendarWidget.selectedDate() != self.select_data or self.last_id != id or update:
            self.last_id = id
            self.select_data = self.calendarWidget.selectedDate()
            self.tw_traffic.clearContents()
            self.tw_traffic.setRowCount(0)
            for data in self.sql_traffic:
                if data[2].strftime("%d.%m.%Y") == self.select_data.toString("dd.MM.yyyy"):
                    self.tw_traffic.insertRow(self.tw_traffic.rowCount())

                    new_table_item = QTableWidgetItem(str(data[1]))
                    new_table_item.setData(-2, data[0])
                    self.tw_traffic.setItem(self.tw_traffic.rowCount()-1, 0, new_table_item)

                    new_table_item = QTableWidgetItem(data[2].strftime("%d.%m.%Y %H:%M"))
                    new_table_item.setData(-2, data[0])
                    self.tw_traffic.setItem(self.tw_traffic.rowCount()-1, 1, new_table_item)

                    tab_date = data[3].strftime("%d.%m.%Y %H:%M") if data[3] else ""
                    new_table_item = QTableWidgetItem(tab_date)
                    new_table_item.setData(-2, data[0])
                    self.tw_traffic.setItem(self.tw_traffic.rowCount()-1, 2, new_table_item)

    def ui_select_date(self):
        self.set_work_traffic(int(self.le_worker.whatsThis()))

    def ui_add_date(self):
        self.cut_passport = StaffTrafficData(self, int(self.le_worker.whatsThis()))
        self.cut_passport.setModal(True)
        self.cut_passport.show()

    def ui_change_date(self):
        try:
            id = int(self.tw_traffic.item(self.tw_traffic.currentRow(), 0).data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите запись", QMessageBox.Ok)
            return False

        self.cut_passport = StaffTrafficData(self, int(self.le_worker.whatsThis()), id)
        self.cut_passport.setModal(True)
        self.cut_passport.show()

    def ui_view_list_worker(self):
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_acc(self):
        self.close()
        self.destroy()

    def of_list_worker(self, item):
        self.le_worker.setWhatsThis(str(item[0]))
        self.le_worker.setText(item[1])
        self.set_work_traffic(item[0])


class StaffTrafficData(QDialog, staff_traffic_data):
    def __init__(self, main, worker_id, traffic_id=None):
        super(StaffTrafficData, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        self.worker = worker_id
        self.traffic_id = traffic_id

        self.set_settings()

    def set_settings(self):
        if self.traffic_id:
            query = """SELECT Position, Data, Table_Data FROM staff_worker_traffic WHERE Id = %s"""
            sql_traffic = my_sql.sql_select(query, (self.traffic_id, ))
            if "mysql.connector.errors" in str(type(sql_traffic)):
                QMessageBox.critical(self, "Ошибка sql получения записей", sql_traffic.msg, QMessageBox.Ok)
                return False
            self.le_position.setText(str(sql_traffic[0][0]))
            self.dt_date.setDateTime(sql_traffic[0][1])
            if sql_traffic[0][2]:
                self.dt_tabel_date.setDateTime(sql_traffic[0][2])
            else:
                min = sql_traffic[0][1].minute
                if 0 <= min <= 15:
                    tab_date = sql_traffic[0][1].replace(minute=0)
                elif 16 <= min <= 45:
                    tab_date = sql_traffic[0][1].replace(minute=30)
                else:
                    tab_date = sql_traffic[0][1].replace(minute=0)
                    tab_date = tab_date(hour=(sql_traffic[0][1].hour+1))

                self.dt_tabel_date.setDateTime(tab_date)

        else:
            self.dt_date.setDateTime(QDateTime.currentDateTime())
            self.dt_tabel_date.setDateTime(QDateTime.currentDateTime())

    def ui_acc(self):
        if self.traffic_id:
            query = """UPDATE staff_worker_traffic SET Position = %s, Data = %s, Table_Data = %s, Worker_Id = %s WHERE Id = %s"""
            sql_param = (self.le_position.text(), self.dt_date.dateTime().toPyDateTime(), self.dt_tabel_date.dateTime().toPyDateTime(), self.worker, self.traffic_id)
            sql_traffic = my_sql.sql_change(query, sql_param)
            if "mysql.connector.errors" in str(type(sql_traffic)):
                QMessageBox.critical(self, "Ошибка sql изменение записи", sql_traffic.msg, QMessageBox.Ok)
                return False
            self.main.set_work_traffic(self.worker, True)
        else:
            query = """INSERT INTO staff_worker_traffic (Position, Data, Table_Data, Worker_Id) VALUES (%s, %s, %s, %s)"""
            sql_param = (self.le_position.text(), self.dt_date.dateTime().toPyDateTime(), self.dt_tabel_date.dateTime().toPyDateTime(), self.worker)
            sql_traffic = my_sql.sql_change(query, sql_param)
            if "mysql.connector.errors" in str(type(sql_traffic)):
                QMessageBox.critical(self, "Ошибка sql лобавление записи", sql_traffic.msg, QMessageBox.Ok)
                return False
            self.main.set_work_traffic(self.worker, True)

        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()


class ChangeCard(QDialog, staff_card):
    def __init__(self, main, id=None):
        super(ChangeCard, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.main = main
        self.id = id
        self.set_start_settings()

    def set_start_settings(self):
        if self.id:
            query = """SELECT CONCAT(Last_Name, ' ', First_Name), staff_worker_kard.Card_Id FROM staff_worker_info
                          LEFT JOIN staff_worker_kard ON staff_worker_info.Id = staff_worker_kard.Worker_Id
                          WHERE Id = %s"""
            sql_info = my_sql.sql_select(query, (self.id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql сохр. карты", sql_info.msg, QMessageBox.Ok)
                    return False
            self.le_worker.setWhatsThis(str(self.id))
            self.le_worker.setText(sql_info[0][0])
            self.le_card.setText(sql_info[0][1])

    def ui_view_worker(self):
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_acc(self):
        if self.id:
            query = "UPDATE staff_worker_kard SET Worker_Id = %s, Card_Id = %s WHERE Worker_Id = %s"
            sql_info = my_sql.sql_change(query, (self.le_worker.whatsThis(), self.le_card.text(), self.id))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql сохр. карты", sql_info.msg, QMessageBox.Ok)
                    return False
        else:
            query = "INSERT INTO staff_worker_kard (Worker_Id, Card_Id) VALUES (%s, %s)"
            sql_info = my_sql.sql_change(query, (self.le_worker.whatsThis(), self.le_card.text()))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql сохр. карты", sql_info.msg, QMessageBox.Ok)
                    return False

        self.main.ui_update()
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()

    def of_list_worker(self, item):
        self.le_worker.setWhatsThis(str(item[0]))
        self.le_worker.setText(item[1])