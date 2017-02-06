import datetime
from form.templates import table
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt
import re
from function import my_sql
from decimal import *


class Warehouse(table.TableList):
    def set_settings(self):
        self.setWindowTitle("Склад фурнитуры")  # Имя окна
        self.resize(470, 550)
        self.toolBar.setStyleSheet("background-color: rgb(251, 110, 255);")  # Цвет бара

        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.pb_add.deleteLater()
        self.pb_change.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_filter.deleteLater()

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Фурнитурра", 270), ("На складе", 90), ("Приходов", 70))

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT accessories_name.Id, accessories_name.Name, SUM(accessories_balance.BalanceValue), SUM(accessories_balance.BalanceValue > 0)
                                      FROM accessories_name LEFT JOIN accessories_supplyposition ON accessories_name.Id = accessories_supplyposition.accessories_NameId
                                        LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.accessories_SupplyPositionId
                                      GROUP BY accessories_name.Id
                                      ORDER BY accessories_name.Name"""
        self.query_table_dell = ""

    def ui_change_table_item(self, id=False):  # изменить элемент
        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
                return False

        self.supply_info = WarehouseSupplyPosition(self, False, item_id)
        self.supply_info.setWindowModality(Qt.ApplicationModal)
        self.supply_info.show()


class WarehouseSupplyPosition(table.TableList):

    def set_settings(self):
        self.setWindowTitle("Позиции фурнитуры")  # Имя окна
        self.resize(440, 450)
        self.toolBar.setStyleSheet("background-color: rgb(251, 110, 255);")  # Цвет бара

        self.pb_copy.deleteLater()
        self.pb_other.setText("Подробнее")
        self.pb_add.deleteLater()
        self.pb_change.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_filter.deleteLater()

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("№ Прихода", 70), ("Дата", 65), ("Цена", 70), ("В приходе", 100), ("Осталось", 100))

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT accessories_balance.Id, accessories_supply.Id, accessories_supply.Data, accessories_supplyposition.Price, accessories_supplyposition.Value,
                                        accessories_balance.BalanceValue
                                      FROM accessories_supplyposition LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.accessories_SupplyPositionId
                                        LEFT JOIN accessories_supply ON accessories_supplyposition.accessories_SupplyId = accessories_supply.Id
                                      WHERE accessories_supplyposition.accessories_NameId = %s AND BalanceValue > 0
                                      ORDER BY accessories_supply.Data DESC"""
        self.query_table_dell = ""

    def set_table_info(self):
        self.table_items = my_sql.sql_select(self.query_table_select, (self.other_value, ))
        if "mysql.connector.errors" in str(type(self.table_items)):
                QMessageBox.critical(self, "Ошибка sql получение таблицы", self.table_items.msg, QMessageBox.Ok)
                return False

        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        if not self.table_items:
            return False

        for table_typle in self.table_items:
            self.table_widget.insertRow(self.table_widget.rowCount())
            for column in range(1, len(table_typle)):
                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(table_typle[column]))
                elif isinstance(table_typle[column], datetime.date):
                    text = table_typle[column].strftime("%d.%m.%Y")
                else:
                    text = str(table_typle[column])

                if table_typle[4] == table_typle[5]:
                    color = QBrush(QColor(150, 255, 161, 255))
                elif table_typle[5] == 0:
                    color = QBrush(QColor(252, 141, 141, 255))
                else:
                    color = QBrush(QColor(255, 255, 153, 255))

                item = QTableWidgetItem(text)
                item.setData(5, table_typle[0])
                item.setBackground(color)
                self.table_widget.setItem(self.table_widget.rowCount() - 1, column - 1, item)

    def ui_other(self):
        query = """SELECT accessories_balance.Id, accessories_supply.Id, accessories_supply.Data, accessories_supplyposition.Price, accessories_supplyposition.Value,
                      accessories_balance.BalanceValue
                    FROM accessories_supplyposition LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.accessories_SupplyPositionId
                      LEFT JOIN accessories_supply ON accessories_supplyposition.accessories_SupplyId = accessories_supply.Id
                    WHERE accessories_supplyposition.accessories_NameId = %s
                    ORDER BY accessories_supply.Data DESC"""
        self.table_items = my_sql.sql_select(query, (self.other_value, ))
        if "mysql.connector.errors" in str(type(self.table_items)):
                QMessageBox.critical(self, "Ошибка sql получение таблицы", self.table_items.msg, QMessageBox.Ok)
                return False

        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        if not self.table_items:
            return False

        for table_typle in self.table_items:
            self.table_widget.insertRow(self.table_widget.rowCount())
            for column in range(1, len(table_typle)):
                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(table_typle[column]))
                elif isinstance(table_typle[column], datetime.date):
                    text = table_typle[column].strftime("%d.%m.%Y")
                else:
                    text = str(table_typle[column])

                if table_typle[4] == table_typle[5]:
                    color = QBrush(QColor(150, 255, 161, 255))
                elif table_typle[5] == 0:
                    color = QBrush(QColor(252, 141, 141, 255))
                else:
                    color = QBrush(QColor(255, 255, 153, 255))

                item = QTableWidgetItem(text)
                item.setData(5, table_typle[0])
                item.setBackground(color)
                self.table_widget.setItem(self.table_widget.rowCount() - 1, column - 1, item)

    def ui_change_table_item(self, id=False):  # изменить элемент
        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
                return False

        self.supply_info = WarehouseTransaction(self, False, item_id)
        self.supply_info.setWindowModality(Qt.ApplicationModal)
        self.supply_info.show()


class WarehouseTransaction(table.TableList):

    def set_settings(self):
        self.setWindowTitle("Транзакции баланса")  # Имя окна
        self.resize(490, 600)
        self.toolBar.setStyleSheet("background-color: rgb(251, 110, 255);")  # Цвет бара

        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.pb_add.deleteLater()
        self.pb_change.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_filter.deleteLater()

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Кол-во", 70), ("Дата", 65), ("Заметка", 300), ("Пачка", 40))

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT transaction_records_accessories.Id, transaction_records_accessories.Balance, transaction_records_accessories.Date,
                                        transaction_records_accessories.Note, transaction_records_accessories.Pack_Accessories_Id
                                      FROM accessories_balance LEFT JOIN transaction_records_accessories ON accessories_balance.Id = transaction_records_accessories.Supply_Balance_Id
                                      WHERE transaction_records_accessories.Supply_Balance_Id = %s
                                      ORDER BY transaction_records_accessories.Date DESC """
        self.query_table_dell = ""

    def set_table_info(self):
        self.table_items = my_sql.sql_select(self.query_table_select, (self.other_value, ))
        if "mysql.connector.errors" in str(type(self.table_items)):
                QMessageBox.critical(self, "Ошибка sql получение таблицы", self.table_items.msg, QMessageBox.Ok)
                return False

        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        if not self.table_items:
            return False

        for table_typle in self.table_items:
            self.table_widget.insertRow(self.table_widget.rowCount())
            for column in range(1, len(table_typle)):
                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(table_typle[column]))
                elif isinstance(table_typle[column], datetime.date):
                    text = table_typle[column].strftime("%d.%m.%Y")
                else:
                    text = str(table_typle[column])

                if table_typle[1] >= 0:
                    color = QBrush(QColor(150, 255, 161, 255))
                else:
                    color = QBrush(QColor(255, 255, 153, 255))

                item = QTableWidgetItem(text)
                item.setData(5, table_typle[0])
                item.setBackground(color)
                self.table_widget.setItem(self.table_widget.rowCount() - 1, column - 1, item)

    def ui_change_table_item(self, id=False):  # изменить элемент
        pass
