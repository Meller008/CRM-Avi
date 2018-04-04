from os import getcwd
from re import findall, sub
from decimal import Decimal
import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QBrush, QColor
from function import my_sql, str_to
from form.templates import table
from form import cut


class TestWarehouseMaterial(QMainWindow):
    def __init__(self):
        super(TestWarehouseMaterial, self).__init__()
        loadUi(getcwd() + '/ui/test_material.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.toolBar.setStyleSheet("background-color: rgb(50, 50, 50);")  # Цвет бара

        self.de_date_from.setDate(QDate.currentDate().addMonths(-3))

        self.tableWidget.horizontalHeader().resizeSection(0, 40)
        self.tableWidget.horizontalHeader().resizeSection(1, 90)
        self.tableWidget.horizontalHeader().resizeSection(2, 90)
        self.tableWidget.horizontalHeader().resizeSection(3, 90)
        self.tableWidget.horizontalHeader().resizeSection(4, 120)
        self.tableWidget.horizontalHeader().resizeSection(5, 120)

    def ui_test(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        # Проверим нужно ли применять фильтр
        if self.rb_filter_no.isChecked():
            query = "SELECT cut.Id FROM cut ORDER BY cut.Id"
        elif self.rb_filter_date.isChecked():
            query = "SELECT cut.Id FROM cut WHERE cut.Date_Cut >= '%s' ORDER BY cut.Id" % self.de_date_from.date().toString(Qt.ISODate)
        elif self.rb_filter_num.isChecked():
            query = "SELECT cut.Id FROM cut WHERE cut.Id >= %s ORDER BY cut.Id" % self.le_cut_num.text()
        else:
            QMessageBox.critical(self, "Фильтр", "Что то не так с фильтром", QMessageBox.Ok)
            return False

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение приходов материала", sql_info.msg, QMessageBox.Ok)
                return False

        cut_id_list = [i[0] for i in sql_info]

        for cut_id in cut_id_list:
            self.statusBar.showMessage("Расчет кроя %s" % cut_id)

            # Проверим записаные суммы в крое
            query = """SELECT cut.Weight_Rest +cut.Weight_Pack_All, material_name.Name
                          FROM cut LEFT JOIN material_name ON cut.Material_Id = material_name.Id
                          WHERE cut.Id = %s"""
            sql_info = my_sql.sql_select(query, (cut_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql 1", sql_info.msg, QMessageBox.Ok)
                    return False

            res1 = sql_info[0][0]
            main_material = sql_info[0][1]

            # Проверим сумму взятую с пачек
            query = """SELECT c.Weight_Rest + (SELECT SUM(p.Weight) FROM pack as p WHERE p.Cut_Id = c.Id)
                          FROM cut as c WHERE c.Id = %s"""
            sql_info = my_sql.sql_select(query, (cut_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql 2/1", sql_info.msg, QMessageBox.Ok)
                    return False

            res2 = sql_info[0][0]

            # сумируем сумму пачек и доп ткани
            query = """SELECT SUM(pack_add_material.Weight_Rest + pack_add_material.Weight), material_name.Name
                          FROM pack_add_material LEFT JOIN pack ON pack_add_material.Pack_Id = pack.Id
                          LEFT JOIN material_name ON pack_add_material.Material_Name_Id = material_name.Id
                          WHERE pack.Cut_Id = %s"""
            sql_info = my_sql.sql_select(query, (cut_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql 2/2", sql_info.msg, QMessageBox.Ok)
                    return False

            if sql_info[0][0]:
                res2 += sql_info[0][0]

            add_material = sql_info[0][1]

            # Проверим сумму транзакций
            query = """SELECT SUM(Balance)
                        FROM transaction_records_material
                        WHERE transaction_records_material.Cut_Material_Id = %s"""
            sql_info = my_sql.sql_select(query, (cut_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql 3", sql_info.msg, QMessageBox.Ok)
                    return False

            if sql_info[0][0]:
                res3 = -sql_info[0][0]
            else:
                res3 = None

            if res1 == res2 == res3:
                color = QBrush(QColor(150, 255, 161, 255))
                status = 1
            elif res1 != res2 == res3:
                color = QBrush(QColor(255, 255, 153, 255))
                status = 2
            else:
                color = QBrush(QColor(252, 141, 141, 255))
                status = 3

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            item = QTableWidgetItem(str(cut_id))
            item.setData(5, cut_id)
            item.setData(-1, status)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            item = QTableWidgetItem(str(res1))
            item.setData(5, cut_id)
            item.setData(-1, status)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            item = QTableWidgetItem(str(res2))
            item.setData(5, cut_id)
            item.setData(-1, status)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            item = QTableWidgetItem(str(res3))
            item.setData(5, cut_id)
            item.setData(-1, status)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

            item = QTableWidgetItem(main_material)
            item.setData(5, cut_id)
            item.setData(-1, status)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

            item = QTableWidgetItem(add_material)
            item.setData(5, cut_id)
            item.setData(-1, status)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, item)

    def ui_view_transaction(self):
        try:
            id_item = self.tableWidget.selectedItems()[0].data(5)
        except:
            QMessageBox.information(self, "Ошибка", "Выделите элемент", QMessageBox.Ok)
            return False

        self.transaction = TransactionPack(id_item)
        self.transaction.setModal(True)
        self.transaction.show()

    def ui_select_cut(self):
        try:
            item_id = self.tableWidget.selectedItems()[0].data(5)
        except:
            QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
            return False

        self.cut_window = cut.CutBrows(self, item_id)
        self.cut_window.setModal(True)
        self.cut_window.show()

    def ui_filter_table(self):
        for row in range(self.tableWidget.rowCount()):
            status = self.tableWidget.item(row, 0).data(-1)
            if status == 1 and self.cb_good.isChecked():
                self.tableWidget.setRowHidden(row, False)
            elif status == 2 and self.cb_waring.isChecked():
                self.tableWidget.setRowHidden(row, False)
            elif status == 3 and self.cb_error.isChecked():
                self.tableWidget.setRowHidden(row, False)
            else:
                self.tableWidget.setRowHidden(row, True)

    def of_change_cut_complete(self):
        # Нужна для принятия кроя
        pass


class TransactionView(table.TableList):
    def set_settings(self):

        self.setWindowTitle("Транзакции")  # Имя окна
        self.resize(700, 500)
        self.pb_copy.deleteLater()
        self.pb_change.deleteLater()
        self.pb_other.deleteLater()
        self.pb_add.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_filter.deleteLater()
        self.toolBar.setStyleSheet("background-color: rgb(50, 50, 50);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("ID", 50), ("ID баланса", 40), ("Материал", 120), ("Кол-во", 70), ("Дата", 90), ("Заметка", 200), ("КОД", 40))

        self.filter = None
        self.query_table_all = """SELECT transaction_records_material.Id, transaction_records_material.Id, transaction_records_material.Supply_Balance_Id, material_name.Name,
                                        transaction_records_material.Balance, transaction_records_material.Date, transaction_records_material.Note, transaction_records_material.Code
                                    FROM transaction_records_material LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                                    LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                    LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                                    WHERE Cut_Material_Id = %s""" % self.other_value[0]

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT transaction_records_material.Id, transaction_records_material.Id, transaction_records_material.Supply_Balance_Id, material_name.Name,
                                        transaction_records_material.Balance, transaction_records_material.Date, transaction_records_material.Note, transaction_records_material.Code
                                    FROM transaction_records_material LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                                    LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                    LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                                    WHERE Cut_Material_Id = %s""" % self.other_value[0]

        self.query_table_dell = ""

    def set_table_info(self):
        tr_id = self.other_value[1]
        self.table_widget.setSortingEnabled(False)

        self.table_items = my_sql.sql_select(self.query_table_select)
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
                    text = sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(table_typle[column]))
                    item = table.QTableWidgetItemFloat(text)

                elif isinstance(table_typle[column], datetime.date):
                    date = QDate(table_typle[column].year, table_typle[column].month, table_typle[column].day)
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, date)

                else:
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, table_typle[column])

                if table_typle[0] in tr_id:
                    item.setBackground(QBrush(QColor(150, 255, 161, 255)))

                item.setData(5, table_typle[0])
                self.table_widget.setItem(self.table_widget.rowCount() - 1, column - 1, item)

        self.table_widget.setSortingEnabled(True)

    def ui_change_table_item(self, id=False):  # изменить элемент
        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
                return False

        self.transaction_change = ChangeTransaction(self, item_id)
        self.transaction_change.setModal(True)
        self.transaction_change.show()


class TransactionPack(QDialog):
    def __init__(self, _id):
        super(TransactionPack, self).__init__()
        loadUi(getcwd() + '/ui/test_material_pack.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.id = _id

        self.set_start_settings()
        self.calc()

    def set_start_settings(self):

        self.tableWidget.horizontalHeader().resizeSection(0, 30)
        self.tableWidget.horizontalHeader().resizeSection(1, 80)
        self.tableWidget.horizontalHeader().resizeSection(2, 80)
        self.tableWidget.horizontalHeader().resizeSection(3, 80)
        self.tableWidget.horizontalHeader().resizeSection(4, 80)

    def calc(self):
        # Проверим записаные суммы в крое
        query = """SELECT transaction_records_material.Note, transaction_records_material.Balance, transaction_records_material.Id
                        FROM transaction_records_material LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                        LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                        WHERE Cut_Material_Id = %s"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql 1", sql_info.msg, QMessageBox.Ok)
                return False

        pack = {}

        for transaction in sql_info:
            search_pack = findall(r"\d+/(\d+) - ", transaction[0])

            if search_pack:
                search_pack = int(search_pack[0])
            else:
                search_pack = 0

            i = pack.setdefault(search_pack, {"count": 0, "balance": 0, "t_id": []})
            i["count"] += 1
            i["t_id"].append(transaction[2])

            if transaction[1]:
                i["balance"] += transaction[1]

        sum_transaction, sum_info, sum_res = 0, 0, 0
        for key, item_key in pack.items():

            # Проверим записаные веса в пачке
            query = """SELECT pack.Weight + IFNULL(pack_add_material.Weight + pack_add_material.Weight_Rest, 0)
                            FROM pack LEFT JOIN pack_add_material ON pack.Id = pack_add_material.Pack_Id
                            WHERE pack.Cut_Id = %s AND pack.Number = %s"""
            sql_info = my_sql.sql_select(query, (self.id, key))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка поиска пачки", sql_info.msg, QMessageBox.Ok)
                    return False

            if sql_info and sql_info[0][0] and -sql_info[0][0] == item_key["balance"]:
                color = QBrush(QColor(150, 255, 161, 255))
            else:
                color = QBrush(QColor(252, 141, 141, 255))

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            item = QTableWidgetItem(str(key))
            item.setBackground(color)
            item.setData(5, item_key["t_id"])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            item = QTableWidgetItem(str(item_key["count"]))
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            item = QTableWidgetItem(str(item_key["balance"]))
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)
            sum_transaction += item_key["balance"]

            if sql_info:
                item = QTableWidgetItem(str(sql_info[0][0]))
                sum_info += sql_info[0][0]
            else:
                item = QTableWidgetItem("Нету")
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

            if sql_info:
                res = -item_key["balance"] - sql_info[0][0]
                sum_res += res
            else:
                res = None
            item = QTableWidgetItem(str(res))
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

        else:
            self.tableWidget.insertRow(self.tableWidget.rowCount())

            item = QTableWidgetItem(str(sum_transaction))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            item = QTableWidgetItem(str(sum_info))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

            item = QTableWidgetItem(str(sum_res))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

    def ui_view_transaction(self, row):
        list_id = [self.id, self.tableWidget.item(row, 0).data(5)]

        self.transaction = TransactionView(self, False, list_id)
        self.transaction.setWindowModality(Qt.ApplicationModal)
        self.transaction.show()


class ChangeTransaction(QDialog):
    def __init__(self, main, _id):
        super(ChangeTransaction, self).__init__()
        loadUi(getcwd() + '/ui/test_material_change.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        self.id = _id

        self.set_info()

    def set_info(self):
        # Получим транзакцию
        query = """SELECT transaction_records_material.Id, transaction_records_material.Balance, transaction_records_material.Note,
                      material_name.Name, transaction_records_material.Supply_Balance_Id, material_balance.BalanceWeight, material_supplyposition.Weight
                    FROM transaction_records_material LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                    LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                    LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                    WHERE transaction_records_material.Id = %s"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql не получил транзакцию", sql_info.msg, QMessageBox.Ok)
                return False

        self.balance_warehouse_now = sql_info[0][5]
        self.balance_warehouse_max = sql_info[0][6]

        self.le_id.setText(str(sql_info[0][0]))
        self.le_balance.setText(str(sql_info[0][1]))
        self.le_note.setText(str(sql_info[0][2]))
        self.le_material.setText(str(sql_info[0][3]))
        self.le_id_balance.setText(str(sql_info[0][4]))
        self.le_value_balance.setText(str(sql_info[0][5]) + "/" + str(sql_info[0][6]))

    def ui_calc(self):
        new = str_to.str_to_decimal(self.le_need_transaction.text())
        if new is None or new is False:
            self.pb_acc.setEnabled(False)
            return False

        old = str_to.str_to_decimal(self.le_balance.text())
        if old is None or old is False:
            self.pb_acc.setEnabled(False)
            return False

        change_value = new - old
        new_warehouse = self.balance_warehouse_now + change_value
        self.le_res.setText(str(change_value))
        self.le_new_balance_warehouse.setText(str(new_warehouse) + "/" + str(self.balance_warehouse_max))

        if 0 <= new_warehouse <= self.balance_warehouse_max:
            self.pb_acc.setEnabled(True)
        else:
            self.pb_acc.setEnabled(False)

    def ui_del(self):
        if self.le_need_transaction.isEnabled():
            self.le_need_transaction.setEnabled(False)
            self.le_need_transaction.setText("0")
            self.ui_calc()
        else:
            self.le_need_transaction.setEnabled(True)

    def ui_acc(self):
        change_balance = str_to.str_to_decimal(self.le_res.text())
        if change_balance is None or change_balance is False:
            QMessageBox.critical(self, "Проверка", "Что то не так с изменяемым кол-вом", QMessageBox.Ok)
            return False

        new_balance = str_to.str_to_decimal(self.le_need_transaction.text())
        if new_balance is None or new_balance is False:
            self.pb_acc.setEnabled(False)
            return False

        try:
            bal_id = int(self.le_id_balance.text())
            trans_id = int(self.le_id.text())
        except:
            QMessageBox.critical(self, "Проверка", "Что то не так с ID", QMessageBox.Ok)
            return False

        sql_connect_transaction = my_sql.sql_start_transaction()

        # Меняем баланс
        query = "UPDATE material_balance SET BalanceWeight = BalanceWeight + %s WHERE Id = %s"
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (change_balance, bal_id))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Ошибка SQL", "Не смог изменить баланс", QMessageBox.Ok)
            return False

        # Делаем запись о заборе ткани с баланса склада
        query = """UPDATE transaction_records_material SET Balance = %s, Note = %s WHERE Id = %s"""
        txt_note = self.le_note.text() + "*"
        sql_values = (new_balance, txt_note, trans_id)
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            QMessageBox.critical(self, "Ошибка SQL", "Не смог изменить запись", QMessageBox.Ok)
            return False

        my_sql.sql_commit_transaction(sql_connect_transaction)

        self.main.ui_update()
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()


# Тест фурнитуры
class TestWarehouseAccessories(QMainWindow):
    def __init__(self):
        super(TestWarehouseAccessories, self).__init__()
        loadUi(getcwd() + '/ui/test_accessories.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.toolBar.setStyleSheet("background-color: rgb(50, 50, 50);")  # Цвет бара

        self.de_date_from.setDate(QDate.currentDate().addMonths(-3))

        self.tableWidget.horizontalHeader().resizeSection(0, 40)
        self.tableWidget.horizontalHeader().resizeSection(1, 90)
        self.tableWidget.horizontalHeader().resizeSection(2, 90)

    def ui_test(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        # Проверим нужно ли применять фильтр
        if self.rb_filter_no.isChecked():
            query = "SELECT pack.Id FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id ORDER BY cut.Id"
        elif self.rb_filter_date.isChecked():
            query = "SELECT pack.Id FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id WHERE cut.Date_Cut >= '%s' ORDER BY cut.Id" % self.de_date_from.date().toString(Qt.ISODate)
        elif self.rb_filter_num.isChecked():
            query = "SELECT pack.Id FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id WHERE cut.Id >= %s ORDER BY cut.Id" % self.le_cut_num.text()
        else:
            QMessageBox.critical(self, "Фильтр", "Что то не так с фильтром", QMessageBox.Ok)
            return False

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение приходов материала", sql_info.msg, QMessageBox.Ok)
                return False

        pack_id_list = [i[0] for i in sql_info]
        pack_id_list_str = str(pack_id_list).replace("[", "").replace("]", "").replace("None,", "")

        # Проверим записаные суммы в крое
        query = """SELECT Pack_Id, SUM(Value * Value_Thing)
                    FROM pack_accessories
                    WHERE Pack_Id IN (%s)
                    GROUP BY pack_accessories.Pack_Id""" % pack_id_list_str
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql 1", sql_info.msg, QMessageBox.Ok)
                return False

        res1 = sql_info

        # Проверим сумму взятую с пачек
        query = """SELECT pack_accessories.Pack_Id, SUM(Balance)
                    FROM transaction_records_accessories
                      LEFT JOIN pack_accessories ON transaction_records_accessories.Pack_Accessories_Id = pack_accessories.Id
                    WHERE pack_accessories.Pack_Id IN (%s)
                    GROUP BY pack_accessories.Pack_Id""" % pack_id_list_str
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql 2", sql_info.msg, QMessageBox.Ok)
                return False

        res2 = sql_info
        res = {}
        for i in res1+res2:
            res.setdefault(i[0], []).append(i[1])

        for key, val in res.items():
            self.statusBar.showMessage("Расчет пачки %s" % key)

            if val[0] == -val[1]:
                color = QBrush(QColor(150, 255, 161, 255))
                status = 1

            else:
                color = QBrush(QColor(252, 141, 141, 255))
                status = 2

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            item = QTableWidgetItem(str(key))
            item.setData(5, key)
            item.setData(-1, status)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            item = QTableWidgetItem(str(val[0]))
            item.setData(-1, status)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            item = QTableWidgetItem(str(val[1]))
            item.setData(-1, status)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

    def ui_view_transaction(self):
        pass

    def ui_select_cut(self):
        pass

    def ui_filter_table(self):
        for row in range(self.tableWidget.rowCount()):
            status = self.tableWidget.item(row, 0).data(-1)
            if status == 1 and self.cb_good.isChecked():
                self.tableWidget.setRowHidden(row, False)
            elif status == 2 and self.cb_waring.isChecked():
                self.tableWidget.setRowHidden(row, False)
            elif status == 3 and self.cb_error.isChecked():
                self.tableWidget.setRowHidden(row, False)
            else:
                self.tableWidget.setRowHidden(row, True)

    def of_change_cut_complete(self):
        # Нужна для принятия кроя
        pass


# Быстрый тест складов
class TestFastWarehouse(QMainWindow):
    def __init__(self):
        super(TestFastWarehouse, self).__init__()
        loadUi(getcwd() + '/ui/fast_test_warehouse.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.test()

    def test(self):
        # Вес пачек
        query = "SELECT SUM(pack.Weight) FROM pack"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес пачек", sql_info.msg, QMessageBox.Ok)
            return False
        pack_w = sql_info[0][0]

        # Вес доп материала
        query = "SELECT SUM(Weight + Weight_Rest) FROM pack_add_material"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес доп материала", sql_info.msg, QMessageBox.Ok)
            return False
        pack_ad = sql_info[0][0]

        # Вес обрези
        query = "SELECT SUM(cut.Weight_Rest) FROM cut"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес обрези", sql_info.msg, QMessageBox.Ok)
            return False
        cut_w = sql_info[0][0]

        # Вес бейки
        query = "SELECT SUM(Value) FROM beika WHERE Finished = 1"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес бейки", sql_info.msg, QMessageBox.Ok)
            return False
        beika = sql_info[0][0]

        # Вес проданого
        query = "SELECT SUM(Balance) FROM transaction_records_material WHERE Code IN (150, 151)"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес проданого", sql_info.msg, QMessageBox.Ok)
            return False
        sel = -sql_info[0][0]

        all_w = pack_w + pack_ad + cut_w + beika + sel

        # Вес списано
        query = "SELECT SUM(Balance) FROM transaction_records_material WHERE Code NOT IN (110, 111)"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес списаного", sql_info.msg, QMessageBox.Ok)
            return False
        trans = -sql_info[0][0]

        # Всего пришло
        query = "SELECT SUM(Weight) FROM material_supplyposition"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес прихода", sql_info.msg, QMessageBox.Ok)
            return False
        supply = sql_info[0][0]

        # Вес склада
        query = "SELECT SUM(BalanceWeight) FROM material_balance"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес склада", sql_info.msg, QMessageBox.Ok)
            return False
        warehouse = sql_info[0][0]

        self.le_w_pack.setText(str(pack_w))
        self.le_w_add.setText(str(pack_ad))
        self.le_w_rest.setText(str(cut_w))
        self.le_w_beika.setText(str(beika))
        self.le_w_sell.setText(str(sel))
        self.le_w_sum.setText(str(all_w))
        self.le_w_trans.setText(str(trans))
        self.le_w_diff.setText(str(trans - all_w))
        self.le_w_supply.setText(str(supply))
        self.le_w_warehouse.setText(str(warehouse))
        self.le_w_diff_w.setText(str(warehouse - (supply - all_w)))

        # кол-ов в пачках
        query = "SELECT SUM(Value * Value_Thing) FROM pack_accessories"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql кол-во в пачках", sql_info.msg, QMessageBox.Ok)
            return False
        pack_v = sql_info[0][0]

        # кол-во списано
        query = "SELECT SUM(Balance) FROM transaction_records_accessories WHERE Code NOT IN (210, 211, 240)"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес доп материала", sql_info.msg, QMessageBox.Ok)
            return False
        trans = -sql_info[0][0]

        # кол-во пришло
        query = "SELECT SUM(Value) FROM accessories_supplyposition"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес обрези", sql_info.msg, QMessageBox.Ok)
            return False
        sup = sql_info[0][0]

        # Кол-во на складе
        query = "SELECT SUM(BalanceValue) FROM accessories_balance"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql вес бейки", sql_info.msg, QMessageBox.Ok)
            return False
        war = sql_info[0][0]

        self.le_f_pack.setText(str(pack_v))
        self.le_f_trans.setText(str(trans))
        self.le_f_diff.setText(str(trans - pack_v))
        self.le_f_supply.setText(str(sup))
        self.le_f_warehouse.setText(str(war))
        self.le_f_diff_w.setText(str(war - (sup - pack_v)))



