from os import getcwd
from form import order, staff
from datetime import datetime
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt, QDate, QObject
from form.supply_material import MaterialName
from form.pack import PackBrows

import re

from function import my_sql
from classes import cut

cut_list_class = loadUiType(getcwd() + '/ui/cut_list.ui')[0]
cut_brows_class = loadUiType(getcwd() + '/ui/cut_brows.ui')[0]

cut_list_mission_class = loadUiType(getcwd() + '/ui/cut_list_mission.ui')[0]
new_cut_mission_class = loadUiType(getcwd() + '/ui/cut_new_mission.ui')[0]
edit_cut_mission_class = loadUiType(getcwd() + '/ui/cut_edit_mission.ui')[0]


class CutList(QMainWindow, cut_list_class):
    def __init__(self):
        super(CutList, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_size_table()
        self.set_cut_table()

    def ui_add_cut(self):
        self.cut_window = CutBrows(self)
        self.cut_window.setModal(True)
        self.cut_window.show()

    def set_size_table(self):
        self.tw_cut_list.horizontalHeader().resizeSection(0, 35)
        self.tw_cut_list.horizontalHeader().resizeSection(1, 80)
        self.tw_cut_list.horizontalHeader().resizeSection(2, 80)
        self.tw_cut_list.horizontalHeader().resizeSection(3, 80)
        self.tw_cut_list.horizontalHeader().resizeSection(4, 55)
        self.tw_cut_list.horizontalHeader().resizeSection(5, 140)
        self.tw_cut_list.horizontalHeader().resizeSection(6, 220)

    def ui_double_table(self, table_item):
        self.cut_window = CutBrows(self, table_item.data(-2))
        self.cut_window.setModal(True)
        self.cut_window.show()

    def ui_del_cut(self):
        try:
            id = int(self.tw_cut_list.item(self.tw_cut_list.currentRow(), 0).data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите крой", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить крой?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            cut_del = cut.Cut(id)
            del_note = cut_del.del_sql()
            if not del_note[0]:
                QMessageBox.information(self, "Ошибка удаления кроя", del_note[1], QMessageBox.Ok)

            self.set_cut_table()
            return True
        else:
            return False

    def set_cut_table(self):
        query = """SELECT cut.Id, SUM(pack.Weight), cut.Weight_Rest, COUNT(pack.Id), staff_worker_info.Last_Name, cut.Note
                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                      LEFT JOIN staff_worker_info ON cut.Worker_Id = staff_worker_info.Id
                      GROUP BY cut.Id
                      ORDER BY Cut_Id DESC"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить список кроя")
            return False

        self.tw_cut_list.clearContents()
        self.tw_cut_list.setRowCount(0)

        for row, cut in enumerate(sql_info):
            self.tw_cut_list.insertRow(row)

            new_table_item = QTableWidgetItem(str(cut[0]))
            new_table_item.setData(-2, cut[0])
            self.tw_cut_list.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(cut[1]))
            new_table_item.setData(-2, cut[0])
            self.tw_cut_list.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(cut[2]))
            new_table_item.setData(-2, cut[0])
            self.tw_cut_list.setItem(row, 2, new_table_item)

            rest = cut[2] if cut[2] is not None else 0
            weight = cut[1] if cut[1] is not None else 0
            new_table_item = QTableWidgetItem(str(rest + weight))
            new_table_item.setData(-2, cut[0])
            self.tw_cut_list.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(cut[3]))
            new_table_item.setData(-2, cut[0])
            self.tw_cut_list.setItem(row, 4, new_table_item)

            new_table_item = QTableWidgetItem(str(cut[4]))
            new_table_item.setData(-2, cut[0])
            self.tw_cut_list.setItem(row, 5, new_table_item)

            new_table_item = QTableWidgetItem(str(cut[5]))
            new_table_item.setData(-2, cut[0])
            self.tw_cut_list.setItem(row, 6, new_table_item)

    def of_change_cut_complete(self):
        self.set_cut_table()


class CutBrows(QDialog, cut_brows_class):
    def __init__(self, main=None, cut_id=None):
        super(CutBrows, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.insert_values_sql = False
        self.cut = cut.Cut(cut_id)
        self.main = main

        self.set_start_info()
        self.set_size_table()

    def set_start_info(self):
        if self.cut.number() is None:
            self.le_number_cut.setText(str(self.cut.take_new_number()))
            self.de_cut_date.setDate(QDate.currentDate())
        else:
            self.insert_values_sql = True

            self.le_number_cut.setText(str(self.cut.number()))
            self.de_cut_date.setDate(self.cut.date())
            self.le_worker_cut.setWhatsThis(str(self.cut.worker_id()))
            self.le_worker_cut.setText(str(self.cut.worker_name()))
            self.le_material_price.setText(str(self.cut.material_price()))
            self.le_material_cut.setWhatsThis(str(self.cut.material_id()))
            self.le_material_cut.setText(str(self.cut.material_name()))
            self.le_weight_cut.setText(str(self.cut.weight()))
            self.le_weight_rest_cut.setText(str(self.cut.weight_rest()))
            self.le_all_weight_cut.setText(str(self.cut.weight_all()))
            self.le_rest_cut.setText(str(self.cut.percent_rest()))
            self.le_note_cut.setText(str(self.cut.note()))

            self.cut.take_pack_sql()
            self.set_pack()

            self.insert_values_sql = False

    def set_size_table(self):
        self.tw_pack.horizontalHeader().resizeSection(0, 35)
        self.tw_pack.horizontalHeader().resizeSection(1, 65)
        self.tw_pack.horizontalHeader().resizeSection(2, 55)
        self.tw_pack.horizontalHeader().resizeSection(3, 180)
        self.tw_pack.horizontalHeader().resizeSection(4, 55)
        self.tw_pack.horizontalHeader().resizeSection(5, 55)
        self.tw_pack.horizontalHeader().resizeSection(6, 65)
        self.tw_pack.horizontalHeader().resizeSection(7, 65)
        self.tw_pack.horizontalHeader().resizeSection(8, 65)

    def ui_edit_date_cut(self):
        if not self.insert_values_sql:
            self.cut.set_date(self.de_cut_date.date())

    def ui_edit_material_cut(self):
        if not self.insert_values_sql:
            price = self.cut.set_material_id(self.le_material_cut.whatsThis())
            self.le_material_price.setText(str(price))

            if not self.cut.change_cut_weight():
                self.bu_pack_add.setEnabled(False)
                self.bu_pack_change.setEnabled(False)
                self.bu_pack_del.setEnabled(False)

                self.le_weight_rest_cut.setText(str(self.cut.weight_rest_old()))
                self.le_weight_rest_cut.setReadOnly(True)
                self.le_weight_rest_cut.setStyleSheet("border: 4px solid;\nborder-color: rgb(247, 84, 84);")
                self.le_weight_rest_cut.setToolTip("При смене материала нельзя менять вес обрези!\n Изменения не сохранятся!")
            else:
                self.set_width_rest_color()

    def ui_edit_worker_cut(self):
        if not self.insert_values_sql:
            self.cut.set_worker_id(self.le_worker_cut.whatsThis())

    def ui_edit_width_cut(self):
        if not self.insert_values_sql:
            self.set_width_all()

    def ui_edit_width_rest_cut(self):
        if not self.insert_values_sql:
            self.cut.set_weight_rest(self.le_weight_rest_cut.text())
            self.set_width_rest_color()
            self.set_width_all()

    def ui_edit_note_cut(self):
        if not self.insert_values_sql:
            self.cut.set_note(self.le_note_cut.text())

    def ui_view_list_material(self):
        self.material_name = MaterialName(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_view_list_worker(self):
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_add_pack(self):
        if self.cut.material_id() is None:
            QMessageBox.critical(self, "Ошибка ткани", "Сначало выберите ткань.", QMessageBox.Ok)
            return False

        self.pack = cut.Pack()
        self.pack.set_number_pack(self.cut.take_new_number_pack())
        self.pack.set_number_cut(self.cut.number())
        self.pack.set_material_id(self.cut.material_id())

        self.pack_win = PackBrows(self, self.pack)
        self.pack_win.setModal(True)
        self.pack_win.show()

    def ui_edit_pack(self):
        try:
            id = int(self.tw_pack.item(self.tw_pack.currentRow(), 0).data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите пачку", QMessageBox.Ok)
            return False

        self.pack_win = PackBrows(self, self.cut.pack(id))
        self.pack_win.setModal(True)
        self.pack_win.show()

    def ui_del_pack(self):
        try:
            id = int(self.tw_pack.item(self.tw_pack.currentRow(), 0).data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите пачку", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить пачку?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            save_note = self.cut.pack(id).del_pack()
            if not save_note[0]:
                QMessageBox.critical(self, "Ошибка удаления пачки.", save_note[1], QMessageBox.Ok)
                return False

            self.cut.check_material_weight()
            self.le_weight_cut.setText(str(self.cut.weight()))
            self.cut.take_pack_sql()
            self.set_pack()
            return True
        else:
            return False

    def ui_double_click_pack(self, table_item):
        if self.cut.change_cut_weight():
            self.pack_win = PackBrows(self, self.cut.pack(table_item.data(-2)))
            self.pack_win.setModal(True)
            self.pack_win.show()

    def ui_acc(self):
        if self.cut.error_material():
            result = QMessageBox.question(self, "Сохранить?", "Что то не так с весом обрези.\nМогу сохранить без веса обрези!", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == 16384:
                pass
            else:
                return False

        save_note = self.cut.save_sql()
        if not save_note[0]:
            QMessageBox.critical(self, "Ошибка сохранения кроя", save_note[1], QMessageBox.Ok)
            return False

        if self.main is not None:
            self.main.of_change_cut_complete()
        self.close()
        self.destroy()

    def ui_can(self):
        if self.cut.need_save():
            result = QMessageBox.question(self, "Выйти?", "Есть несохраненая информация.\nТочно выйти без сохранения?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == 16384:
                self.close()
                self.destroy()
            else:
                return False
        else:
            self.close()
            self.destroy()

    def set_pack(self):
        self.tw_pack.clearContents()
        self.tw_pack.setRowCount(0)

        if not self.cut.pack_list():
            return False

        need_set_pack = len(self.cut.pack_list())
        pack_number_table = 1

        pack_list = self.cut.pack_list()
        row = 0
        while need_set_pack != 0:
            for pack_id, pack in pack_list.items():
                if pack.number_pack() == pack_number_table:
                    self.tw_pack.insertRow(row)

                    new_table_item = QTableWidgetItem(str(pack.number_pack()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 0, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.article()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 1, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.size()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 2, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.parametr_name()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 3, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.value()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 4, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.value_damage()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 5, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.weight()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 6, new_table_item)

                    date_make = pack.date_make().strftime("%d.%m.%Y") if pack.date_make() is not None else ""
                    new_table_item = QTableWidgetItem(date_make)
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 7, new_table_item)

                    date_complete = pack.date_complete().strftime("%d.%m.%Y") if pack.date_complete() is not None else ""
                    new_table_item = QTableWidgetItem(date_complete)
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 8, new_table_item)

                    row += 1
                    pack_number_table += 1
                    need_set_pack -= 1
                    break
            else:
                    pack_number_table += 1

    def set_width_all(self):
        self.le_all_weight_cut.setText(str(self.cut.weight_all()))
        self.le_rest_cut.setText(str(self.cut.rest_percent()))

    def set_material_price(self):
        self.le_material_price.setText(str(self.cut.material_price()))

    def set_width_rest_color(self):
        material_check = self.cut.check_balance_material()
        if material_check[0]:
            self.le_weight_rest_cut.setStyleSheet("border: 4px solid;\nborder-color: rgb(122, 247, 84);")
            self.le_weight_rest_cut.setToolTip(material_check[1])
        else:
            self.le_weight_rest_cut.setStyleSheet("border: 4px solid;\nborder-color: rgb(247, 84, 84);")
            self.le_weight_rest_cut.setToolTip(material_check[1])

    def of_list_material_name(self, item):
        result = self.cut.check_balance_new_material(item[0])
        if result[0]:
            self.le_material_cut.setWhatsThis(str(item[0]))
            self.le_material_cut.setText(item[1])
        else:
            QMessageBox.critical(self, "Ошибка новой ткани", result[1], QMessageBox.Ok)
            return False

    def of_list_worker(self, item):
        self.le_worker_cut.setWhatsThis(str(item[0]))
        self.le_worker_cut.setText(item[1])

    def of_cut_id(self):
        if self.cut.id() is None:
            return self.cut.new_save()
        else:
            return self.cut.id()

    def of_save_pack_complete(self):
        self.cut.check_material_weight()
        self.le_weight_cut.setText(str(self.cut.weight()))
        self.cut.take_pack_sql()
        self.set_pack()
        self.cut.take_material_price()
        self.set_width_all()
        self.cut.set_material_id_old(self.cut.material_id())


class CutListMission(QMainWindow, cut_list_mission_class):
    def __init__(self):
        super(CutListMission, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.set_start_settings()
        self.get_start_sql_info()

    def set_start_settings(self):
        self.tw_cut_mission_list.horizontalHeader().resizeSection(0, 50)
        self.tw_cut_mission_list.horizontalHeader().resizeSection(1, 150)
        self.tw_cut_mission_list.horizontalHeader().resizeSection(2, 100)
        self.tw_cut_mission_list.horizontalHeader().resizeSection(3, 80)
        self.tw_cut_mission_list.horizontalHeader().resizeSection(4, 90)
        self.tw_cut_mission_list.horizontalHeader().resizeSection(5, 90)

    def get_start_sql_info(self):
        query = """SELECT cut_m.Id, cut_m.Name, DATE_FORMAT(cut_m.Date_Shipment, '%d.%m.%Y'), count(*),
                      SUM(cut_p.Value) AS all_value, SUM(cut_p.Value_Complete) AS com_value,
                      CASE SUM(cut_p.Value_Complete)
                        WHEN SUM(cut_p.Value) THEN '#66FFCC'
                        WHEN 0 THEN '#FFFFFF'
                        ELSE '#FFFF99'
                      END AS color
                    FROM cut_mission AS cut_m
                      LEFT JOIN cut_mission_position AS cut_p
                        ON cut_m.Id = cut_p.Cut_Mission_Id
                    GROUP BY cut_m.Id"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение таблицы закройных листов", sql_info.msg, QMessageBox.Ok)
            return False
        self.set_start_table_info(sql_info)

    def set_start_table_info(self, sql_table_info):
        self.tw_cut_mission_list.clearContents()
        for row in range(len(sql_table_info)):
            self.tw_cut_mission_list.insertRow(row)
            for col in range(len(sql_table_info[row]) - 1):
                table_item = QTableWidgetItem(str(sql_table_info[row][col]))
                table_item.setData(-2, sql_table_info[row][0])
                table_item.setBackground(QBrush(QColor(sql_table_info[row][6])))
                self.tw_cut_mission_list.setItem(row, col, table_item)

    def ui_new_cut_mission(self):
        self.new_cut_mission = NewCutMission()
        self.new_cut_mission.setModal(True)
        self.new_cut_mission.show()

    def ui_double_click_cut_mission(self, row):
        id = self.tw_cut_mission_list.item(row, 0).data(-2)
        self.edit_cut_mission = EditCutMission(self, id)
        self.edit_cut_mission.setModal(True)
        self.edit_cut_mission.show()


class NewCutMission(QDialog, new_cut_mission_class):
    def __init__(self):
        super(NewCutMission, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()
        self.set_order_sql()

    def set_start_settings(self):
        self.tw_order.horizontalHeader().resizeSection(0, 120)
        self.tw_order.horizontalHeader().resizeSection(1, 240)
        self.tw_order.horizontalHeader().resizeSection(2, 80)
        self.tw_order.horizontalHeader().resizeSection(3, 80)
        self.tw_order.horizontalHeader().resizeSection(4, 60)
        self.tw_order.horizontalHeader().resizeSection(5, 200)

        self.tw_position_list.horizontalHeader().resizeSection(0, 60)
        self.tw_position_list.horizontalHeader().resizeSection(1, 60)
        self.tw_position_list.horizontalHeader().resizeSection(2, 80)
        self.tw_position_list.horizontalHeader().resizeSection(3, 60)
        self.tw_position_list.horizontalHeader().resizeSection(4, 60)
        self.tw_position_list.horizontalHeader().resizeSection(5, 60)
        self.tw_position_list.horizontalHeader().resizeSection(6, 150)
        self.tw_position_list.horizontalHeader().resizeSection(7, 70)

        self.tw_position_list_complete.horizontalHeader().resizeSection(0, 60)
        self.tw_position_list_complete.horizontalHeader().resizeSection(1, 60)
        self.tw_position_list_complete.horizontalHeader().resizeSection(2, 80)
        self.tw_position_list_complete.horizontalHeader().resizeSection(3, 60)
        self.tw_position_list_complete.horizontalHeader().resizeSection(4, 150)

    def set_order_sql(self):
        query = """SELECT `order`.Id, clients.Name, clients_actual_address.Name, DATE_FORMAT(`order`.Date_Order, '%d.%m.%Y'),
                   DATE_FORMAT(`order`.Date_Shipment, '%d.%m.%Y'), `order`.Number_Doc, `order`.Note FROM `order` LEFT JOIN clients ON `order`.Client_Id = clients.Id
                    LEFT JOIN clients_actual_address ON `order`.Clients_Adress_Id = clients_actual_address.Id
                    LEFT JOIN order_position ON `order`.Id = order_position.Order_Id
                    WHERE `order`.Cut_Mission_Id = -1 GROUP BY `order`.Id ORDER BY `order`.Date_Order DESC"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение таблицы заказов", sql_info.msg, QMessageBox.Ok)
            return False

        for order in sql_info:
            row = self.tw_order.rowCount()
            self.tw_order.insertRow(row)
            for col in range(1, len(order)):
                table_item = QTableWidgetItem(str(order[col]))
                table_item.setData(-2, order[0])
                if col == 1:
                    table_item.setCheckState(Qt.Unchecked)
                self.tw_order.setItem(row, col - 1, table_item)

    def ui_order_select_comlete(self):
        self.check_id = []
        for row in range(self.tw_order.rowCount()):
            table_item = self.tw_order.item(row, 0)
            if table_item.checkState() == Qt.Checked:
                self.check_id.append(table_item.data(-2))

        if not self.check_id:
            QMessageBox.information(self, "Выберите позицию", "Вам нужно выбрать хотя бы один заказ", QMessageBox.Ok)
            return False

        str_id_list = str(self.check_id)
        str_id_list = str_id_list.replace("[", "(")
        str_id_list = str_id_list.replace("]", ")")

        query = """SELECT material_name.Name, material_name.Id, product_article.Article, product_article.Id,
                      product_article_size.Size, product_article_size.Id, product_article_parametrs.Name, product_article_parametrs.Id,
                      COUNT(*), SUM(order_position.Value)
                    FROM `order` LEFT JOIN order_position
                      ON `order`.Id = order_position.Order_Id
                    LEFT JOIN product_article_parametrs
                      ON order_position.Product_Article_Parametr_Id = product_article_parametrs.Id
                    LEFT JOIN product_article_size
                      ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                    LEFT JOIN product_article
                      ON product_article_size.Article_Id = product_article.Id
                    LEFT JOIN product_article_material
                      ON product_article_parametrs.Id = product_article_material.Product_Article_Parametrs_Id AND Material_Id IS NOT NULL
                    LEFT JOIN material_name
                      ON product_article_material.Material_Id = material_name.Id
                    WHERE Order_Id IN %s GROUP BY material_name.Name, product_article_parametrs.Id"""
        sql_info = my_sql.sql_select(query % str_id_list)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение общего колличество заказаных трусов", sql_info.msg, QMessageBox.Ok)
            return False

        material_name = "None Material"
        row = 0
        for sql_position in sql_info:
            if sql_position[0] != material_name:
                self.tw_position_list.insertRow(row)
                self.tw_position_list.setSpan(row, 0, 1, 7)
                new_table_item = QTableWidgetItem(sql_position[0])
                new_table_item.setData(-2, sql_position[1])
                new_table_item.setFont(QFont("Tahoma", 10, QFont.Bold))
                new_table_item.setTextAlignment(Qt.AlignJustify)
                new_table_item.setTextAlignment(Qt.AlignHCenter)
                self.tw_position_list.setItem(row, 0, new_table_item)
                material_name = sql_position[0]
                row += 1

            self.tw_position_list.insertRow(row)

            new_table_item = QTableWidgetItem(sql_position[2])
            new_table_item.setData(-2, sql_position[3])
            new_table_item.setFlags(Qt.ItemIsEnabled)
            self.tw_position_list.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(sql_position[4])
            new_table_item.setData(-2, sql_position[5])
            new_table_item.setFlags(Qt.ItemIsEnabled)
            self.tw_position_list.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(sql_position[6])
            new_table_item.setData(-2, sql_position[7])
            new_table_item.setFlags(Qt.ItemIsEnabled)
            self.tw_position_list.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(sql_position[8]))
            new_table_item.setFlags(Qt.ItemIsEnabled)
            self.tw_position_list.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d))', ' ', str(sql_position[9])))
            new_table_item.setFlags(Qt.ItemIsEnabled)
            self.tw_position_list.setItem(row, 4, new_table_item)

            new_table_item = QTableWidgetItem(re.sub(r'(?<=\d)(?=(\d\d\d))', ' ', str(sql_position[9])))
            self.tw_position_list.setItem(row, 5, new_table_item)

            new_table_item = QTableWidgetItem(str(sql_position[0]))
            new_table_item.setFlags(Qt.ItemIsEnabled)
            new_table_item.setData(-2, sql_position[1])
            self.tw_position_list.setItem(row, 6, new_table_item)

            butt = QPushButton("Изм. ткань")
            butt.setProperty("row", row)
            butt.clicked.connect(self.check_material_name)
            self.tw_position_list.setCellWidget(row, 7, butt)

            row += 1

        self.sw_new.setCurrentIndex(1)

    def ui_position_complete(self):
        all_position = []
        for row in range(self.tw_position_list.rowCount()):
            if self.tw_position_list.item(row, 1) is not None:
                tuple_position = ((self.tw_position_list.item(row, 0).text(), self.tw_position_list.item(row, 0).data(-2)),
                                  (self.tw_position_list.item(row, 1).text(), self.tw_position_list.item(row, 1).data(-2)),
                                  (self.tw_position_list.item(row, 2).text(), self.tw_position_list.item(row, 2).data(-2)),
                                  (self.tw_position_list.item(row, 5).text(), self.tw_position_list.item(row, 5).text()),
                                  (self.tw_position_list.item(row, 6).text(), self.tw_position_list.item(row, 6).data(-2)))
                all_position.append(tuple_position)

        all_position.sort(key=lambda x: x[4][1])

        row = 0
        material_name = "None Material"
        for tuple_position_cut in all_position:
            if tuple_position_cut[4][0] != material_name:
                self.tw_position_list_complete.insertRow(row)
                self.tw_position_list_complete.setSpan(row, 0, 1, 5)
                new_table_item = QTableWidgetItem(str(tuple_position_cut[4][0]))
                new_table_item.setData(-2, tuple_position_cut[4][1])
                new_table_item.setFont(QFont("Tahoma", 10, QFont.Bold))
                new_table_item.setTextAlignment(Qt.AlignJustify)
                new_table_item.setTextAlignment(Qt.AlignHCenter)
                self.tw_position_list_complete.setItem(row, 0, new_table_item)
                material_name = tuple_position_cut[4][0]
                row += 1
            col = 0
            self.tw_position_list_complete.insertRow(row)
            for item_position in tuple_position_cut:
                new_table_item = QTableWidgetItem(item_position[0])
                new_table_item.setData(-2, item_position[1])
                self.tw_position_list_complete.setItem(row, col, new_table_item)
                col += 1
            row += 1

        date_shipment = 0
        for row in range(self.tw_order.rowCount()):
            table_item = self.tw_order.item(row, 0)
            if table_item.checkState() == Qt.Checked:
                date_shipment = datetime.strptime(self.tw_order.item(row, 3).text(), "%d.%m.%Y")
        self.de_date.setDate(date_shipment)

        self.sw_new.setCurrentIndex(2)

    def ui_complete(self):
        cut_name = self.le_name.text()
        if cut_name == "":
            self.le_name.setStyleSheet("border: 2px solid red;")
            return False
        else:
            self.le_name.setStyleSheet("")

        date_shipment = self.de_date.date().toString(Qt.ISODate)

        query = """INSERT INTO cut_mission (Name, Data_Create, Date_Shipment) VALUES (%s, CURDATE(), %s)"""
        sql_id_cut_mission = my_sql.sql_change(query, (cut_name, date_shipment))
        if "mysql.connector.errors" in str(type(sql_id_cut_mission)):
            QMessageBox.critical(self, "Ошибка sql запись кроя", sql_id_cut_mission.msg, QMessageBox.Ok)
            return False

        all_position = []
        for row in range(self.tw_position_list_complete.rowCount()):
            if self.tw_position_list_complete.item(row, 1) is not None:
                tuple_position = (
                int(sql_id_cut_mission), self.tw_position_list_complete.item(row, 2).data(-2), self.tw_position_list_complete.item(row, 4).data(-2),
                int(self.tw_position_list_complete.item(row, 3).text().replace(" ", "")), 0)
                all_position.append(tuple_position)

        query = """INSERT INTO cut_mission_position (Cut_Mission_Id, Article_Parametr_Id, Material_Id, Value, Value_Complete) VALUES (%s, %s, %s, %s, %s)"""
        sql_info = my_sql.sql_many(query, all_position)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql запись позиций", sql_info.msg, QMessageBox.Ok)
            return False

        query = """UPDATE `order` SET Cut_Mission_Id = %s WHERE Id IN %s"""
        str_id_list = str(self.check_id)
        str_id_list = str_id_list.replace("[", "(")
        str_id_list = str_id_list.replace("]", ")")
        sql_info = my_sql.sql_change(query % (int(sql_id_cut_mission), str_id_list))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql изменеия id листа в заказах", sql_info.msg, QMessageBox.Ok)
            return False

        self.close()
        self.destroy()

    def check_material_name(self):
        butt = QObject.sender(self)
        self.row_change_material = butt.property("row")
        self.material = MaterialName(self, True)
        self.material.setWindowModality(Qt.ApplicationModal)
        self.material.show()

    def of_list_material_name(self, material):
        table_item = QTableWidgetItem(material[1])
        table_item.setData(-2, material[0])
        self.tw_position_list.setItem(self.row_change_material, 6, table_item)


class EditCutMission(QDialog, edit_cut_mission_class):
    def __init__(self, main, id):
        super(EditCutMission, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.main = main
        self.id = id
        self.set_start_settings()
        self.get_start_sql_info()
        self.set_start_table_info()

    def set_start_settings(self):
        self.tw_order.horizontalHeader().resizeSection(0, 100)
        self.tw_order.horizontalHeader().resizeSection(1, 220)
        self.tw_order.horizontalHeader().resizeSection(2, 90)
        self.tw_order.horizontalHeader().resizeSection(3, 90)
        self.tw_order.horizontalHeader().resizeSection(4, 50)
        self.tw_order.horizontalHeader().resizeSection(5, 150)

        self.tw_cut_position.horizontalHeader().resizeSection(0, 70)
        self.tw_cut_position.horizontalHeader().resizeSection(1, 50)
        self.tw_cut_position.horizontalHeader().resizeSection(2, 90)
        self.tw_cut_position.horizontalHeader().resizeSection(3, 80)
        self.tw_cut_position.horizontalHeader().resizeSection(4, 80)
        self.tw_cut_position.horizontalHeader().resizeSection(5, 180)

        self.save_change_main_cut_sql = False
        self.save_change_position_cut_sql = []

    def get_start_sql_info(self):
        query = """SELECT cut_mission.Name, cut_mission.Date_Shipment FROM cut_mission WHERE Id = %s"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение информации о крой личте", sql_info.msg, QMessageBox.Ok)
            return False
        self.cut_info = sql_info

        query = """SELECT `order`.Id, clients.Name, clients_actual_address.Adres, `order`.Date_Order, `order`.Date_Shipment, `order`.Number_Doc, `order`.Note
                    FROM cut_mission
                      LEFT JOIN `order` ON cut_mission.Id = `order`.Cut_Mission_Id
                      LEFT JOIN clients ON `order`.Client_Id = clients.Id
                      LEFT JOIN clients_actual_address ON `order`.Clients_Adress_Id = clients_actual_address.Id
                    WHERE cut_mission.Id = %s"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение таблицы заказов", sql_info.msg, QMessageBox.Ok)
            return False
        self.order_sql = sql_info

        query = """SELECT cut_p.Id, art.Article, art_size.Size, art_par.Name, art_par.Id, cut_p.Value, cut_p.Value_Complete, material.Name, material.Id,
                      CASE cut_p.Value_Complete
                        WHEN cut_p.Value THEN '#66FFCC'
                        WHEN 0 THEN '#FFFFFF'
                        ELSE '#FFFF99'
                      END AS color
                    FROM cut_mission AS cut_m
                      LEFT JOIN cut_mission_position AS cut_p ON cut_m.Id = cut_p.Cut_Mission_Id
                      LEFT JOIN product_article_parametrs AS art_par ON cut_p.Article_Parametr_Id = art_par.Id
                      LEFT JOIN product_article_size AS art_size ON art_par.Product_Article_Size_Id = art_size.Id
                      LEFT JOIN product_article AS art ON art_size.Article_Id = art.Id
                      LEFT JOIN material_name AS material ON cut_p.Material_Id = material.Id
                    WHERE cut_m.Id = %s"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение списка позиций для крой листа", sql_info.msg, QMessageBox.Ok)
            return False
        self.cut_position = sql_info

    def set_start_table_info(self, who_set="all"):

        if who_set == "all" or who_set == "main":
            self.le_name.setText(self.cut_info[0][0])
            self.de_date_shipment.setDate(self.cut_info[0][1])

        if who_set == "all" or who_set == "order":
            self.tw_order.clearContents()
            self.tw_order.setRowCount(0)
            for order in self.order_sql:
                row = self.tw_order.rowCount()
                self.tw_order.insertRow(row)
                for col in range(1, len(order)):
                    table_item = QTableWidgetItem(str(order[col]))
                    table_item.setData(-2, order[0])
                    self.tw_order.setItem(row, col - 1, table_item)

        if who_set == "all" or who_set == "position":
            self.tw_cut_position.clearContents()
            self.tw_cut_position.setRowCount(0)
            for cut_position in self.cut_position:
                row = self.tw_cut_position.rowCount()
                self.tw_cut_position.insertRow(row)

                table_item = QTableWidgetItem(str(cut_position[1]))
                table_item.setData(-1, "set")
                table_item.setData(5, cut_position[0])
                table_item.setBackground(QBrush(QColor(cut_position[9])))
                table_item.setFlags(Qt.ItemIsEnabled)
                self.tw_cut_position.setItem(row, 0, table_item)

                table_item = QTableWidgetItem(str(cut_position[2]))
                table_item.setData(-1, "set")
                table_item.setData(5, cut_position[0])
                table_item.setBackground(QBrush(QColor(cut_position[9])))
                table_item.setFlags(Qt.ItemIsEnabled)
                self.tw_cut_position.setItem(row, 1, table_item)

                table_item = QTableWidgetItem(str(cut_position[3]))
                table_item.setData(-1, "set")
                table_item.setData(5, cut_position[0])
                table_item.setData(-2, cut_position[4])
                table_item.setBackground(QBrush(QColor(cut_position[9])))
                table_item.setFlags(Qt.ItemIsEnabled)
                self.tw_cut_position.setItem(row, 2, table_item)

                table_item = QTableWidgetItem(str(cut_position[5]))
                table_item.setData(-1, "set")
                table_item.setData(5, cut_position[0])
                table_item.setBackground(QBrush(QColor(cut_position[9])))
                self.tw_cut_position.setItem(row, 3, table_item)

                table_item = QTableWidgetItem(str(cut_position[6]))
                table_item.setData(-1, "set")
                table_item.setData(5, cut_position[0])
                table_item.setBackground(QBrush(QColor(cut_position[9])))
                table_item.setFlags(Qt.ItemIsEnabled)
                self.tw_cut_position.setItem(row, 4, table_item)

                table_item = QTableWidgetItem(str(cut_position[7]))
                table_item.setData(-1, "set")
                table_item.setData(5, cut_position[0])
                table_item.setData(-2, cut_position[8])
                table_item.setBackground(QBrush(QColor(cut_position[9])))
                table_item.setFlags(Qt.ItemIsEnabled)
                self.tw_cut_position.setItem(row, 5, table_item)

                butt = QPushButton("Изм. ткань")
                butt.setProperty("row", row)
                butt.clicked.connect(self.check_material_name)
                self.tw_cut_position.setCellWidget(row, 6, butt)

    def check_material_name(self):
        butt = QObject.sender(self)
        self.row_change_material = butt.property("row")
        self.material = MaterialName(self, True)
        self.material.setWindowModality(Qt.ApplicationModal)
        self.material.show()

    def ui_save_trigger_cut_mission(self):
        if not self.save_change_main_cut_sql:
            self.save_change_main_cut_sql = True

    def ui_save_trigger_cut_mission_position(self, row, column):
        if column == 3:
            self.tw_cut_position.item(row, column).setData(-1, "upd")
            if self.tw_cut_position.item(row, column).data(5) not in self.save_change_position_cut_sql:
                self.save_change_position_cut_sql.append(self.tw_cut_position.item(row, column).data(5))

    def ui_select_order(self, order_item):
        self.order = order.Order(self, order_item.data(-2))
        self.order.start_set_sql_info()
        self.order.setWindowModality(Qt.ApplicationModal)
        self.order.show()

    def ui_acc(self):
        self.save_sql()
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()

    def save_sql(self):
        if self.save_change_main_cut_sql:
            query = "UPDATE cut_mission SET Name = %s, Date_Shipment = %s WHERE Id = %s"
            sql_info = my_sql.sql_change(query, (self.le_name.text(), self.de_date_shipment.date().toString(Qt.ISODate),  self.id))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql запись основной информации крой листа", sql_info.msg, QMessageBox.Ok)
                return False

        if self.save_change_position_cut_sql:
            for row in range(self.tw_cut_position.rowCount()):
                if self.tw_cut_position.item(row, 0).data(5) in self.save_change_position_cut_sql:
                    value = int(self.tw_cut_position.item(row, 3).text())
                    complete_value = int(self.tw_cut_position.item(row, 4).text())
                    if complete_value > value:
                        complete_value = value
                    query = "UPDATE cut_mission_position SET Value = %s, Value_Complete = %s, Material_Id = %s WHERE Id = %s"
                    sql_info = my_sql.sql_change(query, (value, complete_value, self.tw_cut_position.item(row, 5).data(-2),  self.tw_cut_position.item(row, 0).data(5)))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql запись строки крой листа", sql_info.msg, QMessageBox.Ok)
                        return False

    def of_list_material_name(self, material):
        table_item = QTableWidgetItem(material[1])
        table_item.setData(-2, material[0])
        table_item.setData(5, self.tw_cut_position.item(self.row_change_material, 5).data(5))
        table_item.setData(-1, "upd")
        self.tw_cut_position.setItem(self.row_change_material, 5, table_item)
        if self.tw_cut_position.item(self.row_change_material, 5).data(5) not in self.save_change_position_cut_sql:
                self.save_change_position_cut_sql.append(self.tw_cut_position.item(self.row_change_material, 5).data(5))

    def of_order_complete(self):
        self.get_start_sql_info()
        self.set_start_table_info("order")
