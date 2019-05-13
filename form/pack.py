from os import getcwd
from form import staff, operation, order, supply_accessories
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QInputDialog, QListWidgetItem, QLineEdit, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QBrush, QColor, QRegExpValidator
from PyQt5.QtCore import Qt, QDate, QRegExp
import re
import codecs
from decimal import *
from classes import cut, print_qt
from form import clients, article, print_label, supply_material
from function import barcode, files, my_sql, str_to
from classes.my_class import User
from form.templates import table
import logging
import logging.config


class PackList(table.TableList):
    def set_settings(self):

        self.setWindowTitle("Пачки")  # Имя окна
        self.resize(900, 500)
        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.pb_add.deleteLater()
        self.pb_dell.deleteLater()
        self.toolBar.setStyleSheet("background-color: rgb(170, 0, 0);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("ID", 35), ("Крой", 60), ("Пачка", 60), ("Дата", 70), ("Артикул", 150), ("Ткань", 130), ("Штук", 60), ("Брак", 60), ("Вес", 70),
                                  ("Дата приемки", 70), ("Дата проверки", 70))

        # Быстрый фильтр
        self.le_fast_filter = QLineEdit()
        self.le_fast_filter.setPlaceholderText("id пачки")
        self.le_fast_filter.setMaximumWidth(150)
        self.le_fast_filter.editingFinished.connect(self.fast_filter)
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(dummy)
        self.toolBar.addWidget(self.le_fast_filter)

        self.filter = None
        self.query_table_all = """SELECT pack.Id, pack.Id, pack.Cut_Id, pack.Number, cut.Date_Cut,
                                        CONCAT(product_article.Article, '(', product_article_size.Size, ')[', product_article_parametrs.Name,']'), material_name.Name, pack.Value_Pieces,
                                        pack.Value_Damage, pack.Weight, pack.Date_Make, pack.Date_Coplete
                                      FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
                                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                                        LEFT JOIN material_name ON cut.Material_Id = material_name.Id LIMIT 10000"""

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT pack.Id, pack.Id, pack.Cut_Id, pack.Number, cut.Date_Cut,
                                        CONCAT(product_article.Article, '(', product_article_size.Size, ')[', product_article_parametrs.Name,']'), material_name.Name, pack.Value_Pieces,
                                        pack.Value_Damage, pack.Weight, pack.Date_Make, pack.Date_Coplete
                                      FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
                                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                                        LEFT JOIN material_name ON cut.Material_Id = material_name.Id LIMIT 10000"""

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

        self.cut_window = PackBrows(self, pack_id=item_id)
        self.cut_window.setModal(True)
        self.cut_window.show()

    def ui_filter(self):
        if self.filter is None:
            self.filter = PackFilter(self)
            self.filter.start_settings()
        self.filter.of_set_sql_query(self.query_table_all)
        self.filter.setWindowModality(Qt.ApplicationModal)
        self.filter.show()

    def fast_filter(self):
        # Блок условий id пачки
        if self.le_fast_filter.text() != '':
            q_filter = " WHERE (pack.Id = %s)" % self.le_fast_filter.text()
            self.query_table_select = self.query_table_all + " " + q_filter
        else:
            self.query_table_select = self.query_table_all

        self.ui_update()

    def of_set_filter(self, sql):
        self.query_table_select = sql
        self.ui_update()

    def of_save_pack_complete(self):
        self.ui_update()


class PackBrows(QDialog):
    def __init__(self, main=None, pack=None, pack_id=None, save_pack_weight=False):
        super(PackBrows, self).__init__()
        loadUi(getcwd() + '/ui/pack.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        if pack_id is not None:
            self.pack = cut.Pack(pack_id)
        else:
            self.pack = pack

        logging.config.fileConfig(getcwd() + '/setting/logger_conf.ini')
        self.logger = logging.getLogger("CutLog")

        self.insert_values_sql = False
        self.access_save_sql = True
        self.reminder_make = False  # Переменная которая сообщает нужно ли выкинуть предупреждение о непринятой пачке
        self.save_pack = save_pack_weight  # Переменная которая не даст сохранить пачку если она открыта не в крое

        # Прячем рвсчетную часть пачки (Открываем доступами) self.frame_calc.show()
        self.frame_calc.hide()

        self.set_start_info()
        self.set_size_table()
        self.access()

        if not save_pack_weight:  # Если пачка открыта не в крое то ее нельзя сохранять!
            self.le_weight.setEnabled(False)

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

    # Функция включает предупреждение о забытии отметки о принятии пачки
    def reminder_make_pack(self):
        self.reminder_make = True

    def set_start_info(self):
        self.le_value_product.setValidator(QRegExpValidator(QRegExp("[0-9]{0,3}"), self))

        self.le_number_pack.setText(str(self.pack.number_pack()))
        self.le_number_cut.setText(str(self.pack.number_cut()))

        if self.pack.id() is not None:
            # Пачка не новая
            self.insert_values_sql = True
            self.pb_article.setEnabled(False)

            self.pb_copy.hide()  # Скрыть кнопку копирования

            self.pack.take_accessories_pack()
            self.pack.take_operation_pack()
            self.pack.take_add_material()

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

            self.le_id_pack.setText(str(self.pack.id()))

            self.le_article.setWhatsThis(str(self.pack.article()))
            self.le_article.setText(str(self.pack.parametr_name()))

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

            self.cb_print.setChecked(self.pack.print_label_bool())

            self.set_operation_name()
            self.set_accessories_name()
            self.set_add_material()

            self.insert_values_sql = False

            self.tw_accessories_operation.setCurrentIndex(0)
            self.logger.info(u"[Крой {:04d} Пользователь {:04d}] {}".format(self.pack.number_cut() or 0, User().id(), "Открыта пачка %s" % self.pack.id()))

        else:
            # Пачка новая
            self.de_date_complete.setDate(QDate.currentDate())
            self.de_date_make.setDate(QDate.currentDate())
            self.tw_accessories_operation.setCurrentIndex(1)

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

        self.tw_add_material.horizontalHeader().resizeSection(0, 230)
        self.tw_add_material.horizontalHeader().resizeSection(1, 75)
        self.tw_add_material.horizontalHeader().resizeSection(2, 75)
        self.tw_add_material.horizontalHeader().resizeSection(3, 75)

    def ui_edit_date_complete(self):
        if not self.insert_values_sql:
            self.logger.info(u"[Крой {:04d} Пользователь {:04d}] {}".format(self.pack.number_cut() or 0, User().id(), "Пачка %s изменение даты проверки" % self.pack.id()))
            if self.cb_date_complete.isChecked():

                if self.cb_date_make.isChecked():
                    self.pack.set_date_complete(self.de_date_complete.date())
                else:
                    result = QMessageBox.question(self, "Отметить", "Пачка еще не принята. Вы уверены что хотите ее отметить как проверенную?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if result == 16384:
                        self.pack.set_date_complete(self.de_date_complete.date())
                    else:
                        self.cb_date_complete.setChecked(False)
            else:
                self.pack.set_date_complete(None)

    def ui_edit_date_make(self):
        if not self.insert_values_sql:
            self.logger.info(u"[Крой {:04d} Пользователь {:04d}] {}".format(self.pack.number_cut() or 0, User().id(), "Пачка %s изменение даты приемки" % self.pack.id()))
            if self.cb_date_make.isChecked():
                self.pack.set_date_make(self.de_date_make.date())
            else:
                self.pack.set_date_make(None)

    def ui_edit_size(self, size):
        if not self.insert_values_sql:
            self.pack.set_size(size)

    def ui_edit_value_product(self):
        if not self.insert_values_sql:
            self.logger.info(u"[Крой {:04d} Пользователь {:04d}] {}".format(self.pack.number_cut() or 0, User().id(),
                                                                            "Пачка %s изменение кол-ва в пачке %s" % (self.pack.id(), self.le_value_product.text())))
            self.pack.set_value_pieces(self.le_value_product.text())
            self.set_value_pack()
            self.set_accessories_name()
            self.set_operation_name()

    def ui_edit_weight(self):
        if not self.insert_values_sql:
            self.logger.info(u"[Крой {:04d} Пользователь {:04d}] {}".format(self.pack.number_cut() or 0, User().id(),
                                                                            "Пачка %s изменение веса пачки %s" % (self.pack.id(), self.le_weight.text())))
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
            self.logger.info(u"[Крой {:04d} Пользователь {:04d}] {}".format(self.pack.number_cut() or 0, User().id(),
                                                                            "Пачка %s изменение кол-ва брака %s" % (self.pack.id(), self.le_value_damage.text())))
            self.pack.set_value_damage(self.le_value_damage.text())
            self.set_value_pack()
            self.set_accessories_name()
            self.set_operation_name()

    def ui_edit_print_label(self, bol):
        if bol:
            self.pack.set_print_label(1)
        else:
            self.pack.set_print_label(0)

    def ui_view_client(self):
        self.client_list = clients.ClientList(self, True)
        self.client_list.setWindowModality(Qt.ApplicationModal)
        self.client_list.show()

    def ui_del_client(self):
        self.pack.del_client()
        self.le_client.clear()
        self.le_client.setWhatsThis("")

    def ui_view_list_article(self):
        self.article_list = article.ArticleList(self, select_variant=True, open_variant=self.pack.article())
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
        self.one_operation_window.le_value.setText(str(self.pack.value_all()))  # Выставить кол-во в новой операции
        self.one_operation_window.setModal(True)
        self.one_operation_window.show()

        if self.one_operation_window.exec() <= 0:
            return False
        operation = self.one_operation_window.operation
        self.pack.set_operation(operation)
        self.set_operation_name()

    def ui_add_add_operation(self):
        self.new_operation = operation.OperationAddList(self, dc_select=True)
        self.new_operation.setWindowModality(Qt.ApplicationModal)
        self.new_operation.show()

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
        if not self.toolButton_8.isEnabled():
            return False
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

    def ui_change_price_operations(self):
        self.change_operation_window = PackChangePrice(self, self.pack.operations(), self.pack.parametr_id())
        self.change_operation_window.setModal(True)
        self.change_operation_window.show()

    def ui_double_click_accessories(self, table_item):
        if not self.toolButton_5.isEnabled():
            return False
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
        self.one_accessories_window.le_value.setText(str(self.pack.value()))
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

    def ui_add_material(self):
        self.add_material = PackAddMaterial()
        self.add_material.setModal(True)
        self.add_material.show()
        if self.add_material.exec() <= 0:
            return False

        materail = {"material_id": self.add_material.le_material.whatsThis(),
                    "material_name": self.add_material.le_material.text(),
                    "weight": self.add_material.le_weight.text().replace(",", "."),
                    "weight_rest": self.add_material.le_weight_rest.text().replace(",", ".")}

        result = self.pack.set_add_material(materail)
        if not result[0]:
            QMessageBox.critical(self, "Ошибка добавления ткани", result[1], QMessageBox.Ok)
            return False

        self.set_add_material()

    def ui_del_material(self):
        try:
            id_material = int(self.tw_add_material.item(self.tw_add_material.currentRow(), 0).data(-2))
        except:
            QMessageBox.information(self, "Ошибка", "Выберите запись.", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить доп материал?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            if not self.pack.del_add_material(id_material):
                QMessageBox.information(self, "Ошибка", "Доп материал не удалился", QMessageBox.Ok)
            else:
                self.set_add_material()

    def ui_calc_pack(self):
        value = self.pack.value()
        value_damage = self.pack.value_damage()
        weight = self.pack.weight()
        material_price = self.pack.material_price()

        query = """SELECT cut.Weight_Rest * 100 / (SUM(pack.Weight) + cut.Weight_Rest)
                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                      WHERE cut.Id = %s"""
        sql_info = my_sql.sql_select(query, (self.pack.number_cut(),))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения информации о проценте обрези", sql_info.msg, QMessageBox.Ok)
            return False
        rest_percent = sql_info[0][0]

        percent = int(self.le_calc_percent.text())

        operations_price = 0
        operations = self.pack.operations()
        for operation in operations:
            operations_price += operation["value"] * Decimal(str(operation["price"]))

        accessories_price = 0
        accessories = self.pack.accessories()
        for accessory in accessories:
            accessories_price += accessory["value"] * Decimal(str(accessory["value_thing"])) * Decimal(str(accessory["price"]))

        add_material_price = 0
        add_materials = self.pack.add_materials()
        for add_material in add_materials:
            add_material_price += (add_material["weight"] + add_material["weight_rest"]) * add_material["price"]

        price_one_weight = round((weight / value) * material_price, 4)
        price_many_weight = round(material_price * weight, 4)

        material_and_rest_one = price_one_weight + (price_one_weight / 100 * rest_percent)
        material_and_rest_many = price_many_weight + (price_many_weight / 100 * rest_percent)

        add_material_one = Decimal(round(add_material_price / value, 4))
        add_material_many = Decimal(round(add_material_price, 4))

        all_material_one = material_and_rest_one + add_material_one
        all_meterial_many = material_and_rest_many + add_material_many

        price_all_one = round((operations_price / value) + (accessories_price / value) + all_material_one, 4)
        price_all_many = round(operations_price + accessories_price + all_meterial_many, 4)



        self.le_calc_one_operation.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(operations_price / value, 4))))
        self.le_calc_many_operation.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(operations_price, 4))))
        self.le_calc_one_accessory.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(accessories_price / value, 4))))
        self.le_calc_many_accessory.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(accessories_price, 4))))
        self.le_calc_one_material.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_one_weight, 4))))
        self.le_calc_many_material.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_many_weight, 4))))
        self.le_calc_rest_cut.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(rest_percent, 4))))
        self.le_calc_rest_cut.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(rest_percent, 4))))
        self.le_calc_one_mat_and_rest.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(material_and_rest_one , 4))))
        self.le_calc_many_mat_and_rest.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(material_and_rest_many, 4))))
        self.le_calc_one_add_material.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(add_material_one, 4))))
        self.le_calc_many_add_material.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(add_material_many, 4))))
        self.le_calc_one_all_material.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_material_one, 4))))
        self.le_calc_many_all_material.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_meterial_many, 4))))
        self.le_calc_one_all.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_all_one, 4))))
        self.le_calc_many_all.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_all_many, 4))))
        self.le_calc_one_percent.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_all_one + (price_all_one * percent / 100), 4))))
        self.le_calc_many_percent.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(price_all_many + (price_all_many * percent / 100), 4))))

        self.le_calc_damage.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(material_price * value_damage, 4))))

    def ui_add_value(self):
        dialog = QInputDialog.getInt(self, "Введите сумму", "Введите на сколько пачка больше!", 0, 0, 150)
        if not dialog[1]:
            return False

        try:
            old_value = int(self.le_value_product.text())
            self.le_value_product.setText(str(old_value + dialog[0]))
            self.ui_edit_value_product()
        except:
            pass

    def ui_acc(self):
        if self.check_make():
            return False

        self.logger.info(u"[Крой {:04d} Пользователь {:04d}] {}".format(self.pack.number_cut() or 0, User().id(), "Пачка %s нажата кнопка принять" % self.pack.id()))

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
        if self.check_make():
            return False

        self.logger.info(u"[Крой {:04d} Пользователь {:04d}] {}".format(self.pack.number_cut() or 0, User().id(), "Пачка %s нажата кнопка отмена" % self.pack.id()))
        if self.pack.need_save_sql() and self.access_save_sql:
            result = QMessageBox.question(self, "Выйти?", "Есть несохраненая информация.\nТочно выйти без сохранения?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == 16384:
                self.close()
                self.destroy()
            else:
                return False
        else:
            self.close()
            self.destroy()

    def ui_print_pack_passport(self):
        cod = str(self.pack.id()).zfill(7)
        row_html = """<tr>
                        <td style="width: 30px; height: 30px; text-align: center; vertical-align: middle;"><strong>#o_number#</strong></td>
                        <td style="width: 500px; height: 30px; text-align: left; vertical-align: middle;"><strong>#o_name#</strong></td>
                        <td style="width: 120px; font-size: 10pt; height: 30px; text-align: center; vertical-align: middle;"><strong>#o_sw#</strong></td>
                        <td style="width: 70px; height: 30px; text-align: center; vertical-align: middle;">&nbsp;</td>
                        <td style="width: 150px; height: 30px; text-align: center; vertical-align: middle;">&nbsp;</td>
                        <td style="width: 120px; height: 30px; text-align: center; vertical-align: middle;">&nbsp;</td>
                        </tr>"""

        operation_table = ""

        for operation in self.pack.operations():
            query = "SELECT sewing_machine.Name FROM operations LEFT JOIN sewing_machine ON operations.Sewing_Machine_Id = sewing_machine.Id WHERE operations.Id = %s"
            sql_info = my_sql.sql_select(query, (operation["operation_id"],))
            if "mysql.connector.errors" in str(type(sql_info)):
                print("Не смог получить данные пачки")
                return False
            new_row_html = row_html.replace("#o_number#", str(operation["position"]))
            new_row_html = new_row_html.replace("#o_name#", str(operation["name"]))
            new_row_html = new_row_html.replace("#o_sw#", sql_info[0][0])

            operation_table = operation_table + "\n" + new_row_html

        barcode.generate(cod)

        html = codecs.open(getcwd() + "/templates/pack/passport.html", encoding='utf-8').read()
        html = html.replace("#art#", str(self.pack.parametr_name()))
        html = html.replace("#size#", str(self.pack.size()))
        html = html.replace("#cut#", str(self.pack.number_cut()))
        html = html.replace("#pack#", str(self.pack.number_pack()))
        html = html.replace("#data#", self.pack.cut_date().strftime("%d.%m.%Y"))
        html = html.replace("#pac_barcode_src#", "%s.%s" % (cod, "svg"))
        html = html.replace("#art_name#", str(self.pack.article_product_name()))
        html = html.replace("#pack_value#", str(self.pack.value()))
        html = html.replace("#client#", str(self.pack.client_name()))
        html = html.replace("#art_barcode#", str(self.pack.article_barcode()))
        html = html.replace("#note_art#", str(self.pack.note_article()))
        html = html.replace("#note#", str(self.pack.note()))
        html = html.replace("#o_table#", operation_table)

        self.logger.info(u"[Крой {:04d} Пользователь {:04d}] {}".format(self.pack.number_cut() or 0, User().id(), "Пачка %s напечатан паспорт" % self.pack.id()))
        self.print_class = print_qt.PrintHtml(self, html)

        files.del_temp_file(cod + ".svg")

    def ui_print_label(self):
        data = {
                "article": self.pack.article(),
                "article_size": self.pack.article_size(),
                "article_parametr": self.pack.parametr_name(),
                "article_barcode": self.pack.article_barcode(),
                "pack_id": self.pack.id(),
                "label_value": self.pack.value()}
        self.print_label = print_label.LabelFile(self.pack.parametr_id(), "Путь корень бирки", data)
        self.print_label.setModal(True)
        self.print_label.show()

    def ui_copy_pack(self):
        self.pack_list_window = ListPackNumber(self.pack.number_cut())
        self.pack_list_window.setModal(True)
        self.pack_list_window.show()

        id = self.pack_list_window.exec()

        if id <= 0:
            return False

        self.pack.copy_pack(id)

        self.le_article.setText(self.pack.article_name())
        self.le_article.setWhatsThis(str(self.pack.article_id()))

        self.le_size.setText(self.pack.size())

        self.le_client.setText(self.pack.client_name())
        self.le_client.setWhatsThis(str(self.pack.client()))

        self.le_order.setText(str(self.pack.order()))
        self.le_order.setWhatsThis(str(self.pack.order()))

        self.le_note.setText(self.pack.note())

        self.set_operation_name()
        self.set_accessories_name()

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
            if round(dict["value"] * dict["value_thing"], 4) != round(dict["sql_value_sum"], 4):
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
            value_thing = float(dict["value_thing"]) if dict["value_thing"] is not None else 0

            new_table_item = QTableWidgetItem(str(round(price * value_thing, 4)))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_accessories.setItem(row, 5, new_table_item)

            new_table_item = QTableWidgetItem(str(round(price * (value * value_thing), 4)))
            new_table_item.setData(-2, dict["id"])
            if color is not None:
                new_table_item.setBackground(color)
                new_table_item.setToolTip(note)
            self.tw_accessories.setItem(row, 6, new_table_item)

            row += 1

    def set_add_material(self):
        material_list = self.pack.add_materials()
        self.tw_add_material.clearContents()
        self.tw_add_material.setRowCount(0)
        row = 0
        for dict in material_list:
            self.tw_add_material.insertRow(row)

            new_table_item = QTableWidgetItem(str(dict["material_name"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_add_material.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["weight"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_add_material.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["weight_rest"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_add_material.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(dict["price"]))
            new_table_item.setData(-2, dict["id"])
            self.tw_add_material.setItem(row, 3, new_table_item)

    def set_value_pack(self):
        self.le_value_all.setText(str(self.pack.value_all()))

    def check_make(self):
        if self.reminder_make and not self.cb_date_make.isChecked():
            QMessageBox.question(self, "Выйти?", "Вы не приняли пачку!\nНе забудьте про галочку!", QMessageBox.Ok)
            self.reminder_make = False
            return True
        return False

    def of_select_variant(self, variant):
        query = """SELECT product_article_size.Size
                      FROM product_article_parametrs 
                      LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                    WHERE product_article_parametrs.Id = %s"""
        sql_result = my_sql.sql_select(query, (variant[0], ))
        if "mysql.connector.errors" in str(type(sql_result)):
                QMessageBox.critical(self, "Ошибка sql получение размера", sql_result.msg, QMessageBox.Ok)

        self.le_article.setWhatsThis(str(variant[0]))
        self.le_article.setText(variant[1])

        if sql_result:
            self.le_size.setText(sql_result[0][0])

        self.pack.set_article(variant[0])

        if self.pack.id() is None:
            self.pack.clear_save_operation()
            self.pack.take_article_operations()
            self.set_operation_name()

            self.pack.clear_save_accessories()
            self.pack.take_article_accessories()
            self.set_accessories_name()

    def of_list_clients(self, client):
        self.le_client.setText(client[1])
        self.le_client.setWhatsThis(str(client[0]))
        self.pack.set_client(int(client[0]))

    def of_tree_select_order(self, order):
        self.le_order.setText(str(order[0]))
        self.le_order.setWhatsThis(str(order[1]))
        self.pack.set_order(order[1])

    def of_tree_select_add_operation(self, operation):

        query = "SELECT operations.Price FROM operations WHERE Id = %s"
        sql_info = my_sql.sql_select(query, (operation[1],))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения цены операции", sql_info.msg, QMessageBox.Ok)
            return False

        operation = {"id": None,
                     "position": None,
                     "operation_id": operation[1],
                     "name": operation[0],
                     "worker_id": None,
                     "worker_name": None,
                     "date_make": None,
                     "date_input": None,
                     "value": self.pack.value(),
                     "price": float(sql_info[0][0]),
                     "pay": 0}

        self.pack.set_operation(operation)
        self.set_operation_name()

    def of_set_new_price_operation(self, operation):  # функция вызывается при массовом изменени цены операции, изменяет цену операции.
        self.pack.set_operation(operation, operation["id"])
        self.set_operation_name()


class PackOperation(QDialog):
    def __init__(self, operation=None):
        super(PackOperation, self).__init__()
        loadUi(getcwd() + '/ui/pack_operation.ui', self)
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
            self.le_name.setReadOnly(True)
            self.de_make.setReadOnly(True)
            self.de_input.setReadOnly(True)

            self.toolButton.setEnabled(False)
            self.toolButton_2.setEnabled(False)
            self.toolButton_3.setEnabled(False)

    def ui_acc(self):

        if self.le_value.text() == "New" or self.le_value.text() == "" or self.le_value.text() == "0" or self.le_value.text() == "None":
            QMessageBox.information(self, "Кол-во", "Введите кол-во операций", QMessageBox.Ok)
            return False

        if self.le_operation.text() != "" and self.le_operation.text() != "None":
            self.operation["operation_id"] = int(self.le_operation.whatsThis())
            self.operation["name"] = self.le_name.text()

        if self.le_worker.text() != "" and self.le_worker.text() != "None":
            self.operation["worker_id"] = int(self.le_worker.whatsThis())
            self.operation["worker_name"] = self.le_worker.text()
            self.operation["date_make"] = self.de_make.date()
            self.operation["date_input"] = self.de_input.date()
        else:
            self.operation["worker_id"] = None
            self.operation["worker_name"] = None
            self.operation["date_make"] = None
            self.operation["date_input"] = None

        if self.le_price.text() != "" and self.le_price.text() != "None":
            self.operation["price"] = float(self.le_price.text().replace(",", "."))

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


class PackChangePrice(QDialog):
    def __init__(self, main, operations, article_id):
        super(PackChangePrice, self).__init__()
        loadUi(getcwd() + '/ui/pack_change_price_operations.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.set_size_table()
        self.get_access_change_price(article_id)
        self.set_table_operations(operations)
        self.operations = operations
        self.main = main

    def set_size_table(self):
        self.tw_operations.horizontalHeader().resizeSection(0, 200)
        self.tw_operations.horizontalHeader().resizeSection(1, 75)
        self.tw_operations.horizontalHeader().resizeSection(2, 75)

    def get_access_change_price(self, article_id):
        query = """SELECT product_article_operation.Operation_Id FROM product_article_operation WHERE Product_Article_Parametrs_Id = %s AND Change_Price = 1"""
        sql_info = my_sql.sql_select(query, (article_id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            return False

        self.accept_operations_id = [i[0] for i in sql_info]

    def set_table_operations(self, operations):
        row = 0
        for dict in operations:
            if dict["operation_id"] in self.accept_operations_id:
                self.tw_operations.insertRow(row)

                new_table_item = QTableWidgetItem(str(dict["name"]))
                new_table_item.setData(-2, dict)
                self.tw_operations.setItem(row, 0, new_table_item)

                new_table_item = QTableWidgetItem(str(dict["price"]))
                self.tw_operations.setItem(row, 1, new_table_item)

                row += 1

    def ui_calc(self):
        multiply = str_to.str_to_float(self.le_multiply_price.text())
        for row in range(self.tw_operations.rowCount()):
            old_price = str_to.str_to_float(self.tw_operations.item(row, 1).text())
            new_price = round(old_price * multiply, 2)

            new_table_item = QTableWidgetItem(str(new_price))
            self.tw_operations.setItem(row, 2, new_table_item)

    def ui_acc(self):
        for row in range(self.tw_operations.rowCount()):
            try:
                if not self.tw_operations.item(row, 2).text():
                    QMessageBox.information(self, "Ошибка цены", "В строчке %s неправильное значение" % row, QMessageBox.Ok)
                    return False
            except AttributeError:
                QMessageBox.information(self, "Ошибка цены", "В строчке %s нет цены" % row, QMessageBox.Ok)
                return False

        for row in range(self.tw_operations.rowCount()):
            operation_dict = self.tw_operations.item(row, 0).data(-2)
            operation_dict["price"] = str_to.str_to_float(self.tw_operations.item(row, 2).text())

            self.main.of_set_new_price_operation(operation_dict)
        else:
            self.close()
            self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()


class PackAccessories(QDialog):
    def __init__(self, accessories=None):
        super(PackAccessories, self).__init__()
        loadUi(getcwd() + '/ui/pack_accsessories.ui', self)
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
        self.accessories_name = supply_accessories.AccessoriesName(self, True)
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


class PackAddMaterial(QDialog):
    def __init__(self):
        super(PackAddMaterial, self).__init__()
        loadUi(getcwd() + '/ui/pack_add_material.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

    def ui_view_material(self):
        self.material_name = supply_material.MaterialName(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_acc(self):
        if not self.le_material.text():
            QMessageBox.critical(self, "Ошибка материала", "Выберите материал", QMessageBox.Ok)
            return False

        try:
            float(self.le_weight.text().replace(",", "."))
        except:
            QMessageBox.critical(self, "Ошибка кол-вы", "Неправильно задано количство", QMessageBox.Ok)
            return False

        self.done(1)
        self.close()

    def ui_can(self):
        self.done(-1)
        self.close()
        self.destroy()

    def of_list_material_name(self, item):
        self.le_material.setWhatsThis(str(item[0]))
        self.le_material.setText(item[1])


class ListPackNumber(QDialog):
    def __init__(self, cut_id):
        super(ListPackNumber, self).__init__()
        loadUi(getcwd() + '/ui/pack_list_number.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.cut_id = cut_id

        self.start_sql()

    def start_sql(self):
        query = """SELECT pack.Id, CONCAT(pack.Number, ' ', product_article.Article, ' (', product_article_size.Size, ') [', product_article_parametrs.Name, ']')
                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE cut.Id = %s ORDER BY pack.Number"""
        sql_info = my_sql.sql_select(query, (self.cut_id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения пачек", sql_info.msg, QMessageBox.Ok)
            return False

        for pack in sql_info:
            item = QListWidgetItem(pack[1])
            item.setData(5, pack[0])
            self.listWidget.addItem(item)

    def ui_select(self, item):
        self.done(int(item.data(5)))
        self.close()
        self.destroy()


class PackFilter(QDialog):
    def __init__(self, main):
        super(PackFilter, self).__init__()
        loadUi(getcwd() + '/ui/pack_filter.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main

    def start_settings(self):
        self.de_date_cut_from.setDate(QDate.currentDate())
        self.de_date_cut_to.setDate(QDate.currentDate())
        self.de_date_make_from.setDate(QDate.currentDate())
        self.de_date_make_to.setDate(QDate.currentDate())
        self.de_date_complete_from.setDate(QDate.currentDate())
        self.de_date_complete_to.setDate(QDate.currentDate())

    def ui_view_article(self):
        self.article_list = article.ArticleList(self, select_variant=True)
        self.article_list.setWindowModality(Qt.ApplicationModal)
        self.article_list.show()

    def ui_view_client(self):
        self.client_list = clients.ClientList(self, True)
        self.client_list.setWindowModality(Qt.ApplicationModal)
        self.client_list.show()

    def ui_view_order(self):
        self.order_list = order.OrderList(self, True)
        self.order_list.setWindowModality(Qt.ApplicationModal)
        self.order_list.show()

    def ui_view_material(self):
        self.material_name = supply_material.MaterialName(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_acc(self):
        where = ""

        # Блок условий ID пачки
        if self.le_id_pack.text() != '':
            where = self.add_filter(where, "(pack.Id = %s)" % self.le_id_pack.text())

        # Блок  условий номера кроя
        if self.le_cut_num.text() != '':
            where = self.add_filter(where, "(pack.Cut_Id = %s)" % self.le_cut_num.text())

        # Блок  условий выбора номера пачки
        if self.le_pack_num.text() != '':
            where = self.add_filter(where, "(pack.Number = %s)" % self.le_pack_num.text())

        # Блок условий выбора артикула
        if self.gb_article.isChecked() and self.le_art.text() != "":
            if self.rb_art.isChecked():
                where = self.add_filter(where, "(product_article.Id = %s)" % self.rb_art.whatsThis())
            elif self.rb_size.isChecked():
                where = self.add_filter(where, "(product_article_size.Id = %s)" % self.rb_size.whatsThis())
            elif self.rb_parametr.isChecked():
                where = self.add_filter(where, "(product_article_parametrs.Id = %s)" % self.rb_parametr.whatsThis())

        # Блок  условий выбора клиента
        if self.le_client.text() != "":
            where = self.add_filter(where, "(pack.Client_Id = %s)" % self.le_client.whatsThis())

        # Блок  условий выбора закза
        if self.le_order.text() != "":
            where = self.add_filter(where, "(pack.Order_Id = %s)" % self.le_order.whatsThis())

        # Блок  условий выбора ткани
        if self.le_material.text() != "":
            where = self.add_filter(where, "(cut.Material_Id = %s)" % self.le_material.whatsThis())

        # блок условий выбора веса
        if self.le_weight_from.text() != "" and self.le_weight_to != "":
            where = self.add_filter(where, "(pack.Weight BETWEEN %s AND %s)" % (self.le_weight_from.text(), self.le_weight_to.text()))

        # Блок условий выбора колва
        if self.le_value_from.text() != "" and self.le_value_to != "":
            where = self.add_filter(where, "(pack.Value_Pieces BETWEEN %s AND %s)" % (self.le_value_from.text(), self.le_value_to.text()))

        # Блок условий выбора брака
        if self.le_damag_from.text() != "" and self.le_damag_to != "":
            where = self.add_filter(where, "(pack.Weight BETWEEN %s AND %s)" % (self.le_damag_from.text(), self.le_damag_to.text()))

        # Блок  условий даты коря
        if self.gb_date_cut.isChecked():
            sql_date = "(cut.Date_Cut >= '%s' AND cut.Date_Cut <= '%s')" % \
                       (self.de_date_cut_from.date().toString(Qt.ISODate), self.de_date_cut_to.date().toString(Qt.ISODate))
            where = self.add_filter(where, sql_date)

        # Блок условий даты приемки
        if self.gb_make.isChecked():
            if self.cb_make.isChecked():
                where = self.add_filter(where, "(pack.Date_Make IS NULL)")
            else:
                sql_date = "(pack.Date_Make >= '%s' AND pack.Date_Make <= '%s')" % \
                           (self.de_date_make_from.date().toString(Qt.ISODate), self.de_date_make_to.date().toString(Qt.ISODate))
                where = self.add_filter(where, sql_date)

        # Блок условий даты проверки
        if self.gb_complete.isChecked():
            if self.cb_complete.isChecked():
                where = self.add_filter(where, "(pack.Date_Coplete IS NULL)")
            else:
                sql_date = "(pack.Date_Coplete >= '%s' AND pack.Date_Coplete <= '%s')" % \
                           (self.de_date_complete_from.date().toString(Qt.ISODate), self.de_date_complete_to.date().toString(Qt.ISODate))
                where = self.add_filter(where, sql_date)

        # Делаем замену так как Were должно быть перед Group by
        if where:
            self.sql_query_all = self.sql_query_all.replace("LIMIT", " WHERE " + where + " LIMIT ")

        self.main.of_set_filter(self.sql_query_all)

        self.close()

    def ui_can(self):
        self.close()

    def add_filter(self, where, add, and_add=True):
        if where:
            if and_add:
                where += " AND " + add
            else:
                where += " OR " + add
        else:
            where = add

        return where

    def of_select_variant(self, variant):
        query = """SELECT product_article_size.Article_Id, product_article_size.Size
                      FROM product_article_parametrs 
                      LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                    WHERE product_article_parametrs.Id = %s"""
        sql_result = my_sql.sql_select(query, (variant[0], ))
        if "mysql.connector.errors" in str(type(sql_result)):
            QMessageBox.critical(self, "Ошибка sql получение артиикула", sql_result.msg, QMessageBox.Ok)
            return False

        self.le_art.setWhatsThis(str(variant[0]))
        self.le_art.setText(variant[1])

        self.rb_art.setWhatsThis(str(sql_result[0][0]))
        self.rb_size.setWhatsThis(str(sql_result[0][1]))
        self.rb_parametr.setWhatsThis(str(variant[0]))

    def of_list_clients(self, client):
        self.le_client.setText(client[1])
        self.le_client.setWhatsThis(str(client[0]))

    def of_tree_select_order(self, order):
        self.le_order.setText(str(order[0]))
        self.le_order.setWhatsThis(str(order[1]))

    def of_list_material_name(self, item):
        self.le_material.setWhatsThis(str(item[0]))
        self.le_material.setText(item[1])

    def of_set_sql_query(self, sql):
        self.sql_query_all = sql
