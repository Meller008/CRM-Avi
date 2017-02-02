from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import QDate, Qt
from function import my_sql

warehouse_change = loadUiType(getcwd() + '/ui/warehouse_rest_change.ui')[0]
warehouse_info = loadUiType(getcwd() + '/ui/warehouse_rest.ui')[0]


class WarehouseRest(QMainWindow, warehouse_info):
    def __init__(self):
        super(WarehouseRest, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_size_table()
        self.set_start_info()

    def set_size_table(self):
        self.tw_info.horizontalHeader().resizeSection(0, 35)
        self.tw_info.horizontalHeader().resizeSection(1, 70)
        self.tw_info.horizontalHeader().resizeSection(2, 70)
        self.tw_info.horizontalHeader().resizeSection(3, 240)

    def set_start_info(self):
        query = """SELECT Weight FROM rest_warehouse"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения склада", sql_info.msg, QMessageBox.Ok)
            return False

        self.le_weight.setText(str(sql_info[0][0]))

        query = """SELECT Id, Balance, Date, Note, Cut_Id FROM transaction_records_rest ORDER BY Date DESC LIMIT 30"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения информации", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_info.clearContents()
        self.tw_info.setRowCount(0)

        for row, info in enumerate(sql_info):
            self.tw_info.insertRow(row)
            if info[1] >= 0:
                color = QBrush(QColor(150, 255, 161, 255))
            else:
                color = QBrush(QColor(252, 141, 141, 255))

            new_table_item = QTableWidgetItem(str(info[0]))
            new_table_item.setData(-2, info[4])
            new_table_item.setBackground(color)
            self.tw_info.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(info[1]))
            new_table_item.setData(-2, info[4])
            new_table_item.setBackground(color)
            self.tw_info.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(info[2].strftime("%d.%m.%Y"))
            new_table_item.setData(-2, info[4])
            new_table_item.setBackground(color)
            self.tw_info.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(info[3]))
            new_table_item.setData(-2, info[4])
            new_table_item.setBackground(color)
            self.tw_info.setItem(row, 3, new_table_item)

    def ui_update(self):
        self.set_start_info()

    def ui_big_info(self):
        query = """SELECT Id, Balance, Date, Note, Cut_Id FROM transaction_records_rest ORDER BY Date DESC"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения информации", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_info.clearContents()
        self.tw_info.setRowCount(0)

        for row, info in enumerate(sql_info):
            self.tw_info.insertRow(row)
            if info[1] >= 0:
                color = QBrush(QColor(150, 255, 161, 255))
            else:
                color = QBrush(QColor(252, 141, 141, 255))

            new_table_item = QTableWidgetItem(str(info[0]))
            new_table_item.setData(-2, info[4])
            new_table_item.setBackground(color)
            self.tw_info.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(info[1]))
            new_table_item.setData(-2, info[4])
            new_table_item.setBackground(color)
            self.tw_info.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(info[2].strftime("%d.%m.%Y"))
            new_table_item.setData(-2, info[4])
            new_table_item.setBackground(color)
            self.tw_info.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(info[3]))
            new_table_item.setData(-2, info[4])
            new_table_item.setBackground(color)
            self.tw_info.setItem(row, 3, new_table_item)

    def ui_change(self):
        self.warehouse_change = WarehouseChange(self)
        self.warehouse_change.setModal(True)
        self.warehouse_change.show()


class WarehouseChange(QDialog, warehouse_change):
    def __init__(self, main):
        super(WarehouseChange, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main

        self.de_date.setDate(QDate.currentDate())

    def ui_acc(self):
        if self.le_balance.text() != "":
            sql_connect_transaction = my_sql.sql_start_transaction()
            query = """UPDATE rest_warehouse SET Weight = Weight + %s"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.le_balance.text(), ))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql не смог изменить обрезь", sql_info.msg, QMessageBox.Ok)
                return False

            query = """INSERT INTO transaction_records_rest (Cut_Id, Date, Balance, Note) VALUES (NULL, %s, %s, %s)"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.de_date.date().toString(Qt.ISODate), self.le_balance.text(), self.le_note.text()))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql не смог сохранить запись об изменениях", sql_info.msg, QMessageBox.Ok)
                return False

            my_sql.sql_commit_transaction(sql_connect_transaction)
            self.main.ui_update()

        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()