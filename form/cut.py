from os import getcwd
from form import order, staff, print_label
from datetime import datetime, date
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QPushButton, QLineEdit, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt, QDate, QObject
from form.supply_material import MaterialName
from form.pack import PackBrows
import re
from function import my_sql, barcode, files, table_to_html
from classes import cut, print_qt
from classes.my_class import User
from form.templates import table
import codecs
from decimal import Decimal

cut_brows_class = loadUiType(getcwd() + '/ui/cut_brows.ui')[0]
cut_filter = loadUiType(getcwd() + '/ui/cut_filter.ui')[0]

cut_list_mission_class = loadUiType(getcwd() + '/ui/cut_list_mission.ui')[0]
new_cut_mission_class = loadUiType(getcwd() + '/ui/cut_new_mission.ui')[0]
edit_cut_mission_class = loadUiType(getcwd() + '/ui/cut_edit_mission.ui')[0]
cut_print_passport = loadUiType(getcwd() + '/ui/cut_print_passport.ui')[0]


class CutList(table.TableList):
    def set_settings(self):

        self.setWindowTitle("Кроя")  # Имя окна
        self.resize(900, 270)
        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.toolBar.setStyleSheet("background-color: rgb(63, 173, 191);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("№", 35), ("Дата кроя", 70), ("Вес пачек", 80), ("Вес обрези", 80), ("Вес итого", 80), ("Пачек", 55),
                                  ("Раскладчик", 100), ("ткань", 120), ("Заметка", 200))

        # Быстрый фильтр
        self.le_fast_filter = QLineEdit()
        self.le_fast_filter.setPlaceholderText("Номер кроя")
        self.le_fast_filter.setMaximumWidth(150)
        self.le_fast_filter.editingFinished.connect(self.fast_filter)
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(dummy)
        self.toolBar.addWidget(self.le_fast_filter)

        self.filter = None
        self.query_table_all = """SELECT cut.Id, cut.Print_passport, cut.Id, cut.Date_Cut, SUM(pack.Weight), cut.Weight_Rest, SUM(pack.Weight) + cut.Weight_Rest,
                                        COUNT(pack.Id), staff_worker_info.Last_Name, material_name.Name, cut.Note
                                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                                      LEFT JOIN staff_worker_info ON cut.Worker_Id = staff_worker_info.Id
                                      LEFT JOIN material_name ON cut.Material_Id = material_name.Id
                                      GROUP BY cut.Id
                                      ORDER BY cut.Id DESC"""

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT cut.Id, cut.Print_passport, cut.Id, cut.Date_Cut, SUM(pack.Weight), cut.Weight_Rest, SUM(pack.Weight) + cut.Weight_Rest,
                                        COUNT(pack.Id), staff_worker_info.Last_Name, material_name.Name, cut.Note
                                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                                      LEFT JOIN staff_worker_info ON cut.Worker_Id = staff_worker_info.Id
                                      LEFT JOIN material_name ON cut.Material_Id = material_name.Id
                                      GROUP BY cut.Id
                                      ORDER BY cut.Id DESC"""

        self.query_table_dell = "DELETE FROM cut WHERE Id = %s"

    def ui_add_table_item(self):  # Добавить предмет
        self.cut_window = CutBrows(self)
        self.cut_window.setModal(True)
        self.cut_window.show()

    def ui_change_table_item(self, id=False):  # изменить элемент
        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
                return False

        self.cut_window = CutBrows(self, item_id)
        self.cut_window.setModal(True)
        self.cut_window.show()

    def ui_filter(self):
        if self.filter is None:
            self.filter = CutFilter(self)
        self.filter.of_set_sql_query(self.query_table_all)
        self.filter.setWindowModality(Qt.ApplicationModal)
        self.filter.show()

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

            if table_typle[1] == 1:
                color = QBrush(QColor(62, 240, 130, 255))
            else:
                color = QBrush(QColor(228, 242, 99, 255))

            for column in range(2, len(table_typle)):
                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(table_typle[column]))
                elif isinstance(table_typle[column], date):
                    text = table_typle[column].strftime("%d.%m.%Y")
                else:
                    text = str(table_typle[column])
                item = QTableWidgetItem(text)
                item.setData(5, table_typle[0])
                item.setBackground(color)
                self.table_widget.setItem(self.table_widget.rowCount() - 1, column - 2, item)

    def fast_filter(self):
        # Блок условий номер кроя
        if self.le_fast_filter.text() != '':
            q_filter = " WHERE (cut.Id = %s)" % self.le_fast_filter.text()
            self.query_table_select = self.query_table_all.replace("GROUP BY", q_filter + " GROUP BY")
        else:
            self.query_table_select = self.query_table_all

        self.ui_update()

    def of_set_filter(self, sql):
        self.query_table_select = sql
        self.ui_update()

    def of_change_cut_complete(self):
        self.ui_update()


class CutBrows(QDialog, cut_brows_class):
    def __init__(self, main=None, cut_id=None):
        super(CutBrows, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.access_save_sql = True
        self.insert_values_sql = False
        self.cut = cut.Cut(cut_id)
        self.main = main

        self.set_start_info()
        self.set_size_table()
        self.access()

    def access(self):
        for item in User().access_list(self.__class__.__name__):
            a = getattr(self, item["atr1"])
            if item["atr2"]:
                a = getattr(a, item["atr2"])

            if item["value"]:
                if item["value"] == "True":
                    val = True
                elif item["value"] == "False":
                    val = False
                else:
                    val = item["value"]
                a(val)
            else:
                a()

    def access_save(self, bool):
        self.access_save_sql = bool

    def set_start_info(self):
        if self.cut.number() is None:
            self.le_number_cut.setText(str(self.cut.take_new_number()))
            self.de_cut_date.setDate(QDate.currentDate())
            self.cut.set_date(self.de_cut_date.date())
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
            self.cb_print.setChecked(self.cut.print_passport())

            self.cut.take_pack_sql()
            self.set_pack()

            self.insert_values_sql = False

    def set_size_table(self):
        self.tw_pack.horizontalHeader().resizeSection(0, 25)
        self.tw_pack.horizontalHeader().resizeSection(1, 65)
        self.tw_pack.horizontalHeader().resizeSection(2, 35)
        self.tw_pack.horizontalHeader().resizeSection(3, 145)
        self.tw_pack.horizontalHeader().resizeSection(4, 85)
        self.tw_pack.horizontalHeader().resizeSection(5, 35)
        self.tw_pack.horizontalHeader().resizeSection(6, 35)
        self.tw_pack.horizontalHeader().resizeSection(7, 55)
        self.tw_pack.horizontalHeader().resizeSection(8, 65)
        self.tw_pack.horizontalHeader().resizeSection(9, 65)
        self.tw_pack.horizontalHeader().resizeSection(10, 165)

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

    def ui_edit_print(self, bol):
        if not self.insert_values_sql:
            self.cut.set_print_passport(bol)

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

    def ui_print_passport(self):
        self.cut_passport = CutPassport(self, self.cut)
        self.cut_passport.setModal(True)
        self.cut_passport.show()

    def ui_print_cut(self):
        head = "Крой №%s" % self.cut.id()

        up_html = """
          <table>
          <caption>#caption#</caption>
          <tr>
          <th>Крой</th><th>Дата кроя</th><th>Вид ткани</th><th>Цена ткани</th><th>Раскладчик</th>
          </tr>
          <tr>
          <td>#id_cut#</td><td>#cut_date#</td><td>#cut_material#</td><td>#material_price#</td><td>#worker#</td>
          </tr>
          </table>
          <table>
          <tr>
          <th>Вес пачек</th><th>Вес обрези</th><th>Вес итого</th><th>% обрези</th><th>Заметка</th>
          </tr>
          <tr>
          <td>#weight_pack#</td><td>#weight_rest#</td><td>#weight_all#</td><td>#percent_rest#</td><td>#note#</td>
          </tr>
          </table>
          """

        up_html = up_html.replace("#caption#", head)
        up_html = up_html.replace("#id_cut#", str(self.cut.id()))
        up_html = up_html.replace("#cut_date#", str(self.cut.date().strftime("%d.%m.%Y")))
        up_html = up_html.replace("#cut_material#", str(self.cut.material_name()))
        up_html = up_html.replace("#material_price#", str(self.cut.material_price()))
        up_html = up_html.replace("#worker#", str(self.cut.worker_name()))

        up_html = up_html.replace("#weight_pack#", str(self.cut.weight()))
        up_html = up_html.replace("#weight_rest#", str(self.cut.weight_rest()))
        up_html = up_html.replace("#weight_all#", str(self.cut.weight_all()))
        up_html = up_html.replace("#percent_rest#", str(self.cut.percent_rest()))
        up_html = up_html.replace("#note#", str(self.cut.note()))

        html = table_to_html.tab_html(self.tw_pack, up_template=up_html)
        self.print_class = print_qt.PrintHtml(self, html)

    def ui_print_label(self):
        self.label_list = LabelList(self, self.cut)
        self.label_list.setModal(True)
        self.label_list.show()

    def ui_fast_filter(self):
        if self.le_pack_number_filter.text():
            try:
                filter_pack = int(self.le_pack_number_filter.text())
            except:
                return False

            self.tw_pack.clearContents()
            self.tw_pack.setRowCount(0)

            if not self.cut.pack_list():
                return False
            pack_list = self.cut.pack_list()
            row = 0

            for pack_id, pack in pack_list.items():
                if pack.number_pack() == filter_pack:
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
                    break

        else:
            self.set_pack()

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
        if self.cut.need_save() and self.access_save_sql:
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
        while need_set_pack > 0:
            for pack_id, pack in pack_list.items():

                if pack.number_pack() == pack_number_table:
                    self.tw_pack.insertRow(row)

                    if pack.print_label():
                        color = QBrush(QColor(62, 240, 130, 255))
                    else:
                        color = QBrush(QColor(228, 242, 99, 255))

                    new_table_item = QTableWidgetItem(str(pack.number_pack()))
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 0, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.article()))
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 1, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.size()))
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 2, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.parametr_name()))
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 3, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.client_name()))
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 4, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.value()))
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 5, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.value_damage()))
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 6, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.weight()))
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 7, new_table_item)

                    date_make = pack.date_make().strftime("%d.%m.%Y") if pack.date_make() is not None else ""
                    new_table_item = QTableWidgetItem(date_make)
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 8, new_table_item)

                    date_complete = pack.date_complete().strftime("%d.%m.%Y") if pack.date_complete() is not None else ""
                    new_table_item = QTableWidgetItem(date_complete)
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 9, new_table_item)

                    new_table_item = QTableWidgetItem(pack.article_client_name())
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setBackground(color)
                    self.tw_pack.setItem(row, 10, new_table_item)

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


class CutFilter(QDialog, cut_filter):
    def __init__(self, main):
        super(CutFilter, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main

    def ui_view_material(self):
        self.material_name = MaterialName(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_view_worker(self):
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_del_material(self):
        self.le_material.setWhatsThis("")
        self.le_material.setText("")

    def ui_del_worker(self):
        self.le_work.setWhatsThis("")
        self.le_work.setText("")

    def ui_acc(self):
        where = ""

        # Блок условий номер кроя
        if self.le_number_cut.text() != '':
            where = self.add_filter(where, "(cut.Id = %s)" % self.le_number_cut.text())

        # Блок  условий выбора ткани
        if self.le_material.whatsThis() != '':
            where = self.add_filter(where, "(cut.Material_Id = %s)" % self.le_material.whatsThis())

        # Блок  условий выбора закройщика
        if self.le_work.whatsThis() != '':
            where = self.add_filter(where, "(cut.Worker_Id = %s)" % self.le_work.whatsThis())

        # Блок  условий даты коря
        if self.gb_date_cut.isChecked():
            sql_date = "(cut.Date_Cut >= '%s' AND cut.Date_Cut <= '%s')" % \
                       (self.de_date_cut_from.date().toString(Qt.ISODate), self.de_date_cut_to.date().toString(Qt.ISODate))
            where = self.add_filter(where, sql_date)

        # Делаем замену так как Were должно быть перед Group by
        if where:
            self.sql_query_all = self.sql_query_all.replace("GROUP BY", " WHERE " + where + " GROUP BY")

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

    def of_list_material_name(self, item):
        self.le_material.setWhatsThis(str(item[0]))
        self.le_material.setText(item[1])

    def of_list_worker(self, item):
        self.le_work.setWhatsThis(str(item[0]))
        self.le_work.setText(item[1])


class CutPassport(QDialog, cut_print_passport):
    def __init__(self, main, cut):
        super(CutPassport, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        self.cut = cut

        self.set_size_table()
        self.set_pack()

    def set_size_table(self):
        self.tw_pack.horizontalHeader().resizeSection(0, 20)
        self.tw_pack.horizontalHeader().resizeSection(1, 35)
        self.tw_pack.horizontalHeader().resizeSection(2, 65)
        self.tw_pack.horizontalHeader().resizeSection(3, 55)
        self.tw_pack.horizontalHeader().resizeSection(4, 200)

    def set_pack(self):
        self.tw_pack.clearContents()
        self.tw_pack.setRowCount(0)

        if not self.cut.pack_list():
            return False

        need_set_pack = len(self.cut.pack_list())
        pack_number_table = 1

        pack_list = self.cut.pack_list()
        row = 0

        while need_set_pack > 0:
            for pack_id, pack in pack_list.items():

                if pack.number_pack() == pack_number_table:
                    self.tw_pack.insertRow(row)

                    new_table_item = QTableWidgetItem()
                    new_table_item.setData(-2, pack_id)
                    new_table_item.setCheckState(Qt.Unchecked)
                    self.tw_pack.setItem(row, 0, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.number_pack()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 1, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.article()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 2, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.size()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 3, new_table_item)

                    new_table_item = QTableWidgetItem(str(pack.parametr_name()))
                    new_table_item.setData(-2, pack_id)
                    self.tw_pack.setItem(row, 4, new_table_item)

                    row += 1
                    pack_number_table += 1
                    need_set_pack -= 1
                    break
            else:
                pack_number_table += 1

    def ui_check_all(self):
        for row in range(self.tw_pack.rowCount()):
            self.tw_pack.item(row, 0).setCheckState(Qt.Checked)

    def ui_uncheck_all(self):
        for row in range(self.tw_pack.rowCount()):
            self.tw_pack.item(row, 0).setCheckState(Qt.Unchecked)

    def ui_acc(self):
        select_pack = []
        for row in range(self.tw_pack.rowCount()):
            if self.tw_pack.item(row, 0).checkState() == Qt.Checked:
                select_pack.append(self.tw_pack.item(row, 0).data(-2))

        if not select_pack:
            QMessageBox.information(self, "Ошибка", "Выберите хотя бы одну пачку", QMessageBox.Ok)
            return False

        #  Начинаем перебор выбраных пачек
        pack_html = """    <div style="display: inline-block; width: 100%">
                            <table style="height: 150px; border-color: black; margin-left: auto; margin-right: auto;" border="1" width="100%" cellspacing="0" cellpadding="0">
                            <tbody>
                            <tr>
                            <td style="height: 10px; text-align: center; vertical-align: middle;">Артикул</td>
                            <td style="width: 60px; height: 10px; text-align: center; vertical-align: middle;">Размер</td>
                            <td style="width: 60px; height: 10px; text-align: center; vertical-align: middle;">Крой</td>
                            <td style="width: 60px; height: 10px; text-align: center; vertical-align: middle;">Пачка</td>
                            <td style="width: 160px; height: 10px; text-align: center; vertical-align: middle;">ID пачки</td>
                            <td style="width: 130px; height: 10px; text-align: center; vertical-align: middle;">Дата</td>
                            </tr>
                            <tr>
                            <td style="height: 10px; font-size: 15pt; text-align: center; vertical-align: middle;"><strong>#art#</strong></td>
                            <td style="width: 60px; height: 10px; font-size: 18pt; text-align: center; vertical-align: middle;"><strong>#size#</strong></td>
                            <td style="width: 60px; height: 10px; font-size: 18pt; text-align: center; vertical-align: middle;"><strong>#cut#</strong></td>
                            <td style="width: 60px; height: 10px; font-size: 18pt; text-align: center; vertical-align: middle;"><strong>#pack#</strong></td>
                            <td style="width: 160px; height: 10px; font-size: 18pt; text-align: center; vertical-align: middle;" rowspan="3"><strong><img src="#pac_barcode_src#" alt="lorem" width="150" height="70" /></strong></td>
                            <td style="width: 130px; height: 10px; font-size: 18pt; text-align: center; vertical-align: middle;"><strong>#data#</strong></td>
                            </tr>
                            <tr>
                            <td style="height: 10px; text-align: center; vertical-align: middle;">Название</td>
                            <td style="width: 60px; height: 10px; text-align: center; vertical-align: middle;">кол-во</td>
                            <td style="width: 120px; height: 10px; text-align: center; vertical-align: middle;" colspan="2">Клиент</td>
                            <td style="width: 130px; height: 10px; text-align: center; vertical-align: middle;">Штрих код</td>
                            </tr>
                            <tr>
                            <td style="height: 10px; text-align: center; vertical-align: middle;"><strong>#art_name#</strong></td>
                            <td style="width: 60px; height: 10px; text-align: center; vertical-align: middle;"><strong>#pack_value#</strong></td>
                            <td style="width: 120px; height: 10px; text-align: center; vertical-align: middle;" colspan="2"><strong>#client#</strong></td>
                            <td style="width: 130px; height: 10px; text-align: center; vertical-align: middle;"><strong>#art_barcode#</strong></td>
                            </tr>
                            <tr>
                            <td style="height: 10px; text-align: center; vertical-align: middle;" colspan="6">Описание</td>
                            </tr>
                            <tr>
                            <td style="height: 10px; text-align: center; vertical-align: middle;" colspan="6"><strong>#note_art#</strong></td>
                            </tr>
                            <tr>
                            <td style="height: 10px; text-align: center; vertical-align: middle;" colspan="6">Примечание</td>
                            </tr>
                            <tr>
                            <td style="height: 10px; text-align: center; vertical-align: middle;" colspan="6"><strong>#note#</strong></td>
                            </tr>
                            </tbody>
                            </table>
                            <p></p>
                            <table style="height: 78px; border-color: black; margin-left: auto; margin-right: auto;" border="1" width="100%" cellspacing="0" cellpadding="0">
                            <tbody>
                            <tr>
                            <td style="width: 30px; text-align: center; vertical-align: middle;">№</td>
                            <td style="width: 500px; text-align: center; vertical-align: middle;">Операция</td>
                            <td style="width: 120px; text-align: center; vertical-align: middle;">Машинка</td>
                            <td style="width: 70px; text-align: center; vertical-align: middle;">Кол-во</td>
                            <td style="width: 150px; text-align: center; vertical-align: middle;">Фамилия</td>
                            <td style="width: 120px; text-align: center; vertical-align: middle;">Дата</td>
                            </tr>
                            #o_table#
                            </tbody>
                            </table>
                            <p style="text-align: center;">Приемка на склад ___.___._____г</p>
                            </div>"""
        row_operation_html = """<tr>
                        <td style="width: 30px; height: 30px; text-align: center; vertical-align: middle;"><strong>#o_number#</strong></td>
                        <td style="width: 500px; height: 30px; text-align: left; vertical-align: middle;"><strong>#o_name#</strong></td>
                        <td style="width: 120px; font-size: 10pt; height: 30px; text-align: center; vertical-align: middle;"><strong>#o_sw#</strong></td>
                        <td style="width: 70px; height: 30px; text-align: center; vertical-align: middle;">&nbsp;</td>
                        <td style="width: 150px; height: 30px; text-align: center; vertical-align: middle;">&nbsp;</td>
                        <td style="width: 120px; height: 30px; text-align: center; vertical-align: middle;">&nbsp;</td>
                        </tr>"""
        all_pack_html = ""
        cod = []

        for pack_id in select_pack:
            pack = self.cut.pack(pack_id)
            pack.take_operation_pack()
            cod.append(str(pack.id()).zfill(7))
            operation_table = ""

            # Перебор операций пачки
            for operation in pack.operations():
                query = "SELECT sewing_machine.Name FROM operations LEFT JOIN sewing_machine ON operations.Sewing_Machine_Id = sewing_machine.Id WHERE operations.Id = %s"
                sql_info = my_sql.sql_select(query, (operation["operation_id"],))
                if "mysql.connector.errors" in str(type(sql_info)):
                    print("Не смог получить данные пачки")
                    return False
                new_row_html = row_operation_html.replace("#o_number#", str(operation["position"]))
                new_row_html = new_row_html.replace("#o_name#", str(operation["name"]))
                new_row_html = new_row_html.replace("#o_sw#", sql_info[0][0])
                operation_table = operation_table + "\n" + new_row_html

            barcode.generate(cod[-1])
            html = pack_html
            html = html.replace("#art#", str(pack.article_name()))
            html = html.replace("#size#", str(pack.size()))
            html = html.replace("#cut#", str(pack.number_cut()))
            html = html.replace("#pack#", str(pack.number_pack()))
            html = html.replace("#data#", pack.cut_date().strftime("%d.%m.%Y"))
            html = html.replace("#pac_barcode_src#", "%s.%s" % (cod[-1], "svg"))
            html = html.replace("#art_name#", str(pack.article_product_name()))
            html = html.replace("#pack_value#", str(pack.value()))
            html = html.replace("#client#", str(pack.client_name()))
            html = html.replace("#art_barcode#", str(pack.article_barcode()))
            html = html.replace("#note_art#", str(pack.note_article()))
            html = html.replace("#note#", str(pack.note()))
            html = html.replace("#o_table#", operation_table)
            all_pack_html = all_pack_html + html + "\n"

        all_html = codecs.open(getcwd() + "/templates/pack/cut_passport.html", encoding='utf-8').read()
        all_html = all_html.replace("#o_pack#", all_pack_html)
        self.print_class = print_qt.PrintHtml(self, all_html)

        for del_cod in cod:
            files.del_temp_file(del_cod + ".svg")

        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()


class LabelList(CutPassport):
    def __init__(self, main, cut):
        CutPassport.__init__(self, main, cut)
        self.setWindowTitle("Печать бирок")

    def ui_acc(self):
        select_pack = []
        for row in range(self.tw_pack.rowCount()):
            if self.tw_pack.item(row, 0).checkState() == Qt.Checked:
                select_pack.append(self.tw_pack.item(row, 0).data(-2))

        if not select_pack:
            QMessageBox.information(self, "Ошибка", "Выберите хотя бы одну пачку", QMessageBox.Ok)
            return False

        #  Начинаем перебор выбраных пачек
        for pack_id in select_pack:
            pack = self.cut.pack(pack_id)

            data = {
                    "article": pack.article(),
                    "article_size": pack.article_size(),
                    "article_parametr": pack.parametr_name(),
                    "article_barcode": pack.article_barcode(),
                    "pack_id": pack.id(),
                    "label_value": pack.value()}

            self.print_label = print_label.LabelFile(pack.parametr_id(), "Путь корень бирки", data)
            self.print_label.setModal(True)
            self.print_label.show()
            if self.print_label.exec() < 1:
                return False


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
