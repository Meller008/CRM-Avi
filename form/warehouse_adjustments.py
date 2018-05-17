from os import getcwd
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog, QPushButton
from PyQt5.QtCore import Qt, QDate, QDateTime, QObject
from PyQt5.QtGui import QIcon, QBrush, QColor
from decimal import Decimal
from function import my_sql, to_excel, table_to_html, moneyfmt, calc_price, str_to
from classes import print_qt
from form.templates import table, list
from form import warehouse_material, supply_material


class MaterialAdjustmentsList(table.TableList):
    def set_settings(self):

        self.setWindowTitle("Корректировки ткани")  # Имя окна
        self.resize(400, 270)
        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.pb_filter.deleteLater()
        self.toolBar.setStyleSheet("background-color: rgb(80, 80, 80);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("ID", 40), ("Ткань", 150), ("Кол-во", 80), ("Дата", 70))

        self.filter = None
        self.query_table_all = """SELECT material_adjustments.Id, material_adjustments.Id, material_name.Name, material_adjustments.Balance, material_adjustments.Date
                                      FROM material_adjustments
                                        LEFT JOIN material_balance ON material_adjustments.Balance_Id = material_balance.Id
                                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                        LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id """

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT material_adjustments.Id, material_adjustments.Id, material_name.Name, material_adjustments.Balance, material_adjustments.Date
                                      FROM material_adjustments
                                        LEFT JOIN material_balance ON material_adjustments.Balance_Id = material_balance.Id
                                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                        LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id"""

        self.query_table_dell = ""

    def ui_add_table_item(self):  # Добавить предмет
        self.new_order = MaterialAdjustments(self)
        self.new_order.setWindowModality(Qt.ApplicationModal)
        self.new_order.show()


class MaterialAdjustments(QDialog):
    def __init__(self, main, _id=None):
        super(MaterialAdjustments, self).__init__()
        loadUi(getcwd() + '/ui/adjustments_warehouse.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        self.id = _id

        self.start_settings()

    def start_settings(self):
        if not self.id:
            self.de_date.setDate(QDate.currentDate())

    def ui_view_material(self):
        self.material_name = supply_material.MaterialName(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_view_balance(self):
        material_id = self.le_material.whatsThis()

        if not material_id:
            QMessageBox.information(self, "Ошибка", "Выберите ткань", QMessageBox.Ok)
            return False

        self.supply_info = warehouse_material.WarehouseSupplyPosition(self, True, int(material_id))
        self.supply_info.setWindowModality(Qt.ApplicationModal)
        self.supply_info.show()

    def ui_acc(self):
        value_change = str_to.str_to_decimal(self.le_value.text())
        balance_id = self.le_balance_id.whatsThis()

        if not value_change or value_change > 0:
            QMessageBox.information(self, "Ошибка", "Что то не так с балансом, или он больше 0", QMessageBox.Ok)
            return False

        if not balance_id:
            QMessageBox.information(self, "Ошибка", "Выберите изменяемый баланс", QMessageBox.Ok)
            return False

        sql_connect_transaction = my_sql.sql_start_transaction()

        query = "UPDATE material_balance SET BalanceWeight = BalanceWeight + %s WHERE Id = %s"
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (value_change, balance_id))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Ошибка sql изменение баланса", sql_info.msg, QMessageBox.Ok)
            return False

        txt_note = "Корректировка № 000 уменьшение ткани"
        query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                                      VALUES (%s, %s, SYSDATE(), %s, NULL, 160)"""
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (balance_id, value_change, txt_note))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Ошибка sql добавления записи об изменении баланса", sql_info.msg, QMessageBox.Ok)
            return False

        transaction_id = sql_info

        query = """INSERT INTO material_adjustments (Balance_Id, Transaction_Id, Balance, Date, Note)
                                                      VALUES (%s, %s, %s, %s, %s)"""
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (balance_id, transaction_id, value_change,
                                                                                  self.de_date.date().toPyDate(), self.le_note.text()))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Ошибка sql записи коректировки", sql_info.msg, QMessageBox.Ok)
            return False

        adjustment_id = sql_info
        txt_note = "Корректировка №%s уменьшение ткани" % adjustment_id
        query = """UPDATE transaction_records_material SET Note = %s WHERE Id = %s"""
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (txt_note, transaction_id))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Ошибка sql добавления заметки к транзакции", sql_info.msg, QMessageBox.Ok)
            return False

        my_sql.sql_commit_transaction(sql_connect_transaction)

        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()

    def of_list_material_name(self, item):
        self.le_material.setWhatsThis(str(item[0]))
        self.le_material.setText(item[1])

    def of_table_select_warehouse_supply_position(self, item):
        self.le_balance_id.setWhatsThis(str(item[1]))
        self.le_balance_id.setText(item[0])
