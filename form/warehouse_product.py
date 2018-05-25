from os import getcwd
from form import article
from form.pack import PackBrows
from form.order import Order
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QLineEdit, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5 import QtCore
from function import my_sql
import logging
import logging.config
from classes.my_class import User


# Просто перепишем окно отображения артикулов под склад.
class Warehouse(article.ArticleList):
    def set_settings(self):
        self.setWindowTitle("Склад продукции")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(167, 183, 255);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Артикул", 57), ("Размер", 50), ("Параметр", 80), ("Название", 140), ("В цеху", 50), ("На складе", 70), ("В заказах", 65))

        self.query_tree_select = "SELECT Id, Parent_Id, Name FROM product_tree"
        self.query_tree_add = "INSERT INTO product_tree (Parent_Id, Name) VALUES (%s, %s)"
        self.query_tree_change = "UPDATE product_tree SET Name = %s WHERE Id = %s"
        self.query_tree_del = "DELETE FROM product_tree WHERE Id = %s"

        #  нулевой элемент должен быть ID а первый Parent_ID (ID категории)
        self.query_table_select = """SELECT product_article_parametrs.Id, product_article.Tree_Id,
                                        product_article.Article, product_article_size.Size, product_article_parametrs.Name, product_article.Name,
                                                      IFNULL((SELECT SUM(pack.Value_Pieces)
                                                        FROM pack
                                                        WHERE Date_Make IS NULL AND pack.Article_Parametr_Id = product_article_parametrs.Id
                                                        GROUP BY pack.Article_Parametr_Id), 0) AS c,
                                        product_article_warehouse.Value_In_Warehouse AS w,
                                                       (SELECT SUM(order_position.Value) - (c + w)
                                                        FROM order_position LEFT JOIN `order` ON order_position.Order_Id = `order`.Id
                                                        WHERE `order`.Shipped = 0 AND order_position.Product_Article_Parametr_Id = product_article_parametrs.Id
                                                        GROUP BY order_position.Product_Article_Parametr_Id)
                                      FROM product_article_parametrs LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                                        LEFT JOIN product_article_warehouse ON product_article_parametrs.Id = product_article_warehouse.Id_Article_Parametr"""

        self.query_table_all = self.query_table_select

        self.query_transfer_item = ""
        self.query_table_dell = ""

        # Настройки окна добавления и редактирования дерева
        self.set_new_win_tree = {"WinTitle": "Добавление категории",
                                 "WinColor": "(167, 183, 255)",
                                 "lb_name": "Название категории"}

        # Настройки окна переноса элементов
        self.set_transfer_win = {"WinTitle": "Изменение категории",
                                 "WinColor": "(167, 183, 255)"}

        self.pb_tree_add.deleteLater()
        self.pb_tree_change.deleteLater()
        self.pb_tree_dell.deleteLater()
        self.action123.deleteLater()
        self.pb_table_add.deleteLater()
        self.pb_table_change.deleteLater()
        self.pb_table_dell.deleteLater()
        self.pb_table_transfer.deleteLater()
        self.pb_table_double.deleteLater()
        self.pb_table_filter.deleteLater()

        # Быстрый фильтр
        self.le_fast_filter = QLineEdit()
        self.le_fast_filter.setPlaceholderText("Артикул")
        self.le_fast_filter.setMaximumWidth(150)
        self.le_fast_filter.editingFinished.connect(self.fast_filter)
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(dummy)
        self.toolBar.addWidget(self.le_fast_filter)

        self.pb_other.setText("Корректировка склада")

    def ui_double_click_table_item(self, item):  # Двойной клик по элементу
        if not self.dc_select:
            id = item.data(5)
            self.warehouse_info = WarehouseInfo(id)
            self.warehouse_info.setModal(True)
            self.warehouse_info.show()
        else:
            # что хотим получить ставим всместо 0
            item = (self.table_widget.item(item.row(), 0).text() + " (" + self.table_widget.item(item.row(), 1).text() + ") [" + self.table_widget.item(item.row(), 2).text() + "]",
                    item.data(5))
            self.main.of_tree_select_warehouse(item)
            self.close()
            self.destroy()

    def ui_other(self):
        try:
            item_id = self.table_widget.selectedItems()[0].data(5)
            row_item = self.table_widget.selectedItems()[0].row()
            item_name = self.table_widget.item(row_item, 0).text() + " (" + self.table_widget.item(row_item, 1).text() + ") [" + self.table_widget.item(row_item, 2).text() + "]"
        except:
            QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
            return False

        self.warehouse_change = WarehouseChange(self, item_id, item_name)
        self.warehouse_change.setModal(True)
        self.warehouse_change.show()

    def fast_filter(self):
        # Блок условий артикула
        if self.le_fast_filter.text() != '':
            q_filter = " WHERE (product_article.Article LIKE '%s')" % ("%" + self.le_fast_filter.text() + "%", )
            self.query_table_select = self.query_table_all + q_filter
        else:
            self.query_table_select = self.query_table_all

        self.ui_update_table()


class WarehouseChange(QDialog):
    def __init__(self, main, id, name):
        super(WarehouseChange, self).__init__()
        loadUi(getcwd() + '/ui/warehouse_product_change.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        logging.config.fileConfig(getcwd() + '/setting/logger_conf.ini')
        self.logger = logging.getLogger("WarehouseALog")

        self.main = main
        self.id = id
        self.name = name

        self.tab_number = 0

        self.le_art_name.setText(name)
        self.le_art_name.setWhatsThis(str(id))

        self.le_art_name_minus.setText(name)
        self.le_art_name_minus.setWhatsThis(str(id))

        self.de_date_1.setDate(QtCore.QDate.currentDate())
        self.de_date_2.setDate(QtCore.QDate.currentDate())

    def ui_view_warehouse(self):
        self.warehouse = Warehouse(self, True)
        self.warehouse.setWindowModality(QtCore.Qt.ApplicationModal)
        self.warehouse.show()

    def ui_change_tab(self, tab):
        self.tab_number = tab

    def ui_acc(self):
        # Получим данные для лога
        query = """SELECT Value_In_Warehouse FROM product_article_warehouse WHERE Id_Article_Parametr = %s"""
        sql_info = my_sql.sql_select(query, (int(self.le_balance.text()), self.id))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение данных для лога склада", sql_info.msg, QMessageBox.Ok)
            return False

        history_warehouse = sql_info[0][0]

        query = """SELECT SUM(Balance) FROM transaction_records_warehouse WHERE Article_Parametr_Id = %s"""
        sql_info = my_sql.sql_select(query, (int(self.le_balance.text()), self.id))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение данных для лога транзакций", sql_info.msg, QMessageBox.Ok)
            return False

        history_warehouse_transaction = sql_info[0][0]

        if self.tab_number == 0:
            log_text = "Добавленно изменение"
            sql_connect_transaction = my_sql.sql_start_transaction()
            query = """UPDATE product_article_warehouse
                          SET Value_In_Warehouse = Value_In_Warehouse + %s
                          WHERE Id_Article_Parametr = %s"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (int(self.le_balance.text()), self.id))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql изменение склада", sql_info.msg, QMessageBox.Ok)
                return False

            query = """INSERT INTO transaction_records_warehouse (Article_Parametr_Id, Date, Balance, Note, Code)
                        VALUES (%s, %s, %s, %s, 350)"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.id, self.de_date_1.date().toString(QtCore.Qt.ISODate),
                                                                                      int(self.le_balance.text()), self.le_note_1.text()))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql запись изменения склада", sql_info.msg, QMessageBox.Ok)
                return False

            my_sql.sql_commit_transaction(sql_connect_transaction)

            self.logger.info(u"[Артикул ID {:04d} Пользователь {:04d}] {}".format(self.id, User().id(), "%s" % log_text))
            self.logger.info(u"[Артикул ID {:04d} Пользователь {:04d}] {}".format(self.id, User().id(), "Остаток ДО на складе %s По транзакциям %s" %
                                                                                  (history_warehouse, history_warehouse_transaction)))
            self.logger.info(u"[Артикул ID {:04d} Пользователь {:04d}] {}".format(self.id, User().id(), "Изменено %s" % self.le_balance.text()))

        elif self.tab_number == 1:
            # Получим данные для лога второго артикула
            log_text = "Добавленно перешитие"

            query = """SELECT Value_In_Warehouse FROM product_article_warehouse WHERE Id_Article_Parametr = %s"""
            sql_info = my_sql.sql_select(query, (self.le_art_name_plus.whatsThis(), ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение данных для лога склада", sql_info.msg, QMessageBox.Ok)
                return False
            history_warehouse_2 = sql_info[0][0]

            query = """SELECT SUM(Balance) FROM transaction_records_warehouse WHERE Article_Parametr_Id = %s"""
            sql_info = my_sql.sql_select(query, (self.le_art_name_plus.whatsThis(), ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение данных для лога транзакций", sql_info.msg, QMessageBox.Ok)
                return False
            history_warehouse_transaction_2 = sql_info[0][0]

            # Изменяем перешиваемое
            sql_connect_transaction = my_sql.sql_start_transaction()
            query = """UPDATE product_article_warehouse
                                      SET Value_In_Warehouse = Value_In_Warehouse - %s
                                      WHERE Id_Article_Parametr = %s"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (int(self.le_balance_2.text()), self.id))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql изменение склада при перешитии", sql_info.msg, QMessageBox.Ok)
                return False

            query = """INSERT INTO transaction_records_warehouse (Article_Parametr_Id, Date, Balance, Note, Code)
                                    VALUES (%s, %s, %s, %s, 351)"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.id, self.de_date_2.date().toString(QtCore.Qt.ISODate),
                                                                                      -int(self.le_balance_2.text()), self.le_note_2.text()))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql запись изменения склада", sql_info.msg, QMessageBox.Ok)
                return False

            # Добавляем перешитое
            query = """UPDATE product_article_warehouse
                                                  SET Value_In_Warehouse = Value_In_Warehouse + %s
                                                  WHERE Id_Article_Parametr = %s"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (int(self.le_balance_2.text()), self.le_art_name_plus.whatsThis()))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql изменение склада при перешитии", sql_info.msg, QMessageBox.Ok)
                return False

            query = """INSERT INTO transaction_records_warehouse (Article_Parametr_Id, Date, Balance, Note, Code)
                                                VALUES (%s, %s, %s, %s, 352)"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.le_art_name_plus.whatsThis(),
                                                                                      self.de_date_2.date().toString(QtCore.Qt.ISODate),
                                                                                      int(self.le_balance_2.text()), self.le_note_2.text()))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql запись изменения склада", sql_info.msg, QMessageBox.Ok)
                return False

            my_sql.sql_commit_transaction(sql_connect_transaction)

            self.logger.info(u"[Артикул ID {:04d} Пользователь {:04d}] {}".format(self.id, User().id(), "%s" % log_text))
            self.logger.info(u"[Артикул ID {:04d} Пользователь {:04d}] {}".format(self.id, User().id(), "Что перешили"))
            self.logger.info(u"[Артикул ID {:04d} Пользователь {:04d}] {}".format(self.id, User().id(), "Остаток ДО на складе %s По транзакциям %s" %
                                                                                  (history_warehouse, history_warehouse_transaction)))
            self.logger.info(u"[Артикул ID {:04d} Пользователь {:04d}] {}".format(self.id, User().id(), "Изменено %s" % self.le_balance_2.text()))

            self.logger.info(u"[Артикул ID {:04d} Пользователь {:04d}] {}".format(self.id, User().id(), "На что перешили"))
            self.logger.info(u"[Артикул ID {:04d} Пользователь {:04d}] {}".format(self.id, User().id(), "Остаток ДО на складе %s По транзакциям %s" %
                                                                                  (history_warehouse_2, history_warehouse_transaction_2)))
            self.logger.info(u"[Артикул ID {:04d} Пользователь {:04d}] {}".format(self.id, User().id(), "Изменено %s" % self.le_balance_2.text()))



        self.main.ui_update_table()
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()

    def of_tree_select_warehouse(self, item):
        self.le_art_name_plus.setText(item[0])
        self.le_art_name_plus.setWhatsThis(str(item[1]))


class WarehouseInfo(QDialog):
    def __init__(self, id):
        super(WarehouseInfo, self).__init__()
        loadUi(getcwd() + '/ui/warehouse_product_info.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.id = id

        self.date = QtCore.QDate.currentDate()
        self.de_from.setDate(self.date.addMonths(-3))
        self.de_to.setDate(self.date)
        self.de_date_to.setDate(self.date)

        self.set_size_table()
        self.sql_info()

    def ui_new_date(self):
        query = """SELECT Id, Date, Balance, Note
                                      FROM transaction_records_warehouse
                                      WHERE Article_Parametr_Id = %s AND Date >= %s AND Date <= %s
                                      ORDER BY Date"""
        sql_info_warehouse = my_sql.sql_select(query, (self.id, self.de_from.date().toString(1), self.de_to.date().toString(1)))
        if "mysql.connector.errors" in str(type(sql_info_warehouse)):
            QMessageBox.critical(self, "Ошибка sql получение склада", sql_info_warehouse.msg, QMessageBox.Ok)
            return False

        self.warehouse = sql_info_warehouse
        self.set_warehouse_table()

    def ui_pack_double_click(self, item):
        self.pack = PackBrows(pack_id=item.data(-2))
        self.pack.setWindowModality(QtCore.Qt.ApplicationModal)
        self.pack.show()

    def ui_order_double_click(self, item):
        self.order = Order(id=item.data(-2))
        self.order.setWindowModality(QtCore.Qt.ApplicationModal)
        self.order.show()

    def ui_calc_date(self):
        query = """SELECT war.Value_In_Warehouse - (SELECT SUM(transaction_records_warehouse.Balance) FROM transaction_records_warehouse
                                                    WHERE transaction_records_warehouse.Article_Parametr_Id = war.Id_Article_Parametr
                                                      AND transaction_records_warehouse.Date > %s)
                      FROM product_article_warehouse AS war WHERE war.Id_Article_Parametr = %s"""
        sql_info = my_sql.sql_select(query, (self.de_date_to.date().toPyDate(), self.id))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение склада на дату", sql_info.msg, QMessageBox.Ok)
            return False

        warehouse = sql_info[0][0]
        self.le_warehouse_date.setText(str(warehouse))

        # Узнаем всю расчетную себестоимость
        query = """SELECT pr.Price, (
                              SELECT SUM(operations.Price)
                                FROM product_article_operation LEFT JOIN operations ON product_article_operation.Operation_Id = operations.Id
                                WHERE product_article_operation.Product_Article_Parametrs_Id = pr.Id
                          ),(
                              SELECT SUM(s)
                              FROM (SELECT material_supplyposition.Price * product_article_material.Value AS s
                                      FROM product_article_material
                                        LEFT JOIN material_supplyposition ON product_article_material.Material_Id = material_supplyposition.Material_NameId
                                        LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                        LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                                      WHERE product_article_material.Product_Article_Parametrs_Id = %s AND product_article_material.Material_Id IS NOT NULL
                                        AND material_balance.BalanceWeight > 0
                                      GROUP BY product_article_material.Material_Id) t
                          ),(
                              SELECT SUM(s)
                              FROM (SELECT accessories_supplyposition.Price * product_article_material.Value AS s
                                      FROM product_article_material
                                        LEFT JOIN accessories_supplyposition ON product_article_material.Accessories_Id = accessories_supplyposition.Accessories_NameId
                                        LEFT JOIN accessories_supply ON accessories_supplyposition.Accessories_SupplyId = accessories_supply.Id
                                        LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.Accessories_SupplyPositionId
                                      WHERE product_article_material.Product_Article_Parametrs_Id = %s AND product_article_material.Accessories_Id IS NOT NULL
                                            AND accessories_balance.BalanceValue > 0
                                      GROUP BY product_article_material.Accessories_Id) t
                          )
                      FROM product_article_parametrs AS pr WHERE pr.Id = %s"""
        sql_info = my_sql.sql_select(query, (self.id, self.id, self.id))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расчетной себестоимости + цены продажи", sql_info.msg, QMessageBox.Ok)
            return False

        if warehouse:
            self.le_price_one.setText(str(sql_info[0][0]))
            self.le_sebest_one.setText(str(sql_info[0][1] + sql_info[0][2] + sql_info[0][3]))
            self.le_price_many.setText(str(sql_info[0][0] * warehouse))
            self.le_sebest_many.setText(str((sql_info[0][1] + sql_info[0][2] + sql_info[0][3]) * warehouse))

    def sql_info(self):
        query = """SELECT pack.Id, pack.Cut_Id, pack.Number, pack.Value_Pieces, cut.Date_Cut
                      FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
                      WHERE Date_Make IS NULL AND pack.Article_Parametr_Id = %s
                      ORDER BY cut.Date_Cut"""
        sql_info_workshop = my_sql.sql_select(query, (self.id, ))
        if "mysql.connector.errors" in str(type(sql_info_workshop)):
            QMessageBox.critical(self, "Ошибка sql получение цеха", sql_info_workshop.msg, QMessageBox.Ok)
            return False

        query = """SELECT Id, Date, Balance, Note
                      FROM transaction_records_warehouse
                      WHERE Article_Parametr_Id = %s AND Date >= %s AND Date <= %s
                      ORDER BY Date DESC, Id DESC """
        sql_info_warehouse = my_sql.sql_select(query, (self.id, self.date.addMonths(-3).toString(1), self.date.toString(1)))
        if "mysql.connector.errors" in str(type(sql_info_warehouse)):
            QMessageBox.critical(self, "Ошибка sql получение склада", sql_info_warehouse.msg, QMessageBox.Ok)
            return False

        query = """SELECT `order`.Id, `order`.Number_Doc, clients.Name, `order`.Date_Order, order_position.Value
                      FROM order_position LEFT JOIN `order` ON order_position.Order_Id = `order`.Id
                        LEFT JOIN clients ON `order`.Client_Id = clients.Id
                      WHERE `order`.Shipped = 0 AND order_position.Product_Article_Parametr_Id = %s"""
        sql_info_order = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info_order)):
            QMessageBox.critical(self, "Ошибка sql получение заказов", sql_info_order.msg, QMessageBox.Ok)
            return False

        self.workshop = sql_info_workshop
        self.warehouse = sql_info_warehouse
        self.order = sql_info_order

        self.set_workshop_table()
        self.set_warehouse_table()
        self.set_order_table()

    def set_size_table(self):
        self.tw_workshop.horizontalHeader().resizeSection(0, 45)
        self.tw_workshop.horizontalHeader().resizeSection(1, 45)
        self.tw_workshop.horizontalHeader().resizeSection(2, 55)
        self.tw_workshop.horizontalHeader().resizeSection(3, 80)

        self.tw_warehouse.horizontalHeader().resizeSection(0, 50)
        self.tw_warehouse.horizontalHeader().resizeSection(1, 70)
        self.tw_warehouse.horizontalHeader().resizeSection(2, 50)
        self.tw_warehouse.horizontalHeader().resizeSection(3, 250)

        self.tw_order.horizontalHeader().resizeSection(0, 50)
        self.tw_order.horizontalHeader().resizeSection(1, 135)
        self.tw_order.horizontalHeader().resizeSection(2, 85)
        self.tw_order.horizontalHeader().resizeSection(3, 85)

    def set_workshop_table(self):

        self.tw_workshop.clearContents()
        self.tw_workshop.setRowCount(0)

        for row, pack in enumerate(self.workshop):
            self.tw_workshop.insertRow(row)

            new_table_item = QTableWidgetItem(str(pack[1]))
            new_table_item.setData(-2, pack[0])
            self.tw_workshop.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(pack[2]))
            new_table_item.setData(-2, pack[0])
            self.tw_workshop.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(pack[3]))
            new_table_item.setData(-2, pack[0])
            self.tw_workshop.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(pack[4].strftime("%d.%m.%Y"))
            new_table_item.setData(-2, pack[0])
            self.tw_workshop.setItem(row, 3, new_table_item)

    def set_warehouse_table(self):

        self.tw_warehouse.clearContents()
        self.tw_warehouse.setRowCount(0)

        for row, transaction in enumerate(self.warehouse):
            self.tw_warehouse.insertRow(row)

            if transaction[2] > 0:
                color = QBrush(QColor(150, 255, 161, 255))
            else:
                color = QBrush(QColor(252, 141, 141, 255))

            new_table_item = QTableWidgetItem(str(transaction[0]))
            new_table_item.setData(-2, transaction[0])
            new_table_item.setBackground(color)
            self.tw_warehouse.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(transaction[1].strftime("%d.%m.%Y"))
            new_table_item.setData(-2, transaction[0])
            new_table_item.setBackground(color)
            self.tw_warehouse.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(transaction[2]))
            new_table_item.setData(-2, transaction[0])
            new_table_item.setBackground(color)
            self.tw_warehouse.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(transaction[3]))
            new_table_item.setData(-2, transaction[0])
            new_table_item.setBackground(color)
            self.tw_warehouse.setItem(row, 3, new_table_item)

    def set_order_table(self):

        self.tw_order.clearContents()
        self.tw_order.setRowCount(0)

        for row, order in enumerate(self.order):
            self.tw_order.insertRow(row)

            new_table_item = QTableWidgetItem(str(order[1]))
            new_table_item.setData(-2, order[0])
            self.tw_order.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(order[2]))
            new_table_item.setData(-2, order[0])
            self.tw_order.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(order[3].strftime("%d.%m.%Y"))
            new_table_item.setData(-2, order[0])
            self.tw_order.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(order[4]))
            new_table_item.setData(-2, order[0])
            self.tw_order.setItem(row, 3, new_table_item)
