from os import getcwd
from form import order, staff, operation, order, accesspries
from datetime import datetime
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QTreeWidgetItem, QPushButton
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt, QDate, QObject
from form.material import MaterialName
import re

from function import my_sql, classes_function
from classes import cut
from form.templates import table, list
from form import clients, article

pack_class = loadUiType(getcwd() + '/ui/pack.ui')[0]
pack_operation_class = loadUiType(getcwd() + '/ui/pack_operation.ui')[0]
pack_accessories_class = loadUiType(getcwd() + '/ui/pack_accsessories.ui')[0]


class PackBrows(QDialog, pack_class):
    def __init__(self, main=None, pack=None):
        super(PackBrows, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        self.pack = pack

        self.set_start_info()

    def set_start_info(self):

        if self.pack.date_complete() is None:
            self.de_date_complete.setDate(QDate.currentDate())
        else:
            pass

        if self.pack.date_make() is None:
            self.de_date_make.setDate(QDate.currentDate())
        else:
            pass

        self.le_number_pack.setText(str(self.pack.number_pack()))
        self.le_number_cut.setText(str(self.pack.number_cut()))

    def ui_edit_date_complete(self):
        self.pack.set_date_complete(self.de_date_complete.date())

    def ui_edit_date_make(self):
        self.pack.set_date_make(self.de_date_make.date())

    def ui_edit_size(self, size):
        self.pack.set_size(size)

    def ui_edit_value_product(self):
        self.pack.set_value_pieces(self.le_value_product.text())
        self.set_value_pack()

    def ui_edit_weight(self):
        self.pack.set_width(self.le_weight.text())

    def ui_edit_value_damage(self):
        self.pack.set_value_damage(self.le_value_damage.text())
        self.set_value_pack()

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
                QMessageBox.information(self, "Ошибка", "Операция не удалилась", QMessageBox.Ok)
            else:
                self.set_operation_name()

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
        self.one_accessories_window.setModal(True)
        self.one_accessories_window.show()
        if self.one_accessories_window.exec() <= 0:
            return False
        accessories = self.one_accessories_window.accessories
        self.pack.set_accessories(operation, id)
        self.set_accessories_name()

    def ui_acc(self):
        pass

    def set_operation_name(self):
        operation_list = self.pack.operations()
        self.tw_operation.clearContents()
        self.tw_operation.setRowCount(0)
        row = 0
        for dict in operation_list:
            self.tw_operation.insertRow(row)

            new_table_item = QTableWidgetItem(str(dict["name"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_operation.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["worker_name"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_operation.setItem(row, 1, new_table_item)

            date = dict["date_make"].date() if dict["date_make"] is not None else None
            new_table_item = QTableWidgetItem(str(date))
            new_table_item.setData(-2, dict["id"])
            self.tw_operation.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["value"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_operation.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["price"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_operation.setItem(row, 4, new_table_item)

            date = dict["date_input"].date() if dict["date_input"] is not None else None
            new_table_item = QTableWidgetItem(str(date))
            new_table_item.setData(-2, dict["id"])
            self.tw_operation.setItem(row, 5, new_table_item)

            row += 1

    def set_accessories_name(self):
        accessories_list = self.pack.accessories()
        self.tw_accessories.clearContents()
        self.tw_accessories.setRowCount(0)
        row = 0
        for dict in accessories_list:
            self.tw_accessories.insertRow(row)

            new_table_item = QTableWidgetItem(str(dict["accessories_name"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_accessories.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["price"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_accessories.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["value"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_accessories.setItem(row, 2, new_table_item)

            price = float(dict["price"]) if dict["price"] is not None else 0
            value = float(dict["value"]) if dict["value"] is not None else 0
            new_table_item = QTableWidgetItem(str(round(price * value, 4)))
            new_table_item.setData(-2, dict["id"])
            self.tw_accessories.setItem(row, 3, new_table_item)

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
            self.pack.take_article_operations()
            self.set_operation_name()

            self.pack.take_article_accessories()
            self.set_accessories_name()

        pass

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
                              "price": None}
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
                                "value": None}
        else:
            self.accessories = accessories
            self.set_info()

    def set_info(self):
        self.le_accessories.setWhatsThis(str(self.accessories["accessories_id"]))
        self.le_accessories.setText(str(self.accessories["accessories_name"]))
        self.le_value.setText(str(self.accessories["value"]))
        self.le_price.setText(str(self.accessories["price"]))

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

        if self.le_price.text() != "" and self.le_price.text() != "None":
            self.accessories["price"] = int(self.le_price.text())
        else:
            self.accessories["price"] = 0
        self.done(1)

    def ui_can(self):
        self.done(-1)

    def of_list_accessories_name(self, accessories):
        self.le_accessories.setText(str(accessories[1]))
        self.le_accessories.setWhatsThis(str(accessories[0]))