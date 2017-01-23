from os import getcwd
from form import order, staff, operation, order, accesspries
from datetime import datetime
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QTreeWidgetItem, QPushButton
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt, QDate, QObject
from form.material import MaterialName
import re
from decimal import *

from function import my_sql, classes_function
from classes import cut
from form.templates import table, list
from form import clients, article

pack_class = loadUiType(getcwd() + '/ui/pack.ui')[0]
pack_operation_class = loadUiType(getcwd() + '/ui/pack_operation.ui')[0]
pack_accessories_class = loadUiType(getcwd() + '/ui/pack_accsessories.ui')[0]


class PackBrows(QDialog, pack_class):
    def __init__(self, main=None, pack=None, pack_id=None):
        super(PackBrows, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        if pack_id is not None:
            self.pack = cut.Pack(pack_id)
        else:
            self.pack = pack

        self.insert_values_sql = False

        self.set_start_info()
        self.set_size_table()

    def set_start_info(self):

        self.le_number_pack.setText(str(self.pack.number_pack()))
        self.le_number_cut.setText(str(self.pack.number_cut()))

        if self.pack.id() is not None:
            # Пачка не новая
            self.insert_values_sql = True

            self.pack.take_accessories_pack()
            self.pack.take_operation_pack()

            if self.pack.date_complete() is not None:
                self.cb_date_complete.setChecked(True)
                self.de_date_complete.setDate(self.pack.date_complete())
            else:
                self.de_date_complete.setDate(QDate.currentDate())

            if self.pack.date_make() is not None:
                self.cb_date_make.setChecked(True)
                self.de_date_make.setDate(self.pack.date_make())
            else:
                self.de_date_make.setDate(QDate.currentDate())

            self.le_article.setWhatsThis(str(self.pack.article()))
            self.le_article.setText(str(self.pack.article_name()))

            self.le_size.setText(str(self.pack.size()))

            self.le_client.setWhatsThis(str(self.pack.client()))
            self.le_client.setText(str(self.pack.client_name()))

            self.le_order.setWhatsThis(str(self.pack.order()))
            self.le_order.setText(str(self.pack.order()))

            self.le_note.setText(str(self.pack.note()))

            self.le_value_product.setText(str(self.pack.value()))
            self.le_value_damage.setText(str(self.pack.value_damage()))
            self.le_value_all.setText(str(self.pack.value_all()))
            self.le_weight.setText(str(self.pack.weight()))

            self.set_operation_name()
            self.set_accessories_name()

            self.insert_values_sql = False

        else:
            # Пачка новая
            self.de_date_complete.setDate(QDate.currentDate())
            self.de_date_make.setDate(QDate.currentDate())

    def set_size_table(self):
        self.tw_operation.horizontalHeader().resizeSection(0, 175)
        self.tw_operation.horizontalHeader().resizeSection(1, 130)
        self.tw_operation.horizontalHeader().resizeSection(2, 83)
        self.tw_operation.horizontalHeader().resizeSection(3, 50)
        self.tw_operation.horizontalHeader().resizeSection(4, 50)
        self.tw_operation.horizontalHeader().resizeSection(5, 105)
        self.tw_operation.horizontalHeader().resizeSection(6, 60)

        self.tw_accessories.horizontalHeader().resizeSection(0, 230)
        self.tw_accessories.horizontalHeader().resizeSection(1, 75)
        self.tw_accessories.horizontalHeader().resizeSection(2, 75)
        self.tw_accessories.horizontalHeader().resizeSection(3, 75)
        self.tw_accessories.horizontalHeader().resizeSection(4, 75)
        self.tw_accessories.horizontalHeader().resizeSection(5, 75)
        self.tw_accessories.horizontalHeader().resizeSection(6, 75)

    def ui_edit_date_complete(self):
        if not self.insert_values_sql:
            if self.cb_date_complete.isChecked():
                self.pack.set_date_complete(self.de_date_complete.date())
            else:
                self.pack.set_date_complete(None)

    def ui_edit_date_make(self):
        if not self.insert_values_sql:
            if self.cb_date_make.isChecked():
                self.pack.set_date_make(self.de_date_make.date())
            else:
                self.pack.set_date_make(None)

    def ui_edit_size(self, size):
        if not self.insert_values_sql:
            self.pack.set_size(size)

    def ui_edit_value_product(self):
        if not self.insert_values_sql:
            self.pack.set_value_pieces(self.le_value_product.text())
            self.set_value_pack()
            self.set_accessories_name()
            self.set_operation_name()

    def ui_edit_weight(self):
        if not self.insert_values_sql:
            self.pack.set_width(self.le_weight.text())
            material_check = self.pack.check_balance_material()
            if material_check[0]:
                self.le_weight.setStyleSheet("border: 4px solid;\nborder-color: rgb(122, 247, 84);")
                self.le_weight.setToolTip(material_check[1])
            else:
                self.le_weight.setStyleSheet("border: 4px solid;\nborder-color: rgb(247, 84, 84);")
                self.le_weight.setToolTip(material_check[1])

    def ui_edit_note(self):
        if not self.insert_values_sql:
            self.pack.set_note(self.le_note.text())

    def ui_edit_value_damage(self):
        if not self.insert_values_sql:
            self.pack.set_value_damage(self.le_value_damage.text())
            self.set_value_pack()
            self.set_accessories_name()
            self.set_operation_name()

    def ui_view_client(self):
        self.client_list = clients.ClientsList(self, True)
        self.client_list.setWindowModality(Qt.ApplicationModal)
        self.client_list.show()

    def ui_del_client(self):
        self.pack.del_client()
        self.le_client.clear()
        self.le_client.setWhatsThis("")

    def ui_view_list_article(self):
        self.article_list = article.ArticleList(self, True)
        self.article_list.setWindowModality(Qt.ApplicationModal)
        self.article_list.show()

    def ui_view_order(self):
        self.order_list = order.OrderList(self, True)
        self.order_list.setWindowModality(Qt.ApplicationModal)
        self.order_list.show()

    def ui_del_order(self):
        self.pack.del_order()
        self.le_order.clear()
        self.le_order.setWhatsThis("")

    def ui_add_operation(self):
        self.one_operation_window = PackOperation()
        self.one_operation_window.setModal(True)
        self.one_operation_window.show()
        if self.one_operation_window.exec() <= 0:
            return False
        operation = self.one_operation_window.operation
        self.pack.set_operation(operation)
        self.set_operation_name()

    def ui_change_operation(self):
        try:
            id = int(self.tw_operation.item(self.tw_operation.currentRow(), 0).data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите операцию.", QMessageBox.Ok)
            return False
        self.one_operation_window = PackOperation(self.pack.operation(id))
        self.one_operation_window.setModal(True)
        self.one_operation_window.show()
        if self.one_operation_window.exec() <= 0:
            return False
        operation = self.one_operation_window.operation
        self.pack.set_operation(operation, id)
        self.set_operation_name()

    def ui_del_operation(self):
        try:
            id = int(self.tw_operation.item(self.tw_operation.currentRow(), 0).data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите операцию.", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить операцию?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            if not self.pack.del_operation(id):
                QMessageBox.information(self, "Ошибка", "Операция не удалилась! Возможно она оплачена?", QMessageBox.Ok)
            else:
                self.set_operation_name()

    def ui_double_click_operation(self, table_item):
        try:
            id = int(table_item.data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите операцию.", QMessageBox.Ok)
            return False
        self.one_operation_window = PackOperation(self.pack.operation(id))
        self.one_operation_window.setModal(True)
        self.one_operation_window.show()
        if self.one_operation_window.exec() <= 0:
            return False
        operation = self.one_operation_window.operation
        self.pack.set_operation(operation, id)
        self.set_operation_name()

    def ui_clone_operation(self):
        try:
            id = int(self.tw_operation.item(self.tw_operation.currentRow(), 0).data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите операцию.", QMessageBox.Ok)
            return False

        error = self.pack.clone_operation(id)
        if not error[0]:
            QMessageBox.information(self, "Ошибка", error[1], QMessageBox.Ok)
            return False

        self.set_operation_name()

    def ui_double_click_accessories(self, table_item):
        try:
            id = int(table_item.data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите фурнитуру", QMessageBox.Ok)
            return False
        self.one_accessories_window = PackAccessories(self.pack.accessory(id))
        if id > 0:
            self.one_accessories_window.toolButton.setEnabled(False)
        self.one_accessories_window.setModal(True)
        self.one_accessories_window.show()
        if self.one_accessories_window.exec() <= 0:
            return False
        accessories = self.one_accessories_window.accessories
        self.pack.set_accessories(accessories, id)
        self.set_accessories_name()

    def ui_add_accessories(self):
        self.one_accessories_window = PackAccessories()
        self.one_accessories_window.setModal(True)
        self.one_accessories_window.show()
        if self.one_accessories_window.exec() <= 0:
            return False
        accessories = self.one_accessories_window.accessories
        self.pack.set_accessories(accessories)
        self.set_accessories_name()

    def ui_change_accessories(self):
        try:
            id = int(self.tw_accessories.item(self.tw_accessories.currentRow(), 0).data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите фурнитуру", QMessageBox.Ok)
            return False
        self.one_accessories_window = PackAccessories(self.pack.accessory(id))
        if id > 0:
            self.one_accessories_window.toolButton.setEnabled(False)
        self.one_accessories_window.setModal(True)
        self.one_accessories_window.show()
        if self.one_accessories_window.exec() <= 0:
            return False
        accessories = self.one_accessories_window.accessories
        self.pack.set_accessories(accessories, id)
        self.set_accessories_name()

    def ui_del_accessories(self):
        try:
            id = int(self.tw_accessories.item(self.tw_accessories.currentRow(), 0).data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите фурнитуру.", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить фурнитуру?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            if not self.pack.del_accessories(id):
                QMessageBox.information(self, "Ошибка", "Фурнитура не удалилась", QMessageBox.Ok)
            else:
                self.set_accessories_name()

    def ui_calc_pack(self):
        value = self.pack.value()
        value_damage = self.pack.value_damage()
        weight = self.pack.weight()
        material_price = self.pack.material_price()
        percent = int(self.le_calc_percent.text())

        operations_price = 0
        operations = self.pack.operations()
        for operation in operations:
            operations_price += operation["value"] * Decimal(str(operation["price"]))

        accessories_price = 0
        accessories = self.pack.accessories()
        for accessory in accessories:
            accessories_price += accessory["value"] * Decimal(str(accessory["value_thing"])) * Decimal(str(accessory["price"]))

        price_one_weight = round((weight / value) * material_price, 4)

        price_all_one = round((operations_price / value) + (accessories_price / value) + price_one_weight, 4)
        price_all_many = round(operations_price + accessories_price + (material_price * weight), 4)

        self.le_calc_one_operation.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(operations_price / value, 4))))
        self.le_calc_many_operation.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(operations_price, 4))))
        self.le_calc_one_accessory.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(accessories_price / value, 4))))
        self.le_calc_many_accessory.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(accessories_price, 4))))
        self.le_calc_one_material.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_one_weight, 4))))
        self.le_calc_many_material.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(material_price * weight, 4))))
        self.le_calc_one_all.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_all_one, 4))))
        self.le_calc_many_all.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_all_many, 4))))
        self.le_calc_one_percent.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_all_one + (price_all_one * percent / 100), 4))))
        self.le_calc_many_percent.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_all_many + (price_all_many * percent / 100), 4))))

        self.le_calc_damage.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(material_price * value_damage, 4))))

    def ui_acc(self):
        cut_id = None
        if self.pack.id() is None:
            cut_id = self.main.of_cut_id()

        save_note = self.pack.save_sql(cut_id)
        if not save_note[0]:
            QMessageBox.critical(self, "Ошибка сохранения пачки", save_note[1], QMessageBox.Ok)
            return False
        if self.main is not None:
            self.main.of_save_pack_complete()

        self.close()
        self.destroy()

    def ui_can(self):
        if self.pack.need_save_sql():
            result = QMessageBox.question(self, "Выйти?", "Есть несохраненая информация.\nТочно выйти без сохранения?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == 16384:
                self.close()
                self.destroy()
            else:
                return False
        else:
            self.close()
            self.destroy()

    def set_operation_name(self):
        operation_list = self.pack.operations()
        self.tw_operation.clearContents()
        self.tw_operation.setRowCount(0)
        row = 0
        for dict in operation_list:

            color = None
            note = ""
            if dict["pay"] == 1:
                color = QBrush(QColor(62, 181, 240, 255))
                note = "Зарплата выдана"
            elif dict["worker_id"] is not None:
                color = QBrush(QColor(62, 240, 130, 255))
                note = "Операция выполнена"
            else:
                color = QBrush(QColor(228, 242, 99, 255))
                note = ""

            self.tw_operation.insertRow(row)

            new_table_item = QTableWidgetItem(str(dict["name"]))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_operation.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["worker_name"]))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_operation.setItem(row, 1, new_table_item)

            date = dict["date_make"].strftime("%d.%m.%y") if dict["date_make"] is not None else None
            new_table_item = QTableWidgetItem(str(date))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_operation.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["value"]))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)

            self.tw_operation.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["price"]))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_operation.setItem(row, 4, new_table_item)

            date = dict["date_input"].strftime("%d.%m.%y %H:%M:%S") if dict["date_input"] is not None else None
            new_table_item = QTableWidgetItem(str(date))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_operation.setItem(row, 5, new_table_item)

            new_table_item = QTableWidgetItem(str(round(dict["price"] * dict["value"], 4)))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_operation.setItem(row, 6, new_table_item)

            row += 1

    def set_accessories_name(self):
        accessories_list = self.pack.accessories()
        self.tw_accessories.clearContents()
        self.tw_accessories.setRowCount(0)
        row = 0
        for dict in accessories_list:

            color = None
            note = ""
            if round(dict["value"] * dict["value_thing"], 4) != dict["sql_value_sum"]:
                balance = self.pack.check_balance_accessories(dict["id"])
                if balance[0]:
                    color = QBrush(QColor(122, 247, 84, 255))
                    note = balance[1]
                else:
                    color = QBrush(QColor(247, 84, 84, 255))
                    note = balance[1]

            self.tw_accessories.insertRow(row)

            new_table_item = QTableWidgetItem(str(dict["accessories_name"]))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_accessories.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["value"]))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_accessories.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["value_thing"]))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_accessories.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(round(dict["value_thing"] * dict["value"], 4)))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_accessories.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["price"]))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_accessories.setItem(row, 4, new_table_item)

            price = float(dict["price"]) if dict["price"] is not None else 0
            value = float(dict["value"]) if dict["value"] is not None else 0
            new_table_item = QTableWidgetItem(str(round(price * value, 4)))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_accessories.setItem(row, 5, new_table_item)

            row += 1

    def set_value_pack(self):
        self.le_value_all.setText(str(self.pack.value_all()))

    def of_tree_select_article(self, article):
        self.article_list.close()
        self.article_list.destroy()
        self.le_article.setWhatsThis(str(article["parametr_id"]))
        str_article = str(article["article"]) + " (" + str(article["size"]) + ") [" + str(article["parametr"]) + "]"
        self.le_article.setText(str_article)
        self.le_size.setText(article["size"])
        self.pack.set_article(article["parametr_id"])

        if self.pack.id() is None:
            self.pack.clear_save_operation()
            self.pack.take_article_operations()
            self.set_operation_name()

            self.pack.clear_save_accessories()
            self.pack.take_article_accessories()
            self.set_accessories_name()

    def of_set_client(self, id_client, name_client):
        self.le_client.setText(str(name_client))
        self.le_client.setWhatsThis(str(id_client))
        self.pack.set_client(id_client)

    def of_tree_select_order(self, order):
        self.le_order.setText(str(order[0]))
        self.le_order.setWhatsThis(str(order[1]))
        self.pack.set_order(order[1])


class PackOperation(QDialog, pack_operation_class):
    def __init__(self, operation=None):
        super(PackOperation, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.de_make.setDate(QDate.currentDate())
        self.de_input.setDate(QDate.currentDate())

        if operation is None:
            self.operation = {"id": None,
                              "position": None,
                              "operation_id": None,
                              "name": None,
                              "worker_id": None,
                              "worker_name": None,
                              "date_make": None,
                              "date_input": None,
                              "value": None,
                              "price": None,
                              "pay": 0}
        else:
            self.operation = operation
            self.set_info()

    def set_info(self):
        self.le_operation.setWhatsThis(str(self.operation["operation_id"]))
        self.le_operation.setText(str(self.operation["name"]))
        self.le_name.setText(str(self.operation["name"]))

        self.le_worker.setWhatsThis(str(self.operation["worker_id"]))
        self.le_worker.setText(str(self.operation["worker_name"]))

        self.le_price.setText(str(self.operation["price"]))
        self.le_value.setText(str(self.operation["value"]))

        if self.operation["date_make"] is not None:
            self.de_make.setDate(self.operation["date_make"])
        if self.operation["date_input"] is not None:
            self.de_input.setDate(self.operation["date_input"])

        if self.operation["pay"] == 1:
            self.cb_pay.setChecked(True)

            self.le_price.setReadOnly(True)
            self.le_value.setReadOnly(True)

    def ui_acc(self):
        if self.le_operation.text() != "" and self.le_operation.text() != "None":
            self.operation["operation_id"] = int(self.le_operation.whatsThis())
            self.operation["name"] = self.le_name.text()

        if self.le_worker.text() != "" and self.le_worker.text() != "None":
            self.operation["worker_id"] = int(self.le_worker.whatsThis())
            self.operation["worker_name"] = self.le_worker.text()
            self.operation["date_make"] = self.de_make.date()
            self.operation["date_input"] = self.de_input.date()

        if self.le_price.text() != "" and self.le_price.text() != "None":
            self.operation["price"] = float(self.le_price.text())

        if self.le_value.text() != "" and self.le_value.text() != "New" and self.le_value.text() != "None":
            self.operation["value"] = int(self.le_value.text())
        elif self.le_value.text() != "New":
            self.operation["value"] = 0

        if self.cb_pay.isChecked():
            self.operation["pay"] = 1
        else:
            self.operation["pay"] = 0

        self.done(1)

    def ui_del(self):
        self.done(-1)

    def ui_operation(self):
        self.operation_name = operation.OperationList(self, True)
        self.operation_name.setWindowModality(Qt.ApplicationModal)
        self.operation_name.show()

    def ui_staff(self):
        self.satff_name = staff.Staff(self, True)
        self.satff_name.setWindowModality(Qt.ApplicationModal)
        self.satff_name.show()

    def ui_dell_work(self):
        self.le_worker.setWhatsThis("")
        self.le_worker.setText("")

    def of_tree_select_operation(self, item):
        self.le_operation.setWhatsThis(str(item[0]))
        self.le_operation.setText(item[1])
        if self.le_price.text() == "":
            self.le_price.setText(str(item[2]))

        if self.le_value.text() == "":
            self.le_value.setText("New")

        if self.le_name.text() == "":
            self.le_name.setText(item[1])

    def of_list_worker(self, worker):
        self.le_worker.setWhatsThis(str(worker[0]))
        self.le_worker.setText(worker[1])


class PackAccessories(QDialog, pack_accessories_class):
    def __init__(self, accessories=None):
        super(PackAccessories, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        if accessories is None:
            self.accessories = {"id": None,
                                "accessories_id": None,
                                "accessories_name": None,
                                "price": None,
                                "value": None,
                                "sql_value": None}
        else:
            self.accessories = accessories
            self.set_info()

    def set_info(self):
        self.le_accessories.setWhatsThis(str(self.accessories["accessories_id"]))
        self.le_accessories.setText(str(self.accessories["accessories_name"]))
        self.le_value.setText(str(self.accessories["value"]))
        self.le_price.setText(str(self.accessories["price"]))
        self.le_value_thing.setText(str(self.accessories["value_thing"]))

        self.calc()

    def ui_accessories(self):
        self.accessories_name = accesspries.AccessoriesName(self, True)
        self.accessories_name.setWindowModality(Qt.ApplicationModal)
        self.accessories_name.show()

    def ui_acc(self):
        if self.le_accessories.text() != "" and self.le_accessories.text() != "None":
            self.accessories["accessories_id"] = int(self.le_accessories.whatsThis())
            self.accessories["accessories_name"] = self.le_accessories.text()

        if self.le_value.text() != "" and self.le_value.text() != "None":
            self.accessories["value"] = int(self.le_value.text())
        else:
            self.accessories["value"] = 0

        if self.le_value_thing.text() != "" and self.le_value_thing.text() != "None":
            self.accessories["value_thing"] = float(self.le_value_thing.text().replace(",", "."))
        else:
            self.accessories["value_thing"] = 0

        if self.le_price.text() != "" and self.le_value_thing.text() != "None":
            self.accessories["price"] = float(self.le_price.text())
        else:
            self.accessories["price"] = 0
        self.done(1)

    def ui_can(self):
        self.done(-1)

    def calc(self):
        if self.le_value.text() != "" and self.le_value_thing.text != "" and self.le_price.text() != "":
            if self.le_value.text() != "None" and self.le_value_thing.text != "None" and self.le_price.text() != "None":
                value = int(self.le_value.text())
                value_thing = float(self.le_value_thing.text())
                price = float(self.le_price.text())

                self.le_sum.setText(str(round((value_thing * price) * value, 4)))
                self.le_value_sum.setText(str(round(value_thing * value, 4)))

    def of_list_accessories_name(self, accessories):
        self.le_accessories.setText(str(accessories[1]))
        self.le_accessories.setWhatsThis(str(accessories[0]))