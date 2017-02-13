from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QBrush, QColor
import re
from decimal import Decimal
import datetime
import openpyxl
from openpyxl.styles import Border, Side, Font, Alignment, PatternFill
from openpyxl.worksheet.pagebreak import Break
from copy import copy
from function import my_sql, to_excel
from form.templates import table, list
from form import clients, article

position_class = loadUiType(getcwd() + '/ui/order_position.ui')[0]
order_class = loadUiType(getcwd() + '/ui/order.ui')[0]
order_doc = loadUiType(getcwd() + '/ui/order_doc_list.ui')[0]


class OrderList(table.TableList):
    def set_settings(self):

        self.setWindowTitle("Заказы")  # Имя окна
        self.resize(900, 270)
        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.toolBar.setStyleSheet("background-color: rgb(126, 176, 127);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Клиент", 120), ("Пункт разгрузки", 170), ("Дата заказ.", 75), ("Дата отгр.", 70), ("№ док.", 50), ("Стоймость", 105),
                                  ("Примечание", 230), ("Отгр.", 40))

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT `order`.Id, clients.Name, clients_actual_address.Name, `order`.Date_Order, `order`.Date_Shipment, `order`.Number_Doc,
                                    SUM(order_position.Value * order_position.Price), `order`.Note, IF(`order`.Shipped = 0, 'Нет', 'Да')
                                      FROM `order` LEFT JOIN clients ON `order`.Client_Id = clients.Id
                                        LEFT JOIN clients_actual_address ON `order`.Clients_Adress_Id = clients_actual_address.Id
                                        LEFT JOIN order_position ON `order`.Id = order_position.Order_Id GROUP BY `order`.Id ORDER BY `order`.Date_Order DESC"""

        self.query_table_dell = "DELETE FROM `order` WHERE Id = %s"

    def ui_add_table_item(self):  # Добавить предмет
        id = False
        self.new_order = Order(0, id)
        self.new_order.setWindowModality(Qt.ApplicationModal)
        self.new_order.show()

    def ui_change_table_item(self, id=False):  # изменить элемент
        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
                return False

        self.order = Order(0, item_id)
        self.order.setWindowModality(Qt.ApplicationModal)
        self.order.show()

    def ui_double_click_table_item(self, item):  # Двойной клик по элементу
        if not self.dc_select:
            self.ui_change_table_item(item.data(5))
        else:
            # что хотим получить ставим всместо 0
            item = (self.table_widget.item(item.row(), 4).text(), item.data(5))
            self.main.of_tree_select_order(item)
            self.close()
            self.destroy()

    def set_table_info(self):
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
            if table_typle[8] == "Да":
                color = QBrush(QColor(62, 240, 130, 255))
            else:
                color = QBrush(QColor(228, 242, 99, 255))

            for column in range(1, len(table_typle)):

                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(table_typle[column]))
                elif isinstance(table_typle[column], datetime.date):
                    text = table_typle[column].strftime("%d.%m.%Y")
                else:
                    text = str(table_typle[column])
                item = QTableWidgetItem(text)
                item.setData(5, table_typle[0])
                item.setBackground(color)
                self.table_widget.setItem(self.table_widget.rowCount() - 1, column - 1, item)


class Order(QMainWindow, order_class):
    def __init__(self, main_class=0, id=False):
        super(Order, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.id = id
        self.main = main_class

        self.save_change_order = False
        self.save_change_order_position = False

        self.start_settings()

        self.save_change_order = False
        self.save_change_order_position = False

    def start_settings(self):
        self.tw_position.horizontalHeader().resizeSection(0, 70)
        self.tw_position.horizontalHeader().resizeSection(1, 60)
        self.tw_position.horizontalHeader().resizeSection(2, 120)
        self.tw_position.horizontalHeader().resizeSection(3, 220)
        self.tw_position.horizontalHeader().resizeSection(4, 60)
        self.tw_position.horizontalHeader().resizeSection(5, 50)
        self.tw_position.horizontalHeader().resizeSection(6, 70)

        if self.id:
            self.start_set_sql_info()
        else:
            self.pb_add_position.setEnabled(False)
            self.pb_change_position.setEnabled(False)
            self.pb_dell_position.setEnabled(False)
            self.pb_check_warehouse.setEnabled(False)

            self.sql_shipped = False

            self.de_date_order.setDate(QDate.currentDate())
            self.de_date_shipment.setDate(QDate.currentDate())

            query = "SELECT IFNULL(MAX(Number_Doc + 1), 'No Number') FROM `order` WHERE YEAR(Date_Order) = %s"
            sql_info = my_sql.sql_select(query, (QDate.currentDate().year(),))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения нового номера документа", sql_info.msg, QMessageBox.Ok)
                return False
            if sql_info[0][0] == "No Number":
                self.le_number_doc.setText("1")
            else:
                self.le_number_doc.setText(str(sql_info[0][0]))

    def start_set_sql_info(self):
        query = """SELECT `order`.Client_Id, clients.Name, `order`.Clients_Vendor_Id, `order`.Clients_Adress_Id, order_transport_company.Id,
                    order_transport_company.Name, `order`.Date_Order, `order`.Date_Shipment, `order`.Number_Order, `order`.Number_Doc, `order`.Note, `order`.Shipped
                    FROM `order` LEFT JOIN order_transport_company ON `order`.Transport_Company_Id = order_transport_company.Id
                    LEFT JOIN clients ON `order`.Client_Id = clients.Id WHERE `order`.Id = %s"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения информации о заказе", sql_info.msg, QMessageBox.Ok)
            return False
        self.of_set_client(sql_info[0][0], sql_info[0][1])

        find_index = self.cb_clients_vendor.findData(sql_info[0][2])
        if find_index >= 0:
            self.cb_clients_vendor.setCurrentIndex(find_index)

        find_index = self.cb_clients_adress.findData(sql_info[0][3])
        if find_index >= 0:
            self.cb_clients_adress.setCurrentIndex(find_index)

        self.le_transport_company.setWhatsThis(str(sql_info[0][4]))
        self.le_transport_company.setText(sql_info[0][5])

        self.de_date_order.setDate(sql_info[0][6])
        self.de_date_shipment.setDate(sql_info[0][7])

        self.le_number_order.setText(sql_info[0][8])
        self.le_number_doc.setText(str(sql_info[0][9]))
        self.le_note.setText(sql_info[0][10])

        if sql_info[0][11] != 0:
            self.cb_shipping.setChecked(True)
            self.cb_shipping.setEnabled(True)
            self.pb_add_position.setEnabled(False)
            self.pb_change_position.setEnabled(False)
            self.pb_dell_position.setEnabled(False)
            self.sql_shipped = True
        else:
            self.cb_shipping.setChecked(False)
            self.sql_shipped = False

        query = """SELECT order_position.Id, product_article.Article, product_article_size.Size, product_article_parametrs.Id, product_article_parametrs.Name,
                    product_article_parametrs.Client_Name, order_position.Price, order_position.NDS, order_position.Value, order_position.In_On_Place,
                    order_position.Price * order_position.Value
                    FROM order_position LEFT JOIN product_article_parametrs ON order_position.Product_Article_Parametr_Id = product_article_parametrs.Id
                    LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                    LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id WHERE Order_Id = %s"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения позиций заказа", sql_info.msg, QMessageBox.Ok)
            return False

        for position in sql_info:
            row = self.tw_position.rowCount()
            self.tw_position.insertRow(row)
            table_item = QTableWidgetItem(position[1])
            table_item.setData(-1, "set")
            table_item.setData(-2, position[0])
            self.tw_position.setItem(row, 0, table_item)

            table_item = QTableWidgetItem(position[2])
            table_item.setData(-1, "set")
            table_item.setData(-2, position[0])
            self.tw_position.setItem(row, 1, table_item)

            table_item = QTableWidgetItem(position[4])
            table_item.setData(-1, "set")
            table_item.setData(-2, position[0])
            table_item.setData(5, position[3])
            self.tw_position.setItem(row, 2, table_item)

            table_item = QTableWidgetItem(str(position[5]))
            table_item.setData(-1, "set")
            table_item.setData(-2, position[0])
            self.tw_position.setItem(row, 3, table_item)

            table_item = QTableWidgetItem(str(position[6]))
            table_item.setData(-1, "set")
            table_item.setData(-2, position[0])
            table_item.setData(5, position[7])
            self.tw_position.setItem(row, 4, table_item)

            table_item = QTableWidgetItem(str(position[8]))
            table_item.setData(-1, "set")
            table_item.setData(-2, position[0])
            table_item.setData(5, position[9])
            self.tw_position.setItem(row, 5, table_item)

            table_item = QTableWidgetItem(str(position[10]))
            table_item.setData(-1, "set")
            table_item.setData(-2, position[0])
            self.tw_position.setItem(row, 6, table_item)

    def ui_view_client(self):
        self.client_list = clients.ClientsList(self, True)
        self.client_list.setWindowModality(Qt.ApplicationModal)
        self.client_list.show()

    def ui_view_transport_company(self):
        self.transport_company = TransportCompanyName(self, True)
        self.transport_company.setWindowModality(Qt.ApplicationModal)
        self.transport_company.show()

    def ui_add_position(self):
        self.position = Position()
        self.position.setModal(True)
        self.position.show()

        if not self.position.exec_():
            return False

        if self.position.le_parametr.whatsThis() == "":
            return False

        if not self.sql_shipped:
            self.cb_shipping.setChecked(self.sql_shipped)
            self.cb_shipping.setEnabled(self.sql_shipped)

        row = self.tw_position.rowCount()
        self.tw_position.insertRow(row)
        table_item = QTableWidgetItem(self.position.le_article.text())
        table_item.setData(-1, "new")
        self.tw_position.setItem(row, 0, table_item)

        table_item = QTableWidgetItem(self.position.le_size.text())
        table_item.setData(-1, "new")
        self.tw_position.setItem(row, 1, table_item)

        table_item = QTableWidgetItem(self.position.le_parametr.text())
        table_item.setData(-1, "new")
        table_item.setData(5, self.position.le_parametr.whatsThis())
        self.tw_position.setItem(row, 2, table_item)

        query = "SELECT Client_Name FROM product_article_parametrs WHERE Id = %s"
        sql_info = my_sql.sql_select(query, (self.position.le_parametr.whatsThis(),))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения имени артикула", sql_info.msg, QMessageBox.Ok)
            return False
        table_item = QTableWidgetItem(sql_info[0][0])
        table_item.setData(-1, "new")
        self.tw_position.setItem(row, 3, table_item)

        if self.position.nds_1.isChecked():
            nds = 18
        else:
            nds = 10
        if self.lb_client.whatsThis().find("no_nds") >= 0:
            table_item = QTableWidgetItem(self.position.le_price_no_nds.text())
            table_item.setData(-1, "new")
            table_item.setData(5, nds)
            self.tw_position.setItem(row, 4, table_item)

            table_item = QTableWidgetItem(self.position.le_sum_no_nds.text())
            table_item.setData(-1, "new")
            table_item.setData(5, nds)
            self.tw_position.setItem(row, 6, table_item)
        else:
            table_item = QTableWidgetItem(self.position.le_price.text())
            table_item.setData(-1, "new")
            table_item.setData(5, nds)
            self.tw_position.setItem(row, 4, table_item)

            table_item = QTableWidgetItem(self.position.le_sum_rub.text())
            table_item.setData(-1, "new")
            table_item.setData(5, nds)
            self.tw_position.setItem(row, 6, table_item)

        table_item = QTableWidgetItem(self.position.le_value.text())
        table_item.setData(-1, "new")
        table_item.setData(5, self.position.le_in_on_place.text())
        self.tw_position.setItem(row, 5, table_item)
        self.save_change_order_position = True
        return True

    def ui_change_position(self, row_in=False):
        if row_in:
            select_row = row_in
        else:
            try:
                select_row = self.tw_position.currentRow()
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
                return False

            if select_row == -1:
                return False

        self.position = Position()
        self.position.setModal(True)
        self.position.le_article.setText(self.tw_position.item(select_row, 0).text())
        self.position.le_size.setText(self.tw_position.item(select_row, 1).text())
        self.position.le_parametr.setText(self.tw_position.item(select_row, 2).text())
        self.position.le_parametr.setWhatsThis(str(self.tw_position.item(select_row, 2).data(5)))

        nds = self.tw_position.item(select_row, 4).data(5)
        if nds == 18:
            self.position.nds_1.setChecked(True)
        else:
            self.position.nds_2.setChecked(True)

        if self.lb_client.whatsThis().find("no_nds") >= 0:
            self.position.le_price_no_nds.setText(self.tw_position.item(select_row, 4).text())
            self.position.price_name_change = "no nds"
        else:
            self.position.le_price.setText(self.tw_position.item(select_row, 4).text())
            self.position.price_name_change = "nds"

        self.position.le_value.setText(self.tw_position.item(select_row, 5).text())
        self.position.le_in_on_place.setText(str(self.tw_position.item(select_row, 5).data(5)))
        self.position.ui_calculation()
        self.position.show()
        if not self.position.exec_():
            return False

        if not self.sql_shipped:
            self.cb_shipping.setChecked(self.sql_shipped)
            self.cb_shipping.setEnabled(self.sql_shipped)

        row = select_row
        if self.tw_position.item(row, 0).data(-1) == "new":
            status = "new"
            id = False
        else:
            status = "upd"
            id = self.tw_position.item(row, 0).data(-2)

        table_item = QTableWidgetItem(self.position.le_article.text())
        table_item.setData(-1, status)
        if id:
            table_item.setData(-2, id)
        self.tw_position.setItem(row, 0, table_item)

        table_item = QTableWidgetItem(self.position.le_size.text())
        table_item.setData(-1, status)
        if id:
            table_item.setData(-2, id)
        self.tw_position.setItem(row, 1, table_item)

        table_item = QTableWidgetItem(self.position.le_parametr.text())
        table_item.setData(-1, status)
        if id:
            table_item.setData(-2, id)
        table_item.setData(5, self.position.le_parametr.whatsThis())
        self.tw_position.setItem(row, 2, table_item)

        query = "SELECT Client_Name FROM product_article_parametrs WHERE Id = %s"
        sql_info = my_sql.sql_select(query, (self.position.le_parametr.whatsThis(),))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения имени артикула", sql_info.msg, QMessageBox.Ok)
            return False
        table_item = QTableWidgetItem(sql_info[0][0])
        table_item.setData(-1, status)
        if id:
            table_item.setData(-2, id)
        self.tw_position.setItem(row, 3, table_item)

        if self.position.nds_1.isChecked():
            nds = 18
        else:
            nds = 10
        if self.lb_client.whatsThis().find("no_nds") >= 0:
            table_item = QTableWidgetItem(self.position.le_price_no_nds.text())
            table_item.setData(-1, status)
            if id:
                table_item.setData(-2, id)
            table_item.setData(5, nds)
            self.tw_position.setItem(row, 4, table_item)

            table_item = QTableWidgetItem(self.position.le_sum_no_nds.text())
            table_item.setData(-1, status)
            if id:
                table_item.setData(-2, id)
            table_item.setData(5, nds)
            self.tw_position.setItem(row, 6, table_item)
        else:
            table_item = QTableWidgetItem(self.position.le_price.text())
            table_item.setData(-1, status)
            if id:
                table_item.setData(-2, id)
            table_item.setData(5, nds)
            self.tw_position.setItem(row, 4, table_item)

            table_item = QTableWidgetItem(self.position.le_sum_rub.text())
            table_item.setData(-1, status)
            if id:
                table_item.setData(-2, id)
            table_item.setData(5, nds)
            self.tw_position.setItem(row, 6, table_item)

        table_item = QTableWidgetItem(self.position.le_value.text())
        table_item.setData(-1, status)
        if id:
            table_item.setData(-2, id)
        table_item.setData(5, self.position.le_in_on_place.text())
        self.tw_position.setItem(row, 5, table_item)
        self.save_change_order_position = True
        return True

    def ui_double_click_position(self, row):
        if not self.sql_shipped:
            self.ui_change_position(row)

    def ui_del_position(self):
        try:
            row = self.tw_position.currentRow()
        except:
            QMessageBox.information(self, "Ошибка", "Выберете позицию для удаления", QMessageBox.Ok)
            return False

        if row == -1:
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить позицию?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            if not self.sql_shipped:
                self.cb_shipping.setChecked(self.sql_shipped)
                self.cb_shipping.setEnabled(self.sql_shipped)

            self.tw_position.setRowHidden(row, True)
            for col in range(4):
                self.tw_position.item(row, col).setData(-1, "del")
        self.save_change_order_position = True
        return True

    def ui_change_date_shipment(self):
        query = "SELECT IFNULL(MAX(Number_Doc + 1), 'No Number') FROM `order` WHERE YEAR(Date_Order) = %s"
        sql_info = my_sql.sql_select(query, (self.de_date_shipment.date().year(),))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения нового номера документа", sql_info.msg, QMessageBox.Ok)
            return False
        if sql_info[0][0] == "No Number":
            self.le_number_doc.setText("1")
        else:
            self.le_number_doc.setText(str(sql_info[0][0]))

    def ui_order_info_edit(self):
        if not self.save_change_order:
            self.save_change_order = True

    def ui_check_warehouse(self):
        position_article_id = []

        # Переберем таблицу и получим нужные ID для проверки слада
        for row in range(self.tw_position.rowCount()):
            table_item = self.tw_position.item(row, 2)

            self.tw_position.item(row, 1).setBackground(QBrush(QColor(252, 141, 141, 255)))

            if table_item.data(-1) == "new":
                if position_article_id.count(int(table_item.data(5))) == 0:
                    position_article_id.append(int(table_item.data(5)))
                else:
                    name = str(
                        self.tw_position.item(row, 0).text() + " (" + self.tw_position.item(row, 1).text() + ") [" + self.tw_position.item(row, 2).text() + "]")
                    QMessageBox.critical(self, "Ошибка проверки", "Эта позиция встречается 2 раза\n%s" % name, QMessageBox.Ok)
                    return False

            elif table_item.data(-1) == "upd":
                if position_article_id.count(int(table_item.data(5))) == 0:
                    position_article_id.append(int(table_item.data(5)))
                else:
                    name = str(
                        self.tw_position.item(row, 0).text() + " (" + self.tw_position.item(row, 1).text() + ") [" + self.tw_position.item(row, 2).text() + "]")
                    QMessageBox.critical(self, "Ошибка проверки", "Эта позиция встречается 2 раза\n%s" % name, QMessageBox.Ok)
                    return False

            elif table_item.data(-1) == "del":
                pass

            elif table_item.data(-1) == "set":
                if position_article_id.count(int(table_item.data(5))) == 0:
                    position_article_id.append(int(table_item.data(5)))
                else:
                    name = str(
                        self.tw_position.item(row, 0).text() + " (" + self.tw_position.item(row, 1).text() + ") [" + self.tw_position.item(row, 2).text() + "]")
                    QMessageBox.critical(self, "Ошибка проверки", "Эта позиция встречается 2 раза\n%s" % name, QMessageBox.Ok)
                    return False
            else:
                QMessageBox.critical(self, "Ошибка проверки", "Позиция без состояния", QMessageBox.Ok)
                return False

        # Получим остатки склада
        query = "SELECT Id_Article_Parametr, Value_In_Warehouse FROM product_article_warehouse WHERE Id_Article_Parametr IN %s" % str(
            tuple(position_article_id)).replace(",)", ")")
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение остатков склада", sql_info.msg, QMessageBox.Ok)
            return False

        if len(position_article_id) != len(sql_info):
            QMessageBox.critical(self, "Ошибка проверки", "Не равны списки заказа и баланса склада", QMessageBox.Ok)
            return False

        # переберем таблицу и сравним остатки
        color_yes = QBrush(QColor(150, 255, 161, 255))
        color_no = QBrush(QColor(252, 141, 141, 255))
        error = False

        for row in range(self.tw_position.rowCount()):
            table_item = self.tw_position.item(row, 2)
            if table_item.data(-1) != "del":
                warehouse_id = [warehouse for warehouse in sql_info if warehouse[0] == int(table_item.data(5))][0]

                value = warehouse_id[1] - int(self.tw_position.item(row, 5).text())
                if value >= 0:
                    color = color_yes
                    note = "На складе %s" % warehouse_id[1]
                else:
                    color = color_no
                    note = "Не хватает %s" % -value
                    error = True

                for col in range(7):
                    self.tw_position.item(row, col).setBackground(color)
                    self.tw_position.item(row, col).setToolTip(note)

        if not error:
            self.cb_shipping.setEnabled(True)

    def ui_export(self):
        path = QFileDialog.getSaveFileName(self, "Сохранение")
        if path[0]:
            to_excel.table_to_excel(self.table_widget, path[0])

    def ui_document_list(self):
        self.position = OrderDocList(self)
        self.position.setModal(True)
        self.position.show()

    def ui_acc(self):
        if self.save_sql():
            self.close()
            self.destroy()
            if self.main != 0:
                self.main.of_order_complete()

    def ui_can(self):
        if self.save_change_order or self.save_change_order_position:
            result = QMessageBox.question(self, "Сохранить?", "Сохранить изменение перед выходом?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == 16384:
                self.save_sql()
        self.close()
        self.destroy()

    def save_sql(self):
        if self.save_change_order:

            if self.cb_shipping.isChecked():
                shipped = 1
            else:
                shipped = 0

            if self.id:
                if self.le_transport_company.text() == "":
                    tc_id = None
                else:
                    tc_id = self.le_transport_company.whatsThis()

                query = """UPDATE `order` SET Client_Id = %s, Clients_Vendor_Id = %s, Clients_Adress_Id = %s, Transport_Company_Id = %s, Date_Order = %s,
                            Date_Shipment = %s, Number_Order = %s, Number_Doc = %s, Note = %s WHERE Id = %s"""
                parametrs = (self.le_client.whatsThis(), self.cb_clients_vendor.currentData(), self.cb_clients_adress.currentData(),
                             tc_id, self.de_date_order.date().toString(Qt.ISODate), self.de_date_shipment.date().toString(Qt.ISODate),
                             self.le_number_order.text(), self.le_number_doc.text(), self.le_note.text(), self.id)
                sql_info = my_sql.sql_change(query, parametrs)
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql изменения заказа", sql_info.msg, QMessageBox.Ok)
                    return False
                self.new_id = False
            else:
                query = """INSERT INTO `order` (Client_Id, Clients_Vendor_Id, Clients_Adress_Id, Transport_Company_Id, Date_Order, Date_Shipment,
                                                Number_Order, Number_Doc, Note, Shipped) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 0)"""
                parametrs = (self.le_client.whatsThis(), self.cb_clients_vendor.currentData(), self.cb_clients_adress.currentData(),
                             self.le_transport_company.whatsThis(), self.de_date_order.date().toString(Qt.ISODate),
                             self.de_date_shipment.date().toString(Qt.ISODate), self.le_number_order.text(), self.le_number_doc.text(), self.le_note.text())
                sql_info = my_sql.sql_change(query, parametrs)
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql добавления заказа", sql_info.msg, QMessageBox.Ok)
                    return False
                self.new_id = sql_info[0][0]
        if self.save_change_order_position or self.sql_shipped != self.cb_shipping.isChecked():

            if self.cb_shipping.isChecked():
                shipped = 1
            else:
                shipped = 0

            if self.id:
                sql_order_id = self.id
            elif self.new_id:
                sql_order_id = self.new_id
            else:
                QMessageBox.critical(self, "Ошибка id в save_sql", "Ошибка нету id заказа. Это не нормально", QMessageBox.Ok)
                return False

            sql_new = []
            sql_upd = []
            sql_del = []
            sql_shipped_position = []
            if not self.sql_shipped and shipped == 1:
                str_transaction = "Заказ %s - отгружен" % self.le_number_doc.text()
            elif self.sql_shipped and shipped == 0:
                str_transaction = "Заказ %s - отменен" % self.le_number_doc.text()
            else:
                str_transaction = ""
            for row in range(self.tw_position.rowCount()):
                table_item = self.tw_position.item(row, 2)
                if table_item.data(-1) == "new":
                    sql_new.append((sql_order_id, table_item.data(5), self.tw_position.item(row, 4).text(), self.tw_position.item(row, 4).data(5),
                                    self.tw_position.item(row, 5).text(), self.tw_position.item(row, 5).data(5)))
                    if str_transaction:
                        sql_shipped_position.append([table_item.data(5), int(self.tw_position.item(row, 5).text()), str_transaction])
                elif table_item.data(-1) == "upd":
                    sql_upd.append((sql_order_id, table_item.data(5), self.tw_position.item(row, 4).text(), self.tw_position.item(row, 4).data(5),
                                    self.tw_position.item(row, 5).text(), self.tw_position.item(row, 5).data(5), table_item.data(-2)))
                    if str_transaction:
                        sql_shipped_position.append([table_item.data(5), int(self.tw_position.item(row, 5).text()), str_transaction])
                elif table_item.data(-1) == "del":
                    sql_del.append((table_item.data(-2),))
                elif table_item.data(-1) == "set":
                    if str_transaction:
                        sql_shipped_position.append([table_item.data(5), int(self.tw_position.item(row, 5).text()), str_transaction])
                else:
                    QMessageBox.critical(self, "Ошибка состояния в save_sql", "Ошибка Непонятное sql состояние строки. Это не нормально!", QMessageBox.Ok)
                    return False

            if sql_new:
                query = "INSERT INTO order_position (Order_Id, Product_Article_Parametr_Id, Price, NDS, Value, In_On_Place) VALUES (%s, %s, %s, %s, %s, %s)"
                sql_info = my_sql.sql_many(query, sql_new)
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql добавления позиций", sql_info.msg, QMessageBox.Ok)
                    return False
            elif sql_upd:
                query = "UPDATE order_position SET Order_Id = %s, Product_Article_Parametr_Id = %s, Price = %s, NDS = %s, Value = %s, In_On_Place = %s WHERE Id = %s"
                for sql_tuple in sql_upd:
                    sql_info = my_sql.sql_change(query, sql_tuple)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql изменения позиции", sql_info.msg, QMessageBox.Ok)
                        return False
            elif sql_del:
                query = "DELETE FROM order_position WHERE Id = %s"
                for sql_tuple in sql_del:
                    sql_info = my_sql.sql_change(query, sql_tuple)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql удаления позиции", sql_info.msg, QMessageBox.Ok)
                        return False

            if sql_shipped_position:
                sql_connect_transaction = my_sql.sql_start_transaction()
                if shipped == 0:
                    query = "UPDATE product_article_warehouse SET Value_In_Warehouse = Value_In_Warehouse + %s WHERE Id_Article_Parametr = %s"
                else:
                    query = "UPDATE product_article_warehouse SET Value_In_Warehouse = Value_In_Warehouse - %s WHERE Id_Article_Parametr = %s"
                for item in sql_shipped_position:
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (item[1], item[0]))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        QMessageBox.critical(self, "Ошибка sql изменения склада", sql_info.msg, QMessageBox.Ok)
                        return False

                if shipped == 0:
                    query = "INSERT INTO transaction_records_warehouse (Article_Parametr_Id, Date, Balance, Note) VALUES (%s, NOW(), %s, %s)"
                else:
                    query = "INSERT INTO transaction_records_warehouse (Article_Parametr_Id, Date, Balance, Note) VALUES (%s, NOW(), -%s, %s)"
                sql_info = my_sql.sql_many_transaction(sql_connect_transaction, query, sql_shipped_position)
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql добавления записей изменения склада", sql_info.msg, QMessageBox.Ok)
                    return False

                query = "UPDATE `order` SET Shipped = %s WHERE Id = %s"
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (shipped, self.id))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql добавления записей изменения склада", sql_info.msg, QMessageBox.Ok)
                    return False

                my_sql.sql_commit_transaction(sql_connect_transaction)

        return True

    def of_set_client(self, id_client, name_client):
        self.le_client.setText(str(name_client))
        self.le_client.setWhatsThis(str(id_client))

        query = "SELECT No_Nds FROM clients WHERE Id = %s"
        parametrs = (id_client,)
        sql_info = my_sql.sql_select(query, parametrs)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение НДС/Не НДС", sql_info.msg, QMessageBox.Ok)
            return False

        if sql_info[0][0]:
            self.lb_client.setText("<html><head/><body><p align='center'> Клиент (Без НДС) </p></body></html>")
            self.lb_client.setWhatsThis("no_nds")
        else:
            self.lb_client.setText("<html><head/><body><p align='center'> Клиент (C НДС) </p></body></html>")
            self.lb_client.setWhatsThis("nds")

        query = "SELECT Id, Name, Adres FROM clients_actual_address WHERE Client_Id = %s"
        parametrs = (id_client,)
        sql_info = my_sql.sql_select(query, parametrs)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение адресов клиента", sql_info.msg, QMessageBox.Ok)
            return False

        if not sql_info:
            query = "SELECT Actual_Address FROM clients WHERE Id = %s"
            parametrs = (id_client,)
            sql_info = my_sql.sql_select(query, parametrs)
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение адреса клиента", sql_info.msg, QMessageBox.Ok)
                return False
            if sql_info[0][0] == "":
                self.cb_clients_adress.clear()
                self.cb_clients_adress.addItem("None", None)
                self.cb_clients_adress.setEnabled(False)
            else:
                self.cb_clients_adress.clear()
                self.cb_clients_adress.addItem(sql_info[0][0], -1)
                self.cb_clients_adress.setEnabled(False)

        else:
            self.cb_clients_adress.clear()
            self.cb_clients_adress.setEnabled(True)
            for item in sql_info:
                self.cb_clients_adress.addItem(item[1], item[0])

        query = 'SELECT Id,CONCAT_WS(", ", Number, Contract, Data_From) FROM clients_vendor_number WHERE Client_Id = %s'
        parametrs = (id_client,)
        sql_info = my_sql.sql_select(query, parametrs)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение номеров клиента", sql_info.msg, QMessageBox.Ok)
            return False

        if sql_info:
            self.cb_clients_vendor.clear()
            self.cb_clients_vendor.setEnabled(True)
            for item in sql_info:
                self.cb_clients_vendor.addItem(item[1], item[0])
        else:
            self.cb_clients_vendor.clear()
            self.cb_clients_vendor.addItem("None", None)
            self.cb_clients_vendor.setEnabled(False)

        self.pb_add_position.setEnabled(True)
        self.pb_change_position.setEnabled(True)
        self.pb_dell_position.setEnabled(True)

    def of_list_insert(self, item):
        self.le_transport_company.setText(item[1])
        self.le_transport_company.setWhatsThis(str(item[0]))

    def of_ex_torg12(self, head=True, article=False):

        path = QFileDialog.getSaveFileName(self, "Сохранение")
        if not path[0]:
            return False

        border_all = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
        border_all_big = Border(left=Side(style='medium'), right=Side(style='medium'), top=Side(style='medium'), bottom=Side(style='medium'))

        font_7 = Font(name="Arial", size=7)

        ald_center = Alignment(horizontal="center")
        ald_right = Alignment(horizontal="right")

        wite = PatternFill(start_color='ffffff',
                              end_color='ffffff',
                              fill_type='solid')

        book = openpyxl.load_workbook(filename='%s\\Накладная 2.xlsx' % (getcwd() + "\\templates\\order",))
        sheet = book['Отчет']

        sheet.oddHeader.left.text = "Продолжение накладной № %s от %s г." % (self.le_number_doc.text(), self.de_date_shipment.date().toString("dd.MM.yyyy"))
        sheet.oddHeader.left.size = 7


        # заполнение шапки
        if not head:
            sheet["A1"] = ""

        query = "SELECT Name,  INN, KPP, Actual_Address, Legal_Address, Account, Bank, corres_Account, BIK FROM clients WHERE Id = %s"
        sql_info = my_sql.sql_select(query, (self.le_client.whatsThis(), ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения информации о клиенте", sql_info.msg, QMessageBox.Ok)
            return False

        client = sql_info[0][0] + " ИНН " + str(sql_info[0][1])
        if sql_info[0][2]:
            client += " КПП " + str(sql_info[0][2])
        client += ", " + sql_info[0][3] + ",р/с " + str(sql_info[0][5]) + " в " + sql_info[0][6] + " к/с " + str(sql_info[0][7]) + " БИК " + str(sql_info[0][8])
        sheet["C7"] = client

        client = sql_info[0][0] + " ИНН " + str(sql_info[0][1])
        if sql_info[0][2]:
            client += " КПП " + str(sql_info[0][2])
        client += ", " + sql_info[0][4] + ",р/с " + str(sql_info[0][5]) + " в " + sql_info[0][6] + " к/с " + str(sql_info[0][7]) + " БИК " + str(sql_info[0][8])
        sheet["C11"] = client

        if self.cb_clients_vendor.currentData():
            query = "SELECT Number, Contract, Data_From FROM clients_vendor_number WHERE Client_Id = %s"
            sql_info = my_sql.sql_select(query, (self.le_client.whatsThis(), ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения информации номера поставщика", sql_info.msg, QMessageBox.Ok)
                return False

            base = "№ заказа " + self.le_number_order.text() + ", Номер поставщика " + str(sql_info[0][0]) \
                   + " договор поставки № " + str(sql_info[0][1]) + " от " + sql_info[0][2].strftime("%d.%m.%Y")

            sheet["C13"] = base

        # заполнение середины
        sheet["G16"] = self.le_number_doc.text()
        sheet["I16"] = self.de_date_shipment.date().toString("dd.MM.yyyy")
        sheet["G16"].border = border_all_big
        sheet["I16"].border = border_all_big

        all_value = 0
        all_no_nds = 0
        all_nds = 0
        all_sum = 0

        row_break = 11
        row_ex = 21
        for row in range(self.tw_position.rowCount()):
            query = "SELECT Barcode, Client_code FROM product_article_parametrs WHERE Id = %s"
            sql_info = my_sql.sql_select(query, (self.tw_position.item(row, 2).data(5),))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения информации номера поставщика", sql_info.msg, QMessageBox.Ok)
                return False
            if article:
                name = self.tw_position.item(row, 3).text() + " а " + self.tw_position.item(row, 0).text() + \
                       " р " + self.tw_position.item(row, 1).text() + " " + str(sql_info[0][0])
            else:
                name = self.tw_position.item(row, 3).text() + " " + str(sql_info[0][0])
            nds = self.tw_position.item(row, 4).data(5)
            no_nds_price = round(float(self.tw_position.item(row, 4).text()) - (float(self.tw_position.item(row, 4).text()) * float(nds))
                                 / (100 + float(nds)), 2)
            sum = round(int(self.tw_position.item(row, 5).text()) * float(self.tw_position.item(row, 4).text()), 2)
            sum_no_nds = round(float(sum) - (float(sum) * float(nds)) / (100 + float(nds)), 2)

            sheet.merge_cells("B%s:D%s" % (row_ex, row_ex))
            sheet.merge_cells("L%s:M%s" % (row_ex, row_ex))
            sheet.merge_cells("N%s:O%s" % (row_ex, row_ex))
            sheet.merge_cells("P%s:Q%s" % (row_ex, row_ex))
            sheet.merge_cells("R%s:S%s" % (row_ex, row_ex))
            sheet.merge_cells("T%s:U%s" % (row_ex, row_ex))

            sheet["A%s" % row_ex] = row + 1
            sheet["B%s" % row_ex] = name
            sheet["B%s" % row_ex].font = font_7
            sheet["E%s" % row_ex] = str(sql_info[0][1])
            sheet["F%s" % row_ex] = "шт."
            sheet["G%s" % row_ex] = "796"
            sheet["H%s" % row_ex] = "кор."
            sheet["I%s" % row_ex] = self.tw_position.item(row, 5).data(5)
            sheet["J%s" % row_ex] = int(int(self.tw_position.item(row, 5).text()) / int(self.tw_position.item(row, 5).data(5)))
            sheet["L%s" % row_ex] = int(self.tw_position.item(row, 5).text())
            sheet["N%s" % row_ex] = no_nds_price
            sheet["P%s" % row_ex] = sum_no_nds
            sheet["R%s" % row_ex] = nds
            sheet["T%s" % row_ex] = round(sum - sum_no_nds, 2)
            sheet["V%s" % row_ex] = sum

            all_value += int(self.tw_position.item(row, 5).text())
            all_no_nds += sum_no_nds
            all_nds += round(sum - sum_no_nds, 2)
            all_sum += sum

            sheet.row_dimensions[row_ex].height = 23

            if row_break == 25:
                sheet.page_breaks.append(Break(row_ex))
                row_break = 0

            row_break += 1
            row_ex += 1

        if row_break + 8 > 25:
            sheet.page_breaks.append(Break(row_ex-4))

        # Заполняем сумму
        sheet["K%s" % row_ex] = "Всего по накладной"
        sheet["K%s" % row_ex].alignment = ald_right

        sheet.merge_cells("L%s:M%s" % (row_ex, row_ex))
        sheet["L%s" % row_ex] = all_value
        sheet["L%s" % row_ex].alignment = ald_right

        sheet.merge_cells("N%s:O%s" % (row_ex, row_ex))
        sheet["N%s" % row_ex] = "X"
        sheet["N%s" % row_ex].alignment = ald_center

        sheet.merge_cells("P%s:Q%s" % (row_ex, row_ex))
        sheet["P%s" % row_ex] = all_no_nds
        sheet["P%s" % row_ex].alignment = ald_right

        sheet.merge_cells("R%s:S%s" % (row_ex, row_ex))
        sheet["R%s" % row_ex] = "X"
        sheet["R%s" % row_ex].alignment = ald_center

        sheet.merge_cells("T%s:U%s" % (row_ex, row_ex))
        sheet["T%s" % row_ex] = all_nds
        sheet["T%s" % row_ex].alignment = ald_right

        sheet["V%s" % row_ex] = all_sum
        sheet["V%s" % row_ex].alignment = ald_right

        for row in sheet.iter_rows(min_row=row_ex, min_col=12, max_col=22):
            for cell in row:
                cell.border = border_all

        row_ex += 1

        # Формируем шапку
        for row in sheet.iter_rows(min_row=18, max_col=22, max_row=20):
            for cell in row:
                    cell.border = border_all_big

        for row in sheet.iter_rows(min_row=3, min_col=20, max_row=4):
            for cell in row:
                cell.border = border_all_big

        for row in sheet.iter_rows(min_row=16, min_col=7, max_col=11):
            for cell in row:
                cell.border = border_all_big

        for row in sheet.iter_rows(min_row=12, min_col=17, max_col=19, max_row=15):
            for cell in row:
                cell.border = border_all

        # Формируем границы таблицы
        for row in sheet.iter_rows(min_row=21, max_col=22, max_row=row_ex-2):
            for cell in row:
                cell.border = border_all

        sheet2 = book['Низ']

        for row in sheet2.iter_rows(min_row=1, max_col=22, max_row=17):
            for cell in row:
                sheet["%s%s" % (cell.column, row_ex)] = cell.value
                sheet.row_dimensions[row_ex].height = sheet2.row_dimensions[cell.row].height
                if cell.has_style:
                    sheet["%s%s" % (cell.column, row_ex)].border = copy(cell.border)
                    sheet["%s%s" % (cell.column, row_ex)].font = copy(cell.font)
                    sheet["%s%s" % (cell.column, row_ex)].fill = wite

            row_ex += 1

        book.save(path[0] + ".xlsx")


class Position(QDialog, position_class):
    def __init__(self):
        super(Position, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

    def ui_calculation(self):
        if self.nds_1.isChecked():
            nds = 18
        elif self.nds_2.isChecked():
            nds = 10
        else:
            nds = 0

        try:
            value = int(self.le_value.text().replace(",", "."))
        except:
            value = 0
        try:
            if self.price_name_change == "nds":
                price = round(float(self.le_price.text().replace(",", ".")), 4)
                price_no_nds = round(price - (price * nds) / (100 + nds), 4)
            elif self.price_name_change == "no nds":
                price_no_nds = round(float(self.le_price_no_nds.text().replace(",", ".")), 4)
                price = round(price_no_nds * (0.01 * nds + 1), 4)
            else:
                price = 0.0
                price_no_nds = 0.0
        except:
            price = 0.0
            price_no_nds = 0.0
        try:
            in_on_place = int(self.le_in_on_place.text().replace(",", "."))
        except:
            in_on_place = 0

        if value:
            if self.price_name_change == "nds":
                self.le_price_no_nds.setText(str(round(price_no_nds, 4)))
            elif self.price_name_change == "no nds":
                self.le_price.setText(str(round(price, 4)))
            sum_rub = round(value * price, 4)
            self.le_sum_rub.setText(str(sum_rub))
            if nds:
                self.le_sum_no_nds.setText(str(round(price_no_nds * value, 4)))
                self.le_sum_nds.setText(str(round((price * nds) / (100 + nds) * value, 4)))

        if in_on_place:
            self.le_place_all.setText(str(round(value / in_on_place, 1)))

    def ui_price_nds_change(self):
        self.price_name_change = "nds"
        self.ui_calculation()

    def ui_price_no_nds_change(self):
        self.price_name_change = "no nds"
        self.ui_calculation()

    def ui_view_article(self):
        self.article_list = article.ArticleList(self, True)
        self.article_list.setWindowModality(Qt.ApplicationModal)
        self.article_list.show()

    def ui_acc(self):
        self.done(1)
        self.close()
        self.destroy()

    def ui_cancel(self):
        self.done(0)
        self.close()
        self.destroy()

    def of_tree_select_article(self, article):
        self.article_list.close()
        self.article_list.destroy()
        self.le_article.setText(article["article"])
        self.le_size.setText(article["size"])
        self.le_parametr.setText(article["parametr"])
        self.le_parametr.setWhatsThis(str(article["parametr_id"]))
        self.le_price.setText(article["price"])
        self.le_in_on_place.setText(article["in on place"])
        if article["nds"] == 18:
            self.nds_1.setChecked(True)
        else:
            self.nds_2.setChecked(True)

        self.price_name_change = "nds"
        self.ui_calculation()


class TransportCompanyName(list.ListItems):
    def set_settings(self):
        self.setWindowTitle("Список транспорт компаний")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(211, 49, 60);")  # Цвет бара
        self.title_new_window = "ТК"  # Имя вызываемых окон
        self.resize(300, 400)

        self.sql_list = "SELECT Id, Name FROM order_transport_company"
        self.sql_add = "INSERT INTO order_transport_company (Name, Details) VALUES (%s, %s)"
        self.sql_change_select = "SELECT Name, Details FROM order_transport_company WHERE Id = %s"
        self.sql_update_select = 'UPDATE order_transport_company SET Name = %s, Details = %s WHERE Id = %s'
        self.sql_dell = "DELETE FROM order_transport_company WHERE Id = %s"

        self.set_new_win = {"WinTitle": "ТК",
                            "WinColor": "(211, 49, 60)",
                            "lb_name": "Название",
                            "lb_note": "Подробность"}


class OrderDocList(QDialog, order_doc):
    def __init__(self, main):
        super(OrderDocList, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main

    def ui_double_click(self, item):
        doc_name = item.text()

        if doc_name == "Накладная с шапкой":
            self.main.of_ex_torg12(head=True, article=False)
        elif doc_name == "Накладная без шапки":
            self.main.of_ex_torg12(head=False, article=False)
        elif doc_name == "Накладная с шапкой + артикул":
            self.main.of_ex_torg12(head=False, article=True)
        elif doc_name == "Накладная без шапки + артикул":
            self.main.of_ex_torg12(head=False, article=True)

        self.close()
        self.destroy()
