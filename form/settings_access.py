from os import getcwd
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from function import my_sql
from form import staff


class Access(QDialog):
    def __init__(self):
        super(Access, self).__init__()
        loadUi(getcwd() + '/ui/program_settings_access.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_settings()

    def start_settings(self):
        query = """SELECT Id, Name FROM staff_position"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql при получении должностей", sql_info.msg, QMessageBox.Ok)
            return False

        for position in sql_info:
            self.cb_position.addItem(position[1], position[0])

    def ui_view_worker(self):
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_select_position(self):
        query = """SELECT Id, Class, Atr1, Atr2, Atr_Value FROM access WHERE Staff_Position_Id = %s ORDER BY Class"""
        sql_info = my_sql.sql_select(query, (self.cb_position.currentData(),))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql при получении доступов", sql_info.msg, QMessageBox.Ok)
            return False

        self.worker = None
        self.position = self.cb_position.currentData()

        self.tw_access.clearContents()
        self.tw_access.setRowCount(0)

        for row, item in enumerate(sql_info):
            self.tw_access.insertRow(row)

            new_table_item = QTableWidgetItem(str(item[1]))
            new_table_item.setData(-2, item[0])
            self.tw_access.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(item[2]))
            new_table_item.setData(-2, item[0])
            self.tw_access.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(item[3]))
            new_table_item.setData(-2, item[0])
            self.tw_access.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(item[4]))
            new_table_item.setData(-2, item[0])
            self.tw_access.setItem(row, 3, new_table_item)

    def ui_add_position(self):
        if self.worker:
            self.add_position = AccessPosition(main=self, worker=self.worker)
        else:
            self.add_position = AccessPosition(main=self, position=self.position)

        self.add_position.setModal(True)
        self.add_position.show()

    def ui_double_click(self, row):
        if self.worker:
            self.change_position = AccessPosition(main=self, id=self.tw_access.item(row, 0).data(-2))
        else:
            self.change_position = AccessPosition(main=self, id=self.tw_access.item(row, 0).data(-2))

        self.change_position.setModal(True)

        self.change_position.le_class.setText(self.tw_access.item(row, 0).text())
        self.change_position.le_atr1.setText(self.tw_access.item(row, 1).text())
        self.change_position.le_atr2.setText(self.tw_access.item(row, 2).text())
        self.change_position.le_value.setText(self.tw_access.item(row, 3).text())

        self.change_position.show()

    def ui_del_position(self):
        try:
            item_id = self.tw_access.selectedItems()[0].data(-2)
        except:
            QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите удалить", QMessageBox.Ok)
            return False

        query = """DELETE FROM access WHERE Id = %s"""
        sql_info = my_sql.sql_change(query, (item_id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql при удалении позиции", sql_info.msg, QMessageBox.Ok)
            return False

        self.of_update()

    def select_worker(self):
        query = """SELECT Id, Class, Atr1, Atr2, Atr_Value FROM access WHERE Worker_Id = %s ORDER BY Class"""
        sql_info = my_sql.sql_select(query, (self.le_worker.whatsThis(), ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql при получении доступов", sql_info.msg, QMessageBox.Ok)
            return False

        self.worker = self.le_worker.whatsThis()
        self.position = None

        self.tw_access.clearContents()
        self.tw_access.setRowCount(0)

        for row, item in enumerate(sql_info):

            self.tw_access.insertRow(row)

            new_table_item = QTableWidgetItem(str(item[1]))
            new_table_item.setData(-2, item[0])
            self.tw_access.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(item[2]))
            new_table_item.setData(-2, item[0])
            self.tw_access.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(item[3]))
            new_table_item.setData(-2, item[0])
            self.tw_access.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(item[4]))
            new_table_item.setData(-2, item[0])
            self.tw_access.setItem(row, 3, new_table_item)

    def of_list_worker(self, item):
        self.le_worker.setWhatsThis(str(item[0]))
        self.le_worker.setText(item[1])
        self.select_worker()

    def of_update(self):
        if self.worker:
            self.select_worker()
        else:
            self.ui_select_position()


class AccessPosition(QDialog):
    def __init__(self, main, id=False, worker=None, position=None):
        super(AccessPosition, self).__init__()
        loadUi(getcwd() + '/ui/program_settings_access_one.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        self.id = id
        self.worker = worker
        self.position = position

    def ui_acc(self):
        if not self.id:
            if self.worker:
                sql_value = (self.worker, None, self.le_class.text(), self.le_atr1.text(), self.le_atr2.text(), self.le_value.text())
            elif self.position:
                sql_value = (None, self.position, self.le_class.text(), self.le_atr1.text(), self.le_atr2.text(), self.le_value.text())
            else:
                return False

            query = """INSERT INTO access (Worker_Id, Staff_Position_Id, Class, Atr1, Atr2, Atr_Value) VALUE (%s, %s, %s, %s, %s, %s)"""
            sql_info = my_sql.sql_change(query, sql_value)
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql при добавлении разрешения", sql_info.msg, QMessageBox.Ok)
                return False
        else:
            query = """UPDATE access SET Class = %s, Atr1 = %s, Atr2 = %s, Atr_Value = %s WHERE Id = %s"""
            sql_info = my_sql.sql_change(query, (self.le_class.text(), self.le_atr1.text(), self.le_atr2.text(), self.le_value.text(), self.id))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql при изменении разрешения", sql_info.msg, QMessageBox.Ok)
                return False

        self.main.of_update()
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()

