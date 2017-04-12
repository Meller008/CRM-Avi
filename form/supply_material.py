from os import getcwd
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QTableWidgetItem, QLineEdit, QSizePolicy, QWidget
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5.QtCore import Qt, QDate
from function import my_sql
from form import provider, comparing
from form.templates import table, list
from decimal import Decimal
import re


supply_material = loadUiType(getcwd() + '/ui/supply_material.ui')[0]
supply_material_position = loadUiType(getcwd() + '/ui/supply_material_position.ui')[0]
supply_material_filter = loadUiType(getcwd() + '/ui/supply_filter.ui')[0]


class MaterialSupplyList(table.TableList):
    def set_settings(self):


        self.filter = None

        self.setWindowTitle("Приход материала")  # Имя окна
        self.resize(750, 270)
        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.toolBar.setStyleSheet("background-color: rgb(0, 170, 255);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("№", 30), ("Дата", 70), ("Поставщик", 170), ("Вес", 100), ("Сумма", 100), ("Примечание", 240))

        self.query_table_all = """SELECT material_supply.Id, material_supply.Id, material_supply.Data, material_provider.Name, SUM(material_supplyposition.Weight),
                                                ROUND(IFNULL(SUM(material_supplyposition.Weight * material_supplyposition.Price), 0) +
                                                  IFNULL((SELECT SUM(comparing_supplyposition.Value * comparing_supplyposition.Price)
                                                   FROM comparing_supplyposition WHERE comparing_supplyposition.Material_SupplyId = material_supply.Id), 0), 4), material_supply.Note
                                              FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                                                LEFT JOIN material_provider ON material_supply.Material_ProviderId = material_provider.Id
                                              GROUP BY material_supply.Id ORDER BY material_supply.Data DESC """

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT material_supply.Id, material_supply.Id, material_supply.Data, material_provider.Name, SUM(material_supplyposition.Weight),
                                        ROUND(IFNULL(SUM(material_supplyposition.Weight * material_supplyposition.Price), 0) +
                                          IFNULL((SELECT SUM(comparing_supplyposition.Value * comparing_supplyposition.Price)
                                           FROM comparing_supplyposition WHERE comparing_supplyposition.Material_SupplyId = material_supply.Id), 0), 4), material_supply.Note
                                      FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                                        LEFT JOIN material_provider ON material_supply.Material_ProviderId = material_provider.Id
                                      GROUP BY material_supply.Id ORDER BY material_supply.Data DESC """

        self.query_table_dell = ""

    def ui_add_table_item(self):  # Добавить предмет
        self.new_supply = MaterialSupply(self)
        self.new_supply.setWindowModality(Qt.ApplicationModal)
        self.new_supply.show()

    def ui_change_table_item(self, id=False):  # изменить элемент
        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
                return False

        self.change_supply = MaterialSupply(self, item_id)
        self.change_supply.setWindowModality(Qt.ApplicationModal)
        self.change_supply.show()

    def ui_dell_table_item(self):
        result = QMessageBox.question(self, "Удаление", "Точно удалить элемент?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            try:
                id_item = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка Удаления", "Выделите элемент который хотите удалить", QMessageBox.Ok)
                return False

            query = """SELECT COUNT(*)
                          FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                            LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                          WHERE material_supplyposition.Weight != material_balance.BalanceWeight AND material_supply.Id = %s"""
            sql_info = my_sql.sql_select(query, (id_item, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql при проверке удаляемых остатков", sql_info.msg, QMessageBox.Ok)
                return False

            if sql_info[0][0] != 0:
                QMessageBox.critical(self, "Ошибка удаления", "Нельзя удалить приход который пошел в работу!", QMessageBox.Ok)
                return False

            query = """SELECT material_balance.Id
                          FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                            LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                          WHERE material_supply.Id = %s"""
            sql_info = my_sql.sql_select(query, (id_item,))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql при получении ID балансов", sql_info.msg, QMessageBox.Ok)
                return False

            balance_id_list = sql_info

            sql_connect_transaction = my_sql.sql_start_transaction()

            for id in balance_id_list:
                query = """DELETE FROM transaction_records_material WHERE Supply_Balance_Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (id[0],))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при удалении записей баланса", sql_info.msg, QMessageBox.Ok)
                    return False

                query = """DELETE FROM material_balance WHERE Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (id[0],))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при удалении баланса", sql_info.msg, QMessageBox.Ok)
                    return False

            query = """DELETE FROM material_supplyposition WHERE Material_SupplyId = %s"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (id_item,))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql при удалении позиции", sql_info.msg, QMessageBox.Ok)
                return False

            query = """DELETE FROM material_supply WHERE Id = %s"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (id_item,))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql при удалении прихода", sql_info.msg, QMessageBox.Ok)
                return False

            my_sql.sql_commit_transaction(sql_connect_transaction)

            self.set_table_info()

    def ui_filter(self):
        if self.filter is None:
            self.filter = MaterialSupplyFilter(self)
        self.filter.of_set_sql_query(self.query_table_all)
        self.filter.setWindowModality(Qt.ApplicationModal)
        self.filter.show()

    def of_set_filter(self, sql):
        self.query_table_select = sql

        self.ui_update()


class MaterialSupply(QMainWindow, supply_material):
    def __init__(self, main, id=False):
        super(MaterialSupply, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        self.id = id
        self.change_info = False

        self.del_material = []
        self.del_comparing = []

        self.set_size_table()
        self.set_start_settings()

    def set_start_settings(self):
        if self.id:
            query = """SELECT material_provider.Id, material_provider.Name, material_supply.Data, material_supply.Note
                          FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                            LEFT JOIN material_provider ON material_supply.Material_ProviderId = material_provider.Id
                          WHERE material_supply.Id = %s"""
            sql_info = my_sql.sql_select(query, (self.id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql при получении информации", sql_info.msg, QMessageBox.Ok)
                self.ui_can()

            self.le_provider.setWhatsThis(str(sql_info[0][0]))
            self.le_provider.setText(sql_info[0][1])
            self.de_date.setDate(sql_info[0][2])
            self.le_note.setText(sql_info[0][3])

            query = """SELECT material_supplyposition.Id, material_name.Id, material_name.Name, material_supplyposition.Weight, material_supplyposition.Price,
                            ROUND(material_supplyposition.Price * material_supplyposition.Weight, 4), material_balance.BalanceWeight
                          FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                            LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                            LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                          WHERE material_supply.Id = %s"""
            sql_info = my_sql.sql_select(query, (self.id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql при получении основных позиций", sql_info.msg, QMessageBox.Ok)
                self.ui_can()

            self.tw_position.clearContents()
            self.tw_position.setRowCount(0)

            row_material = len(sql_info)

            for row, info in enumerate(sql_info):
                self.tw_position.insertRow(row)
                if info[3] == info[6]:
                    color = QBrush(QColor(0, 170, 255, 50))
                elif info[6] == 0:
                    color = QBrush(QColor(252, 141, 141, 255))
                else:
                    color = QBrush(QColor(255, 255, 127, 255))

                new_table_item = QTableWidgetItem(str(info[2]))
                new_table_item.setData(-1, info[0])
                new_table_item.setData(-2, "set")
                new_table_item.setData(-3, "material")
                new_table_item.setData(5, info[1])
                new_table_item.setBackground(color)
                self.tw_position.setItem(row, 0, new_table_item)

                new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(info[3], 4))))
                new_table_item.setData(-1, info[0])
                new_table_item.setData(-2, "set")
                new_table_item.setData(-3, "material")
                new_table_item.setData(5, info[3])
                new_table_item.setBackground(color)
                self.tw_position.setItem(row, 1, new_table_item)

                new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(info[4], 4))))
                new_table_item.setData(-1, info[0])
                new_table_item.setData(-2, "set")
                new_table_item.setData(-3, "material")
                new_table_item.setBackground(color)
                self.tw_position.setItem(row, 2, new_table_item)

                new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(info[5], 4))))
                new_table_item.setData(-1, info[0])
                new_table_item.setData(-2, "set")
                new_table_item.setData(-3, "material")
                new_table_item.setBackground(color)
                self.tw_position.setItem(row, 3, new_table_item)

                new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(info[6], 4))))
                new_table_item.setData(-1, info[0])
                new_table_item.setData(-2, "set")
                new_table_item.setData(-3, "material")
                new_table_item.setBackground(color)
                self.tw_position.setItem(row, 4, new_table_item)

                query = """SELECT comparing_supplyposition.Id, comparing_name.Id, comparing_name.Name, comparing_supplyposition.Value, comparing_supplyposition.Price,
                                ROUND(comparing_supplyposition.Price * comparing_supplyposition.Value, 4), ''
                              FROM material_supply LEFT JOIN comparing_supplyposition ON material_supply.Id = comparing_supplyposition.Material_SupplyId
                                LEFT JOIN comparing_name ON comparing_supplyposition.Comparing_NameId = comparing_name.Id
                              WHERE material_supply.Id = %s"""
                sql_info = my_sql.sql_select(query, (self.id,))
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql при получении основных позиций", sql_info.msg, QMessageBox.Ok)
                    self.ui_can()

                if sql_info[0][0] is not None:

                    for row, info in enumerate(sql_info):
                        self.tw_position.insertRow(row_material + row)
                        color = QBrush(QColor(221, 255, 204, 255))

                        new_table_item = QTableWidgetItem(str(info[2]))
                        new_table_item.setData(-1, info[0])
                        new_table_item.setData(-2, "set")
                        new_table_item.setData(-3, "comparing")
                        new_table_item.setData(5, info[1])
                        new_table_item.setBackground(color)
                        self.tw_position.setItem(row_material + row, 0, new_table_item)

                        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(info[3], 4))))
                        new_table_item.setData(-1, info[0])
                        new_table_item.setData(-2, "set")
                        new_table_item.setData(-3, "comparing")
                        new_table_item.setData(5, info[3])
                        new_table_item.setBackground(color)
                        self.tw_position.setItem(row_material + row, 1, new_table_item)

                        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(info[4], 4))))
                        new_table_item.setData(-1, info[0])
                        new_table_item.setData(-2, "set")
                        new_table_item.setData(-3, "comparing")
                        new_table_item.setBackground(color)
                        self.tw_position.setItem(row_material + row, 2, new_table_item)

                        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(info[5], 4))))
                        new_table_item.setData(-1, info[0])
                        new_table_item.setData(-2, "set")
                        new_table_item.setData(-3, "comparing")
                        new_table_item.setBackground(color)
                        self.tw_position.setItem(row_material + row, 3, new_table_item)

                        new_table_item = QTableWidgetItem(str(info[6]))
                        new_table_item.setData(-1, info[0])
                        new_table_item.setData(-2, "set")
                        new_table_item.setData(-3, "comparing")
                        new_table_item.setBackground(color)
                        self.tw_position.setItem(row_material + row, 4, new_table_item)

        else:
            self.de_date.setDate(QDate.currentDate())

        self.calc()

    def set_size_table(self):
        self.tw_position.horizontalHeader().resizeSection(0, 210)
        self.tw_position.horizontalHeader().resizeSection(1, 90)
        self.tw_position.horizontalHeader().resizeSection(2, 70)
        self.tw_position.horizontalHeader().resizeSection(3, 110)
        self.tw_position.horizontalHeader().resizeSection(4, 80)

    def ui_change_info(self):
        self.change_info = True

    def ui_view_provider(self):
        self.provider = provider.ProviderMaterial(self, True)
        self.provider.setWindowModality(Qt.ApplicationModal)
        self.provider.show()

    def ui_add_position(self):
        self.add_position = MaterialSupplyPosition(False)
        self.add_position.setModal(True)
        self.add_position.show()

        if self.add_position.exec() <= 0:
            return False

        row = self.tw_position.rowCount()

        self.tw_position.insertRow(row)
        color = QBrush(QColor(0, 170, 255, 50))

        new_table_item = QTableWidgetItem(self.add_position.le_name_material.text())
        new_table_item.setData(-1, "None")
        new_table_item.setData(-2, "new")
        new_table_item.setData(-3, "material")
        new_table_item.setData(5, self.add_position.le_name_material.whatsThis())
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 0, new_table_item)

        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(Decimal(self.add_position.le_value.text()))))
        new_table_item.setData(-1, "None")
        new_table_item.setData(-2, "new")
        new_table_item.setData(-3, "material")
        new_table_item.setData(5, "None")
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 1, new_table_item)

        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(Decimal(self.add_position.le_price.text()))))
        new_table_item.setData(-1, "None")
        new_table_item.setData(-2, "new")
        new_table_item.setData(-3, "material")
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 2, new_table_item)

        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(Decimal(self.add_position.le_sum.text()))))
        new_table_item.setData(-1, "None")
        new_table_item.setData(-2, "new")
        new_table_item.setData(-3, "material")
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 3, new_table_item)

        new_table_item = QTableWidgetItem("None")
        new_table_item.setData(-1, "None")
        new_table_item.setData(-2, "new")
        new_table_item.setData(-3, "material")
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 4, new_table_item)

        self.calc()
        self.ui_change_info()

    def ui_add_comparing(self):
        self.add_position = ComparingPosition(False)
        self.add_position.setModal(True)
        self.add_position.show()

        if self.add_position.exec() <= 0:
            return False

        row = self.tw_position.rowCount()

        self.tw_position.insertRow(row)
        color = QBrush(QColor(221, 255, 204, 255))

        new_table_item = QTableWidgetItem(self.add_position.le_name_material.text())
        new_table_item.setData(-1, "None")
        new_table_item.setData(-2, "new")
        new_table_item.setData(-3, "comparing")
        new_table_item.setData(5, self.add_position.le_name_material.whatsThis())
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 0, new_table_item)

        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(Decimal(self.add_position.le_value.text()))))
        new_table_item.setData(-1, "None")
        new_table_item.setData(-2, "new")
        new_table_item.setData(-3, "comparing")
        new_table_item.setData(5, "None")
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 1, new_table_item)

        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(Decimal(self.add_position.le_price.text()))))
        new_table_item.setData(-1, "None")
        new_table_item.setData(-2, "new")
        new_table_item.setData(-3, "comparing")
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 2, new_table_item)

        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(Decimal(self.add_position.le_sum.text()))))
        new_table_item.setData(-1, "None")
        new_table_item.setData(-2, "new")
        new_table_item.setData(-3, "comparing")
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 3, new_table_item)

        new_table_item = QTableWidgetItem("None")
        new_table_item.setData(-1, "None")
        new_table_item.setData(-2, "new")
        new_table_item.setData(-3, "comparing")
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 4, new_table_item)

        self.calc()
        self.ui_change_info()

    def ui_double_click(self, row):
        self.ui_change_position(row)

    def ui_change_position(self, in_row=False):
        if in_row:
            row = in_row
        else:
            try:
                row = self.tw_position.currentRow()
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
                return False

        if row < 0:
            QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
            return False

        table_item = self.tw_position.item(row, 0)

        item = {"id": table_item.data(-1),
                "sql status": table_item.data(-2),
                "type": table_item.data(-3),
                "position name id": table_item.data(5),
                "position name": table_item.text().replace(" ", ""),
                "value": self.tw_position.item(row, 1).text().replace(" ", ""),
                "sql value": self.tw_position.item(row, 1).data(5),
                "price": self.tw_position.item(row, 2).text().replace(" ", ""),
                "sum": self.tw_position.item(row, 3).text().replace(" ", ""),
                "warehouse": self.tw_position.item(row, 4).text().replace(" ", "")}

        if item["type"] == "material":
            self.change_position = MaterialSupplyPosition(item)
            self.change_position.setModal(True)
            self.change_position.show()

        else:
            self.change_position = ComparingPosition(item)
            self.change_position.setModal(True)
            self.change_position.show()

        if self.change_position.exec() <= 0:
            return False

        if item["type"] == "material" and (item["sql status"] == "upd" or item["sql status"] == "set"):
            if Decimal(Decimal(item["warehouse"])) + (Decimal(self.change_position.le_value.text()) - item["sql value"]) < 0:
                QMessageBox.critical(self, "Ошибка изменения", "Нельзя изменить меньше чем на складе!", QMessageBox.Ok)
                return False

        if item["type"] == "material":
            color = QBrush(QColor(0, 170, 255, 50))
        else:
            color = QBrush(QColor(221, 255, 204, 255))

        if item["sql status"] == "new":
            new_status = "new"
        else:
            new_status = "upd"

        new_table_item = QTableWidgetItem(self.change_position.le_name_material.text())
        new_table_item.setData(-1, item["id"])
        new_table_item.setData(-2, new_status)
        new_table_item.setData(-3, item["type"])
        new_table_item.setData(5, self.change_position.le_name_material.whatsThis())
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 0, new_table_item)

        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(Decimal(self.change_position.le_value.text()))))
        new_table_item.setData(-1, item["id"])
        new_table_item.setData(-2, new_status)
        new_table_item.setData(-3, item["type"])
        new_table_item.setData(5, item["sql value"])
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 1, new_table_item)

        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(Decimal(self.change_position.le_price.text()))))
        new_table_item.setData(-1, item["id"])
        new_table_item.setData(-2, new_status)
        new_table_item.setData(-3, item["type"])
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 2, new_table_item)

        new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(Decimal(self.change_position.le_sum.text()))))
        new_table_item.setData(-1, item["id"])
        new_table_item.setData(-2, new_status)
        new_table_item.setData(-3, item["type"])
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 3, new_table_item)

        new_table_item = QTableWidgetItem(item["warehouse"])
        new_table_item.setData(-1, item["id"])
        new_table_item.setData(-2, new_status)
        new_table_item.setData(-3, item["type"])
        new_table_item.setBackground(color)
        self.tw_position.setItem(row, 4, new_table_item)

        self.calc()
        self.ui_change_info()

    def ui_del_position(self):
        try:
            row = self.tw_position.currentRow()
        except:
            QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
            return False

        if row < 0:
            QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удаление", "Точно удалить позицию?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            table_item = self.tw_position.item(row, 0)
            if table_item.data(-3) == "material":
                if table_item.data(-2) == "upd"or table_item.data(-2) == "set":
                    # Если это сохраненая позиция
                    if str(self.tw_position.item(row, 1).data(5)) != self.tw_position.item(row, 4).text():
                        # Если на складе и в приходе кол-во не равно то нельзя удалять!
                        QMessageBox.critical(self, "Ошибка удаления", "Нельзя удалить позицию которая пошла в работу!", QMessageBox.Ok)
                        return False
                    self.del_material.append(table_item.data(-1))

                self.tw_position.removeRow(row)
            else:
                if table_item.data(-2) == "upd"or table_item.data(-2) == "set":
                    self.del_comparing.append(table_item.data(-1))

                self.tw_position.removeRow(row)

            self.calc()
            self.ui_change_info()

    def ui_acc(self):
        if not self.id:

            if self.le_provider.whatsThis() == "":
                return False

            sql_connect_transaction = my_sql.sql_start_transaction()

            query = """INSERT INTO material_supply (Material_ProviderId, Data, Note) VALUES (%s, %s, %s)"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.le_provider.whatsThis(), self.de_date.date().toPyDate(), self.le_note.text()))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql при сохранении прихода", sql_info.msg, QMessageBox.Ok)
                return False

            supply_id = sql_info

            for row in range(self.tw_position.rowCount()):
                if self.tw_position.item(row, 0).data(-3) == "material":
                    # Если эта строка материала
                    query = """INSERT INTO material_supplyposition (Material_SupplyId, Material_NameId, Weight, Price) VALUES (%s, %s, %s, %s)"""
                    sql_value = (supply_id, self.tw_position.item(row, 0).data(5), Decimal(self.tw_position.item(row, 1).text().replace(" ", "")),
                                 Decimal(self.tw_position.item(row, 2).text().replace(" ", "")))
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        QMessageBox.critical(self, "Ошибка sql при сохранении позиции материала", sql_info.msg, QMessageBox.Ok)
                        return False

                    position_id = sql_info

                    query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note)
                                  VALUES ((SELECT material_balance.Id FROM material_balance WHERE material_balance.Material_SupplyPositionId = %s), %s, NOW(), %s)"""
                    txt_note = "Заказ %s - новый приход" % supply_id
                    sql_value = (position_id, Decimal(self.tw_position.item(row, 1).text().replace(" ", "")), txt_note)
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        QMessageBox.critical(self, "Ошибка sql при сохранении записи в журнал", sql_info.msg, QMessageBox.Ok)
                        return False

                else:
                    # Если эта строка прочих растрат
                    query = """INSERT INTO comparing_supplyposition (Material_SupplyId, Comparing_NameId, Value, Price) VALUES (%s, %s, %s, %s)"""
                    sql_value = (supply_id, self.tw_position.item(row, 0).data(5), Decimal(self.tw_position.item(row, 1).text().replace(" ", "")),
                                 Decimal(self.tw_position.item(row, 2).text().replace(" ", "")))
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        QMessageBox.critical(self, "Ошибка sql при сохранении позиции расходов", sql_info.msg, QMessageBox.Ok)
                        return False

            my_sql.sql_commit_transaction(sql_connect_transaction)

        else:
            if not self.change_info:
                self.close()
                self.destroy()
                return False
            sql_connect_transaction = my_sql.sql_start_transaction()

            query = """UPDATE material_supply SET Material_ProviderId = %s, Data = %s, Note = %s WHERE Id =  %s"""
            sql_value = (self.le_provider.whatsThis(), self.de_date.date().toPyDate(), self.le_note.text(), self.id)
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql при сохранении прихода", sql_info.msg, QMessageBox.Ok)
                return False

            for row in range(self.tw_position.rowCount()):
                if self.tw_position.item(row, 0).data(-3) == "material":
                    # Если эта строка материала
                    if self.tw_position.item(row, 0).data(-2) == "upd":
                        # Если это измененая строка
                        query = """UPDATE material_supplyposition SET Material_NameId = %s, Weight = %s, Price = %s WHERE Id = %s"""
                        sql_value = (self.tw_position.item(row, 0).data(5), Decimal(self.tw_position.item(row, 1).text().replace(" ", "")),
                                     Decimal(self.tw_position.item(row, 2).text().replace(" ", "")), self.tw_position.item(row, 0).data(-1))
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql при изменении позиции материала", sql_info.msg, QMessageBox.Ok)
                            return False

                        change_value = Decimal(self.tw_position.item(row, 1).text().replace(" ", "")) - Decimal(self.tw_position.item(row, 1).data(5))

                        query = """UPDATE material_balance SET  BalanceWeight = BalanceWeight + %s WHERE Material_SupplyPositionId = %s"""
                        sql_value = (change_value, self.tw_position.item(row, 0).data(-1))
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql при изменении баланса материала", sql_info.msg, QMessageBox.Ok)
                            return False

                        query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note)
                                    VALUES ((SELECT material_balance.Id FROM material_balance WHERE material_balance.Material_SupplyPositionId = %s), %s, NOW(), %s)"""
                        txt_note = "Заказ %s - изменение прихода" % self.id
                        sql_value = (self.tw_position.item(row, 0).data(-1), change_value, txt_note)
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql при сохранении записи в журнал об изменении", sql_info.msg, QMessageBox.Ok)
                            return False

                    elif self.tw_position.item(row, 0).data(-2) == "new":
                        # Если это новая строка
                        query = """INSERT INTO material_supplyposition (Material_SupplyId, Material_NameId, Weight, Price) VALUES (%s, %s, %s, %s)"""
                        sql_value = (self.id,  self.tw_position.item(row, 0).data(5), Decimal(self.tw_position.item(row, 1).text().replace(" ", "")),
                                     Decimal(self.tw_position.item(row, 2).text().replace(" ", "")))
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql при сохранении позиции материала", sql_info.msg, QMessageBox.Ok)
                            return False

                        position_id = sql_info

                        query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note)
                                    VALUES ((SELECT material_balance.Id FROM material_balance WHERE material_balance.Material_SupplyPositionId = %s), %s, NOW(), %s)"""
                        txt_note = "Заказ %s - новый приход" % self.id
                        sql_value = (position_id, Decimal(self.tw_position.item(row, 1).text().replace(" ", "")), txt_note)
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql при сохранении записи в журнал", sql_info.msg, QMessageBox.Ok)
                            return False

                else:
                    # Если эта строка прочих растрат
                    if self.tw_position.item(row, 0).data(-2) == "upd":
                        # Если это измененая строка
                        query = """UPDATE comparing_supplyposition SET Comparing_NameId = %s, Value = %s, Price = %s WHERE Id = %s"""
                        sql_value = (self.tw_position.item(row, 0).data(5), Decimal(self.tw_position.item(row, 1).text().replace(" ", "")),
                                     Decimal(self.tw_position.item(row, 2).text().replace(" ", "")), self.tw_position.item(row, 0).data(-1))
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql при изменении позиции расходов", sql_info.msg, QMessageBox.Ok)
                            return False

                    elif self.tw_position.item(row, 0).data(-2) == "new":
                        # Если это новая строка
                        query = """INSERT INTO comparing_supplyposition (Material_SupplyId, Comparing_NameId, Value, Price) VALUES (%s, %s, %s, %s)"""
                        sql_value = (self.id, self.tw_position.item(row, 0).data(5), Decimal(self.tw_position.item(row, 1).text().replace(" ", "")),
                                     Decimal(self.tw_position.item(row, 2).text().replace(" ", "")))
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql при сохранении новой позиции расходов", sql_info.msg, QMessageBox.Ok)
                            return False

                # Удаление материала
            for id in self.del_material:

                query = """SELECT Id FROM material_balance WHERE Material_SupplyPositionId = %s"""
                sql_info = my_sql.sql_select_transaction(sql_connect_transaction, query, (id, ))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при получении id для удаления баланса", sql_info.msg, QMessageBox.Ok)
                    return False

                balance_sql = sql_info[0][0]

                query = """DELETE FROM transaction_records_material WHERE Supply_Balance_Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (balance_sql,))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при удалении записей баланса", sql_info.msg, QMessageBox.Ok)
                    return False

                query = """DELETE FROM material_balance WHERE Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (balance_sql,))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при удалении баланса", sql_info.msg, QMessageBox.Ok)
                    return False

                query = """DELETE FROM material_supplyposition WHERE Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (id,))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при удалении позиции", sql_info.msg, QMessageBox.Ok)
                    return False

            # Удаление прочих растрат
            for id in self.del_comparing:
                query = """DELETE FROM comparing_supplyposition WHERE Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (id,))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при удалении расходов", sql_info.msg, QMessageBox.Ok)
                    return False

            my_sql.sql_commit_transaction(sql_connect_transaction)

        self.main.ui_update()
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()

    def calc(self):
        value = 0
        sum_material = 0
        sum_all = 0

        for row in range(self.tw_position.rowCount()):
            if self.tw_position.item(row, 1).data(-3) == "material":
                value += Decimal(self.tw_position.item(row, 1).text().replace(" ", ""))
                sum_material += Decimal(self.tw_position.item(row, 3).text().replace(" ", ""))

            sum_all += Decimal(self.tw_position.item(row, 3).text().replace(" ", ""))

        self.le_value.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(value)))
        self.le_sum_material.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sum_material)))
        self.le_sum_all.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sum_all)))

    def of_list_reason_provider_material(self, item):
        self.le_provider.setWhatsThis(str(item[0]))
        self.le_provider.setText(item[1])


class MaterialSupplyPosition(QDialog, supply_material_position):
    def __init__(self, item=None):
        super(MaterialSupplyPosition, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.item = item

        self.set_start_settings()

    def set_start_settings(self):
        if self.item:
            self.le_name_material.setWhatsThis(str(self.item["position name id"]))
            self.le_name_material.setText(self.item["position name"])
            self.le_value.setText(self.item["value"])
            self.le_price.setText(self.item["price"])
            self.le_sum.setText(self.item["sum"])

    def ui_view_material(self):
        self.material_name = MaterialNameAndWarehouse(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_change_value(self, text):
        if text:
            if text[-1].isdigit():
                pass
            elif text[-1] == ".":
                pass
            elif text[-1] == ",":
                self.le_value.setText(text.replace(",", "."))
            else:
                self.le_value.setText(text[:-1])

        self.calc()

    def ui_change_price(self, text):
        if text:
            if text[-1].isdigit():
                pass
            elif text[-1] == ".":
                pass
            elif text[-1] == ",":
                self.le_price.setText(text.replace(",", "."))
            else:
                self.le_price.setText(text[:-1])

        self.calc()

    def ui_change_sum(self, text):
        if text:
            if text[-1].isdigit():
                pass
            elif text[-1] == ".":
                pass
            elif text[-1] == ",":
                self.le_sum.setText(text.replace(",", "."))
            else:
                self.le_sum.setText(text[:-1])

        self.calc(True)

    def ui_acc(self):
        if self.le_name_material.text() == "" or self.le_value.text() == "" or self.le_price.text() == "":
            return False

        self.done(1)
        self.close()
        self.destroy()

    def ui_can(self):
        self.done(-1)
        self.close()
        self.destroy()

    def calc(self, main_sum=False):
        try:
            value = Decimal(self.le_value.text())
        except:
            return False

        if not main_sum:
            try:
                price = Decimal(self.le_price.text())
            except:
                return False
        else:
            try:
                all = Decimal(self.le_sum.text())
            except:
                return False

        if main_sum:
            self.le_price.setText(str(round(all / value, 4)))
        else:
            self.le_sum.setText(str(round(price * value, 4)))

    def of_tree_select_material_name(self, item):
        self.le_name_material.setWhatsThis(str(item[1]))
        self.le_name_material.setText(item[0])


class MaterialSupplyFilter(QDialog, supply_material_filter):
    def __init__(self, main):
        super(MaterialSupplyFilter, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main

    def ui_view_provider(self):
        self.provider = provider.ProviderMaterial(self, True)
        self.provider.setWindowModality(Qt.ApplicationModal)
        self.provider.show()

    def ui_del_provider(self):
        self.le_provider.setWhatsThis("")
        self.le_provider.setText("")

    def ui_acc(self):
        where = ""

        # Блок  условий выбора поставщика
        if self.le_provider.whatsThis() != '':
            where = self.add_filter(where, "(material_supply.Material_ProviderId = %s)" % self.le_provider.whatsThis())

        # Блок  условий даты прихода
        if self.gb_date_supply.isChecked():
            sql_date = "(material_supply.Data >= '%s' AND material_supply.Data <= '%s')" % \
                       (self.de_date_supply_from.date().toString(Qt.ISODate), self.de_date_supply_to.date().toString(Qt.ISODate))
            where = self.add_filter(where, sql_date)

        # Делаем замену так как Were должно быть перед Group by
        if where:
            self.sql_query_all = self.sql_query_all.replace("GROUP BY", " WHERE " + where + "GROUP BY")

        self.main.of_set_filter(self.sql_query_all)

        self.close()

    def ui_can(self):
        self.close()
        self.destroy()

    def add_filter(self, where, add, and_add=True):
        if where:
            if and_add:
                where += " AND " + add
            else:
                where += " OR " + add
        else:
            where = add

        return where

    def of_set_sql_query(self, sql):
        self.sql_query_all = sql

    def of_list_reason_provider_material(self, item):
        self.le_provider.setWhatsThis(str(item[0]))
        self.le_provider.setText(item[1])


class MaterialNameAndWarehouse(table.TableList):
    def set_settings(self):

        self.setWindowTitle("Ткани")  # Имя окна
        self.resize(500, 270)
        self.pb_copy.deleteLater()
        self.pb_add.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_filter.deleteLater()
        self.pb_other.setText("Изменить")
        self.toolBar.setStyleSheet("background-color: rgb(0, 170, 255);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Название", 235), ("На складе", 80), ("Посл. цена", 80), ("Дата цены", 80))

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT material_name.Id, material_name.Name, SUM(material_balance.BalanceWeight), material_supplyposition.Price, MAX(material_supply.Data)
                                      FROM material_name LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                                        LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                                        LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                      GROUP BY material_name.Id ORDER BY material_name.Name"""

        self.query_table_dell = ""

    def ui_double_click_table_item(self, item):  # Двойной клик по элементу
        if not self.dc_select:
            pass
        else:
            # что хотим получить ставим всместо 0
            item = (self.table_widget.item(item.row(), 0).text(), item.data(5))
            self.main.of_tree_select_material_name(item)
            self.close()
            self.destroy()

    def ui_change_table_item(self, id=False):  # изменить элемент
        self.change_material = MaterialName()
        self.change_material.setWindowModality(Qt.ApplicationModal)
        self.change_material.show()

    def ui_other(self):
        self.material_name_settings = MaterialName(self, False)
        self.material_name_settings.setWindowModality(Qt.ApplicationModal)
        self.material_name_settings.show()


class MaterialName(list.ListItems):
    def set_settings(self):
        self.setWindowTitle("Ткань")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(0, 170, 255);")  # Цвет бара
        self.title_new_window = "Ткань"  # Имя вызываемых окон

        self.sql_list = "SELECT Id, Name FROM material_name ORDER BY Name"
        self.sql_add = "INSERT INTO material_name (Name, Information) VALUES (%s, %s)"
        self.sql_change_select = "SELECT Name, Information FROM material_name WHERE Id = %s"
        self.sql_update_select = 'UPDATE material_name SET Name = %s, Information = %s WHERE Id = %s'
        self.sql_dell = "DELETE FROM material_name WHERE Id = %s"

        self.set_new_win = {"WinTitle": "Материал",
                            "WinColor": "(0, 170, 255)",
                            "lb_name": "Название",
                            "lb_note": "Заметка"}

    def ui_double_click_item(self, select_prov):
        if not self.dc_select:
            self.ui_change_item(select_prov.data(3))
        else:
            item = (select_prov.data(3), select_prov.text())
            self.m_class.of_list_material_name(item)
            self.close()
            self.destroy()


class ComparingPosition(QDialog, supply_material_position):
    def __init__(self, item=None):
        super(ComparingPosition, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.item = item

        self.set_start_settings()

    def set_start_settings(self):
        self.widget.setStyleSheet("background-color: rgb(170, 255, 127);")

        if self.item:
            self.le_name_material.setWhatsThis(str(self.item["position name id"]))
            self.le_name_material.setText(self.item["position name"])
            self.le_value.setText(self.item["value"])
            self.le_price.setText(self.item["price"])
            self.le_sum.setText(self.item["sum"])

    def ui_view_material(self):
        self.material_name = comparing.ComparingName(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_change_value(self, text):
        if text:
            if text[-1].isdigit():
                pass
            elif text[-1] == ".":
                pass
            elif text[-1] == ",":
                self.le_value.setText(text.replace(",", "."))
            else:
                self.le_value.setText(text[:-1])

        self.calc()

    def ui_change_price(self, text):
        if text:
            if text[-1].isdigit():
                pass
            elif text[-1] == ".":
                pass
            elif text[-1] == ",":
                self.le_price.setText(text.replace(",", "."))
            else:
                self.le_price.setText(text[:-1])

        self.calc()

    def ui_change_sum(self, text):
        if text:
            if text[-1].isdigit():
                pass
            elif text[-1] == ".":
                pass
            elif text[-1] == ",":
                self.le_sum.setText(text.replace(",", "."))
            else:
                self.le_sum.setText(text[:-1])

        self.calc(True)

    def ui_acc(self):
        if self.le_name_material.text() == "" or self.le_value.text() == "" or self.le_price.text() == "":
            return False

        self.done(1)
        self.close()
        self.destroy()

    def ui_can(self):
        self.done(-1)
        self.close()
        self.destroy()

    def calc(self, main_sum=False):
        try:
            value = Decimal(self.le_value.text())
        except:
            return False

        if not main_sum:
            try:
                price = Decimal(self.le_price.text())
            except:
                return False
        else:
            try:
                all = Decimal(self.le_sum.text())
            except:
                return False

        if main_sum:
            self.le_price.setText(str(round(all / value, 4)))
        else:
            self.le_sum.setText(str(round(price * value, 4)))

    def of_list_reason_comparing_material(self, item):
        self.le_name_material.setWhatsThis(str(item[0]))
        self.le_name_material.setText(item[1])
