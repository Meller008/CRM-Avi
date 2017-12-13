import datetime
from form.templates import table
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt
import re
from function import my_sql
from decimal import *
from math import fabs


class Warehouse(table.TableList):
    def set_settings(self):
        self.setWindowTitle("Склад ткани")  # Имя окна
        self.resize(470, 550)
        self.toolBar.setStyleSheet("background-color: rgb(0, 170, 255);")  # Цвет бара

        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.pb_add.deleteLater()
        self.pb_change.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_filter.deleteLater()

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Ткань", 270), ("На складе", 90), ("Приходов", 70))

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT material_name.Id, material_name.Name, SUM(material_balance.BalanceWeight), SUM(material_balance.BalanceWeight > 0)
                                      FROM material_name LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                                        LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                                      GROUP BY material_name.Id
                                      ORDER BY material_name.Name"""
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
        self.setWindowTitle("Позиции ткани")  # Имя окна
        self.resize(440, 450)
        self.toolBar.setStyleSheet("background-color: rgb(0, 170, 255);")  # Цвет бара

        self.pb_copy.deleteLater()
        self.pb_other.setText("Подробнее")
        self.pb_add.deleteLater()
        self.pb_change.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_filter.deleteLater()

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("№ Прихода", 70), ("Дата", 65), ("Цена", 70), ("В приходе", 100), ("Осталось", 100))

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT material_balance.Id, material_supply.Id, material_supply.Data, material_supplyposition.Price, material_supplyposition.Weight,
                                        material_balance.BalanceWeight
                                      FROM material_supplyposition LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                                        LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                      WHERE material_supplyposition.Material_NameId = %s AND BalanceWeight > 0
                                      ORDER BY material_supply.Data DESC, material_supply.Id DESC """
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
        query = """SELECT material_balance.Id, material_supply.Id, material_supply.Data, material_supplyposition.Price, material_supplyposition.Weight,
                      material_balance.BalanceWeight
                    FROM material_supplyposition LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                      LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                    WHERE material_supplyposition.Material_NameId = %s
                    ORDER BY material_supply.Data DESC"""
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
        self.resize(530, 600)
        self.toolBar.setStyleSheet("background-color: rgb(0, 170, 255);")  # Цвет бара

        self.pb_copy.deleteLater()
        self.pb_add.deleteLater()
        self.pb_change.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_filter.deleteLater()

        self.pb_other.setText("Отменить транзакцию")

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("№", 50), ("Кол-во", 70), ("Дата", 65), ("Заметка", 250), ("Крой", 35), ("Бейка", 40))

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT transaction_records_material.Id, transaction_records_material.Id, transaction_records_material.Balance,
                                        transaction_records_material.Date, transaction_records_material.Note, transaction_records_material.Cut_Material_Id,
                                        transaction_records_material.Beika_Id
                                      FROM material_balance LEFT JOIN transaction_records_material ON material_balance.Id = transaction_records_material.Supply_Balance_Id
                                      WHERE transaction_records_material.Supply_Balance_Id = %s
                                      ORDER BY transaction_records_material.Date DESC, transaction_records_material.Id DESC """
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

                if table_typle[2] >= 0:
                    color = QBrush(QColor(150, 255, 161, 255))
                else:
                    color = QBrush(QColor(255, 255, 153, 255))

                item = QTableWidgetItem(text)
                item.setData(5, table_typle[0])
                item.setBackground(color)
                self.table_widget.setItem(self.table_widget.rowCount() - 1, column - 1, item)

    def ui_change_table_item(self, id=False):  # изменить элемент
        pass

    def ui_other(self):
        try:
            row = self.table_widget.selectedItems()[0].row()
            if self.table_widget.item(row, 4).text() != "None" and self.table_widget.item(row, 5).text() != "None":
                QMessageBox.critical(self, "Ошибка ", "Нельзя откатить транзакцию, которая принадлежит крою или бейке", QMessageBox.Ok)
                return False

            if float(self.table_widget.item(row, 1).text()) > 0:
                QMessageBox.critical(self, "Ошибка ", "Нельзя откатить положительную транзакцию", QMessageBox.Ok)
                return False
            item_id = self.table_widget.selectedItems()[0].data(5)

        except:
            QMessageBox.critical(self, "Ошибка ", "Выделите транзакцию которую хотите откатить", QMessageBox.Ok)
            return False

        sql_connect_transaction = my_sql.sql_start_transaction()

        # Получаем транзакцию
        query = """SELECT Id, Supply_Balance_Id, Balance FROM transaction_records_material WHERE Id = %s"""
        sql_value = (item_id, )
        sql_info_transaction = my_sql.sql_select_transaction(sql_connect_transaction, query, sql_value)
        if "mysql.connector.errors" in str(type(sql_info_transaction)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql получения транзакции", sql_info_transaction.msg, QMessageBox.Ok)
                return False

        if not sql_info_transaction:
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Ошибка", "Транзакция не найдена", QMessageBox.Ok)
            return False

        # Проверяем хватает ли места в данном приоходе
        sql_connect_transaction = my_sql.sql_start_transaction()
        query = """SELECT material_balance.BalanceWeight, material_supplyposition.Weight
                    FROM material_balance LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                    WHERE material_balance.Id = %s"""
        sql_value = (sql_info_transaction[0][1], )
        sql_info_balance = my_sql.sql_select_transaction(sql_connect_transaction, query, sql_value)
        if "mysql.connector.errors" in str(type(sql_info_balance)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Ошибка sql получения баланса", sql_info_balance.msg, QMessageBox.Ok)
            return False

        if not sql_info_balance:
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Ошибка", "Баланс не найден", QMessageBox.Ok)
            return False

        if sql_info_balance[0][0] - sql_info_transaction[0][2] > sql_info_balance[0][1]:
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Ошибка", "Возвращаемое кол-во превышает приход", QMessageBox.Ok)
            return False

        # Возвращаем материал на склад
        query = "UPDATE material_balance SET BalanceWeight = BalanceWeight + %s WHERE Id = %s"
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (fabs(sql_info_transaction[0][2]), sql_info_transaction[0][1]))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Не смог вернуть ткань на баланс склада", sql_info_balance.msg, QMessageBox.Ok)
            return False

        # Делаем запись о возврате
        query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code) 
                      VALUES (%s, %s, SYSDATE(), %s, NULL, 151)"""
        txt_note = "Отмена транзакции № %s" % sql_info_transaction[0][0]
        sql_values = (sql_info_transaction[0][1], fabs(sql_info_transaction[0][2]), txt_note)
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Не смог добавить запись при уменьшении ткани", sql_info_balance.msg, QMessageBox.Ok)
            return False

        my_sql.sql_commit_transaction(sql_connect_transaction)
        self.update()

