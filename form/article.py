from os import getcwd, path, mkdir, listdir
from form.templates import tree
from form import operation, supply_material, supply_accessories, print_label
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QMainWindow, QInputDialog, QTableWidgetItem, QShortcut, QListWidgetItem, QLineEdit, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5 import QtCore
from function import my_sql, table_to_html
from classes.my_class import User
from classes import print_qt

article_class = loadUiType(getcwd() + '/ui/article.ui')[0]
article_change_operation_class = loadUiType(getcwd() + '/ui/article_change_operation.ui')[0]
article_change_material_class = loadUiType(getcwd() + '/ui/article_change_material.ui')[0]
article_copy_parametr = loadUiType(getcwd() + '/ui/article_copy_parametr.ui')[0]
article_filter = loadUiType(getcwd() + '/ui/article_filter.ui')[0]


class ArticleList(tree.TreeList):

    def set_settings(self):

        self.filter = None

        self.resize(1000, 400)

        self.setWindowTitle("Список артикулов")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(167, 183, 255);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Артикул", 70), ("Название", 230), ("Размеры", 220), ("Варианты", 200))

        self.query_tree_select = "SELECT Id, Parent_Id, Name FROM product_tree ORDER BY Parent_Id, Position"
        self.query_tree_add = "INSERT INTO product_tree (Parent_Id, Name, Position) VALUES (%s, %s, %s)"
        self.query_tree_change = "UPDATE product_tree SET Name = %s, Position = %s WHERE Id = %s"
        self.query_tree_del = "DELETE FROM product_tree WHERE Id = %s"

        self.query_table_all = """SELECT product_article.Id, product_article.Tree_Id, product_article.Article, product_article.Name,
                                      GROUP_CONCAT(DISTINCT product_article_size.Size ORDER BY product_article_size.Size),
                                      GROUP_CONCAT(DISTINCT product_article_parametrs.Name ORDER BY product_article_parametrs.Name)
                                      FROM product_article
                                        LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id
                                        LEFT JOIN product_article_parametrs ON product_article_size.Id = product_article_parametrs.Product_Article_Size_Id
                                      GROUP BY product_article.Article
                                      ORDER BY product_article.Article"""

        #  нулевой элемент должен быть ID а первый Parent_ID (ID категории)
        self.query_table_select = """SELECT product_article.Id, product_article.Tree_Id, product_article.Article, product_article.Name,
                                      GROUP_CONCAT(DISTINCT product_article_size.Size ORDER BY product_article_size.Size),
                                      GROUP_CONCAT(DISTINCT product_article_parametrs.Name ORDER BY product_article_parametrs.Name)
                                      FROM product_article
                                        LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id
                                        LEFT JOIN product_article_parametrs ON product_article_size.Id = product_article_parametrs.Product_Article_Size_Id
                                      GROUP BY product_article.Article
                                      ORDER BY product_article.Article"""
        self.query_transfer_item = "UPDATE product_article SET Tree_Id = %s WHERE Id = %s"
        self.query_table_dell = "DELETE FROM product_article WHERE Id = %s"

        # Настройки окна добавления и редактирования дерева
        self.set_new_win_tree = {"WinTitle": "Добавление категории",
                                 "WinColor": "(167, 183, 255)",
                                 "lb_name": "Название категории"}

        # Настройки окна переноса элементов
        self.set_transfer_win = {"WinTitle": "Изменение категории",
                                 "WinColor": "(167, 183, 255)"}

        self.pb_table_double.deleteLater()
        self.pb_other.deleteLater()

        # Быстрый фильтр
        self.le_fast_filter = QLineEdit()
        self.le_fast_filter.setPlaceholderText("Артикул")
        self.le_fast_filter.setMaximumWidth(150)
        self.le_fast_filter.editingFinished.connect(self.fast_filter)
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(dummy)
        self.toolBar.addWidget(self.le_fast_filter)

    def ui_add_table_item(self):  # Добавить предмет
        try:
            tree_id = self.tree_widget.selectedItems()[0].data(0, 5)
        except:
            QMessageBox.critical(self, "Ошибка ", "Выделите элемент дерева куда добавлять предмет", QMessageBox.Ok)
            return False
        if tree_id < 0:
            QMessageBox.critical(self, "Ошибка ", "Вы выбрали неправильный элемент", QMessageBox.Ok)
            return False

        self.new_operation = Article(self, False, tree_id)
        self.new_operation.setWindowModality(QtCore.Qt.ApplicationModal)
        self.new_operation.show()

    def ui_change_table_item(self, id=False):  # изменить элемент
        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
                return False

        self.new_operation = Article(self, item_id)
        self.new_operation.setWindowModality(QtCore.Qt.ApplicationModal)
        self.new_operation.show()

    def ui_double_item_table(self):  # Дублирование строки
        try:
            item_id = self.table_widget.selectedItems()[0].data(5)
        except:
            QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите дублировать", QMessageBox.Ok)
            return False
        query = "INSERT INTO operations (Tree_Id, Name, Price, Sewing_Machine_Id, Note) " \
                "(SELECT Tree_Id, Name, Price, Sewing_Machine_Id, Note FROM operations WHERE Id = %s)"
        sql_info = my_sql.sql_change(query, (item_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql дублирование строки", sql_info.msg, QMessageBox.Ok)
            return False
        self.set_table_info()

    def ui_double_click_table_item(self, item):  # Двойной клик по элементу
        if not self.dc_select:
            self.ui_change_table_item(item.data(5))
        else:
            item_id = item.data(5)
            self.new_operation = Article(self.main, item_id, dc_select=True)
            self.new_operation.setWindowModality(QtCore.Qt.ApplicationModal)
            self.new_operation.show()

    def ui_filter_table(self):
        if self.filter is None:
            self.filter = ArticleFilter(self)
        self.filter.of_set_sql_query(self.query_table_all)
        self.filter.setWindowModality(QtCore.Qt.ApplicationModal)
        self.filter.show()

    def fast_filter(self):
        # Блок условий артикула
        if self.le_fast_filter.text() != '':
            q_filter = " WHERE (product_article.Article LIKE '%s')" % ("%" + self.le_fast_filter.text() + "%", )
            self.query_table_select = self.query_table_all.replace("GROUP BY", q_filter + " GROUP BY")
        else:
            self.query_table_select = self.query_table_all

        self.ui_update_table()

    def of_set_filter(self, sql):
        self.query_table_select = sql

        self.ui_update_table()


class Article(QMainWindow, article_class):
    def __init__(self, main, id=False, tree_id=False, dc_select=False):
        super(Article, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.access_save_sql = True
        self.main = main
        self.id = id
        self.tree_id = tree_id
        self.view_show = False
        self.show_complete = False  # Переменная показывает что страница загружена
        self.dc_select = dc_select
        self.save_change = []  # Переменная для запоминания изменений
        self.pb_up.setIcon(QIcon(getcwd() + "/images/up.ico"))
        self.pb_down.setIcon(QIcon(getcwd() + "/images/down.ico"))
        self.set_start_settings()
        self.show_complete = True  # Переменная показывает что страница загружена
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

    def set_start_settings(self):
        # Ширина материалов
        self.tw_materials.horizontalHeader().resizeSection(0, 240)
        self.tw_materials.horizontalHeader().resizeSection(1, 80)
        self.tw_materials.horizontalHeader().resizeSection(2, 80)
        self.tw_materials.horizontalHeader().resizeSection(3, 80)
        # Ширина операций
        self.tw_operations.horizontalHeader().resizeSection(0, 250)
        self.tw_operations.horizontalHeader().resizeSection(1, 80)
        self.tw_operations.horizontalHeader().resizeSection(2, 110)

        if not self.id and self.tree_id:  # Если новый артикул
            self.set_enabled(False)  # закрываем поля
            self.gb_parametrs.setEnabled(False)

        if self.id:
            if not self.dc_select:
                self.set_start_sql_info()
            else:
                self.set_start_sql_info()
                self.set_all_enabled(False)

        key_up = QShortcut(QtCore.Qt.Key_Up, self)
        key_up.activated.connect(self.key_up)
        key_down = QShortcut(QtCore.Qt.Key_Down, self)
        key_down.activated.connect(self.key_down)
        key_left = QShortcut(QtCore.Qt.Key_Left, self)
        key_left.activated.connect(self.key_left)
        key_right = QShortcut(QtCore.Qt.Key_Right, self)
        key_right.activated.connect(self.key_right)
        key_j = QShortcut(QtCore.Qt.Key_J, self)
        key_j.activated.connect(self.ui_add_operation)
        key_j.activated.connect(self.ui_save_change_operation)
        key_n = QShortcut(QtCore.Qt.Key_N, self)
        key_n.activated.connect(self.ui_add_material)
        key_n.activated.connect(self.ui_save_change_material)
        key_A = QShortcut(QtCore.Qt.Key_A, self)
        key_A.activated.connect(self.ui_add_accessories)
        key_A.activated.connect(self.ui_save_change_material)

    def set_start_sql_info(self):
        if not self.get_start_sql_info():
            return False

        self.le_article.setText(self.article_size[0][0])
        self.le_article.setWhatsThis(str(self.id))
        self.le_name.setText(self.article_size[0][1])

        self.cb_size.clear()
        for size in self.article_size:
            self.cb_size.addItem(size[3], size[2])

        self.calc()
        if "article" in self.save_change:
            self.save_change.remove("article")

    def get_start_sql_info(self):
        query = """SELECT product_article.Article, product_article.Name,product_article_size.Id , product_article_size.Size
                  FROM product_article LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id WHERE product_article.Id = %s
                  ORDER BY product_article_size.Size"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения размера", sql_info.msg, QMessageBox.Ok)
            return False
        self.article_size = sql_info

        query = """SELECT product_article_parametrs.Product_Article_Size_Id, product_article_parametrs.Id, product_article_parametrs.Name,
                product_article_parametrs.Client_Name, product_article_parametrs.Barcode, product_article_parametrs.Client_code, product_article_parametrs.In_On_Place,
                product_article_parametrs.Price, product_article_parametrs.Product_Note, product_article_parametrs.Cut_Note, product_article_parametrs.`Show`,
                product_article_parametrs.NDS FROM product_article LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id
                LEFT JOIN product_article_parametrs ON product_article_size.Id = product_article_parametrs.Product_Article_Size_Id WHERE product_article.Id = %s
                order by product_article_parametrs.Name"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения настроек", sql_info.msg, QMessageBox.Ok)
            return False
        self.article_parametrs = sql_info

        query = """SELECT product_article_operation.Product_Article_Parametrs_Id, product_article_operation.Id, product_article_operation.Operation_Id,
                    operations.Name, operations.Price, sewing_machine.Name
                    FROM product_article LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id
                    LEFT JOIN product_article_parametrs ON product_article_size.Id = product_article_parametrs.Product_Article_Size_Id
                    LEFT JOIN product_article_operation ON product_article_parametrs.Id = product_article_operation.Product_Article_Parametrs_Id
                    LEFT JOIN operations ON product_article_operation.Operation_Id = operations.Id
                    LEFT JOIN sewing_machine ON operations.Sewing_Machine_Id = sewing_machine.Id
                    WHERE product_article.Id = %s ORDER BY product_article_operation.Position"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения операций", sql_info.msg, QMessageBox.Ok)
            return False
        self.article_operations = sql_info

        query = """SELECT product_article_material.Product_Article_Parametrs_Id, product_article_material.Id, product_article_material.Material_Id,
                    material_name.Name, product_article_material.Value, material_supplyposition.Price
                    FROM product_article LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id
                    LEFT JOIN product_article_parametrs ON product_article_size.Id = product_article_parametrs.Product_Article_Size_Id
                    LEFT JOIN product_article_material ON product_article_parametrs.Id = product_article_material.Product_Article_Parametrs_Id
                    LEFT JOIN material_name ON product_article_material.Material_Id = material_name.Id
                    LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                    LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                    WHERE product_article.Id = %s AND product_article_material.Material_Id IS NOT NULL
                    AND (material_supply.Data = (SELECT min(material_supply.Data) FROM material_supply
                    LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                    LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                    WHERE material_balance.BalanceWeight > 0 AND material_supplyposition.Material_NameId = product_article_material.Material_Id)
                    OR material_supply.Data IS NULL)
                    GROUP BY product_article_material.Id"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения материала", sql_info.msg, QMessageBox.Ok)
            return False
        self.article_material = sql_info

        query = """SELECT product_article_material.Product_Article_Parametrs_Id, product_article_material.Id,product_article_material.Accessories_Id,
                    accessories_name.Name, product_article_material.Value, accessories_supplyposition.Price
                    FROM product_article LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id
                    LEFT JOIN product_article_parametrs ON product_article_size.Id = product_article_parametrs.Product_Article_Size_Id
                    LEFT JOIN product_article_material ON product_article_parametrs.Id = product_article_material.Product_Article_Parametrs_Id
                    LEFT JOIN accessories_name ON product_article_material.Accessories_Id = accessories_name.Id
                    LEFT JOIN accessories_supplyposition ON accessories_name.Id = accessories_supplyposition.accessories_NameId
                    LEFT JOIN accessories_supply ON accessories_supplyposition.Accessories_SupplyId = accessories_supply.Id
                    WHERE product_article.Id = %s AND product_article_material.Accessories_Id IS NOT NULL
                    AND (accessories_supply.Data = (SELECT MIN(accessories_supply.Data) FROM accessories_supply
                    LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.Accessories_SupplyId
                    LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.Accessories_SupplyPositionId
                    WHERE accessories_balance.BalanceValue > 0 AND accessories_supplyposition.Accessories_NameId = product_article_material.Accessories_Id)
                    OR accessories_supply.Data IS NULL)
                    GROUP BY product_article_material.Id"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения аксесуаров", sql_info.msg, QMessageBox.Ok)
            return False
        self.article_accessories = sql_info

        return True

    def set_size_parametr(self):
        self.cb_parametrs.clear()
        if self.cb_size.currentData() is not None:
            select_size_id = int(self.cb_size.currentData())

            if hasattr(self, 'article_parametrs'):
                for param in self.article_parametrs:
                    if select_size_id == param[0] and param[10] == 1:
                        self.cb_parametrs.addItem(param[2], param[1])

            if self.cb_show.isChecked():
                icon = QIcon(getcwd() + "/images/eye.ico")
                for param in self.article_parametrs:
                    if select_size_id == param[0] and param[10] == 0:
                        self.cb_parametrs.addItem(icon, param[2], param[1])

    def set_parametr_info(self, other_param_id=False):  # Вставляем данные о параметрах получение из БД
        if not other_param_id:
            self.tw_operations.clearContents()
            self.tw_operations.setRowCount(0)
            self.tw_materials.clearContents()
            self.tw_materials.setRowCount(0)
        self.le_client_name.clear()
        self.le_barcode.clear()
        self.le_client_code.clear()
        self.le_in_on_place.setText("0")
        self.le_price.setText("0")
        self.pe_product_note.clear()
        self.pe_cut_note.clear()
        select_param_id = self.cb_parametrs.currentData() if (not other_param_id) else other_param_id
        status_sql = "set" if (not other_param_id) else "new"
        if select_param_id is None:
            return False
        if self.cb_parametrs.itemIcon(self.cb_parametrs.currentIndex()).isNull():
            self.pb_show_param.setText("Скрыть")
        else:
            self.pb_show_param.setText(" Показ. ")
        for param_info in self.article_parametrs:
            if select_param_id == param_info[1]:
                self.le_client_name.setText(param_info[3])
                self.le_barcode.setText(param_info[4])
                self.le_client_code.setText(param_info[5])
                in_on_place = param_info[6] if (param_info[6] is not None) else "0"
                self.le_in_on_place.setText(str(in_on_place))
                price = param_info[7] if (param_info[7] is not None) else "0"
                self.le_price.setText(str(price))
                self.pe_product_note.appendPlainText(param_info[8])
                self.pe_cut_note.appendPlainText(param_info[9])
                if param_info[11] == 18:
                    self.rb_nds_1.setChecked(True)
                else:
                    self.rb_nds_2.setChecked(True)
                break

        for operation in self.article_operations:
            if select_param_id == operation[0]:
                self.tw_operations.insertRow(self.tw_operations.rowCount())
                for i in range(3, len(operation)):
                    new_item = QTableWidgetItem(str(operation[i]))
                    new_item.setData(5, operation[2])
                    new_item.setData(-1, status_sql)
                    new_item.setData(-2, operation[1])
                    self.tw_operations.setItem(self.tw_operations.rowCount() - 1, i - 3, new_item)

        for material in self.article_material:
            if select_param_id == material[0]:
                self.tw_materials.insertRow(self.tw_materials.rowCount())
                for i in range(3, len(material)):
                    material_text = material[i] if (material[i] is not None) else "0"
                    new_item = QTableWidgetItem(str(material_text))
                    new_item.setData(5, material[2])
                    new_item.setData(-1, status_sql)
                    new_item.setData(-2, material[1])
                    new_item.setBackground(QBrush(QColor(153, 221, 255, 255)))
                    self.tw_materials.setItem(self.tw_materials.rowCount() - 1, i - 3, new_item)
                else:
                    material_price = material[5] if (material[5] is not None) else 0
                    new_item = QTableWidgetItem(str(round(material[4] * material_price, 4)))
                    new_item.setData(5, material[2])
                    new_item.setData(-1, status_sql)
                    new_item.setData(-2, material[1])
                    new_item.setBackground(QBrush(QColor(153, 221, 255, 255)))
                    self.tw_materials.setItem(self.tw_materials.rowCount() - 1, 3, new_item)

        for accessories in self.article_accessories:
            if select_param_id == accessories[0]:
                self.tw_materials.insertRow(self.tw_materials.rowCount())
                for i in range(3, len(accessories)):
                    accessories_text = accessories[i] if (accessories[i] is not None) else 0
                    new_item = QTableWidgetItem(str(accessories_text))
                    new_item.setData(5, accessories[2])
                    new_item.setData(-1, status_sql)
                    new_item.setData(-2, accessories[1])
                    new_item.setBackground(QBrush(QColor(252, 163, 255, 255)))
                    self.tw_materials.setItem(self.tw_materials.rowCount() - 1, i - 3, new_item)
                else:
                    accessories_price = accessories[5] if (accessories[5] is not None) else 0
                    new_item = QTableWidgetItem(str(round(accessories[4] * accessories_price, 4)))
                    new_item.setData(5, accessories[2])
                    new_item.setData(-1, status_sql)
                    new_item.setData(-2, accessories[1])
                    new_item.setBackground(QBrush(QColor(252, 163, 255, 255)))
                    self.tw_materials.setItem(self.tw_materials.rowCount() - 1, 3, new_item)
        self.calc()
        if not other_param_id:
            if "parametr" in self.save_change:
                self.save_change.remove("parametr")
            if "operation" in self.save_change:
                self.save_change.remove("operation")
            if "material" in self.save_change:
                self.save_change.remove("material")
        else:
            if "parametr" not in self.save_change:
                self.save_change.append("parametr")
            if "operation" not in self.save_change:
                self.save_change.append("operation")
            if "material" not in self.save_change:
                self.save_change.append("material")

    def ui_add_size(self):
        id = self.le_article.whatsThis()
        if not id:
            new_name = self.le_article.text()
            if not new_name:
                QMessageBox.information(self, "Ошибка", "Введите артикул нового товара", QMessageBox.Ok)
                return False
            if self.tree_id:
                query = "INSERT INTO product_article (Article, Name, Tree_Id) VALUES (%s, %s, %s)"
                sql_info = my_sql.sql_change(query, (self.le_article.text(), self.le_name.text(), self.tree_id))
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql добавление артикула", sql_info.msg, QMessageBox.Ok)
                    return False
                self.le_article.setWhatsThis(sql_info)
                self.id = sql_info
                self.save_change.remove("article")

        new_size = QInputDialog.getText(self, "Размер", "Введите размер")
        if not new_size[1]:
            return False
        else:
            new_size = new_size[0]
            query = "INSERT INTO product_article_size (Article_Id, Size) VALUES (%s, %s)"
            sql_info = my_sql.sql_change(query, (self.id, new_size))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql добавление размера", sql_info.msg, QMessageBox.Ok)
                return False
            self.cb_size.addItem(str(new_size), str(sql_info))
            self.gb_parametrs.setEnabled(True)
            self.get_start_sql_info()

    def ui_select_size(self):
        if self.save_change and self.show_complete:
            result = QMessageBox.question(self, "Внимание", "Сохранить информацию? (Иначе изменения не сохранятся)", QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.No)
            if result == 16384:
                self.save_sql()
        try:
            self.select_parametr_id = self.cb_parametrs.currentData()
        except:
            self.select_parametr_id = False
        self.get_start_sql_info()
        self.set_size_parametr()
        if self.tab_widget.currentIndex() == 2 and self.cb_parametrs.currentText() and self.cb_size.currentText():
            self.view_file_label()
        self.save_change = []  # Переменная для запоминания изменений

        if not self.dc_select:
            if self.cb_parametrs.count() == 0:
                self.set_enabled(False)  # закрываем поля
            else:
                self.set_enabled(True)

    def ui_dell_size(self):
        if self.cb_parametrs.count() != 0:
            QMessageBox.information(self, "Ошибка", "Сначало надо удалить все настройки размера!", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удаление", "Точно удалить размер???", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            size_id = self.cb_size.currentData()
            query = "DELETE FROM product_article_size WHERE Id = %s"
            sql_info = my_sql.sql_change(query, (size_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql удаление размера", sql_info.msg, QMessageBox.Ok)
                return False
            self.get_start_sql_info()
            self.set_start_sql_info()

    def ui_add_parametr(self):
        size_id = self.cb_size.currentData()
        if not size_id:
            QMessageBox.information(self, "Ошибка", "Добавте сначало размер!", QMessageBox.Ok)
            return False

        new_param = QInputDialog.getText(self, "Добавление параметра", "Введите название настройки товара")
        if not new_param[1] or new_param[0] == 0:
            return False
        else:
            new_param = new_param[0]
            query = "INSERT INTO product_article_parametrs (Product_Article_Size_Id, Name, `Show`) VALUES (%s, %s, %s)"
            sql_info = my_sql.sql_change(query, (size_id, new_param, 1))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql добавление параметра", sql_info.msg, QMessageBox.Ok)
                return False
            query = "INSERT INTO product_article_warehouse (Id_Article_Parametr, Value_In_Warehouse) VALUES (%s, %s)"
            sql_info_2 = my_sql.sql_change(query, (sql_info, 0))
            if "mysql.connector.errors" in str(type(sql_info_2)):
                QMessageBox.critical(self, "Ошибка sql добавление пустой позиции на склад", sql_info_2.msg, QMessageBox.Ok)
                return False
            self.cb_parametrs.addItem(str(new_param), str(sql_info))
            self.set_enabled(True)
            self.get_start_sql_info()

    def ui_change_parametr(self):
        try:
            param_name = self.cb_parametrs.currentText()
            param_id = self.cb_parametrs.currentData()
            curent_index = self.cb_parametrs.currentIndex()
        except:
            QMessageBox.information(self, "Ошибка", "Не выбран параметр артикула", QMessageBox.Ok)
            return False

        new_name = QInputDialog.getText(self, "изменение параметра", "Введите новое название настройки товара", text=param_name)
        if not new_name[1]:
            return False

        query = "UPDATE product_article_parametrs SET Name = %s WHERE Id = %s"
        sql_info = my_sql.sql_change(query, (new_name[0], param_id))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql изменения параметра", sql_info.msg, QMessageBox.Ok)
            return False

        self.cb_parametrs.setItemText(curent_index, new_name[0])

        self.get_start_sql_info()

    def ui_dell_parametr(self):
        try:
            param_id = self.cb_parametrs.currentData()
            curent_index = self.cb_parametrs.currentIndex()
        except:
            QMessageBox.information(self, "Ошибка", "Нет Id это не нормально!", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удаление", "Точно удалить настройку???", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            query = "SELECT Value_In_Warehouse FROM product_article_warehouse WHERE Id_Article_Parametr = %s"
            sql_info = my_sql.sql_select(query, (param_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql удаление параметра", sql_info.msg, QMessageBox.Ok)
                return False

            if sql_info[0][0] != 0:
                QMessageBox.information(self, "Ошибка склада", "На складе есть этот артикул. Удалить невозможно!", QMessageBox.Ok)
                return False

            sql_connect_transaction = my_sql.sql_start_transaction()

            query = "DELETE FROM product_article_warehouse WHERE Id_Article_Parametr = %s"
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (param_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql удаление параметра", sql_info.msg, QMessageBox.Ok)
                return False

            query = "DELETE FROM product_article_parametrs WHERE Id = %s"
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (param_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                QMessageBox.critical(self, "Ошибка sql удаление параметра", sql_info.msg, QMessageBox.Ok)
                return False

            my_sql.sql_commit_transaction(sql_connect_transaction)
            self.cb_parametrs.removeItem(curent_index)
            self.get_start_sql_info()

    def ui_show_parametr(self, cur_index):
        query = """UPDATE product_article_parametrs SET `Show` = %s WHERE Id = %s"""
        select_param_id = self.cb_parametrs.currentData()
        if select_param_id is None:
            return False
        if self.pb_show_param.text() == "Скрыть":
            show = 0
        else:
            show = 1
        sql_info = my_sql.sql_change(query, (show, select_param_id))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql изменения видимости параметра", sql_info.msg, QMessageBox.Ok)
            return False
        self.set_start_sql_info()
        self.set_size_parametr()

    def ui_select_parametr(self):
        if self.save_change and self.show_complete:
            result = QMessageBox.question(self, "Внимание", "Сохранить информацию? (Иначе изменения не сохранятся)", QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.No)
            if result == 16384:
                self.save_sql()
        try:
            self.select_parametr_id = self.cb_parametrs.currentData()
        except:
            self.select_parametr_id = False
        self.set_parametr_info()
        self.get_start_sql_info()
        if self.tab_widget.currentIndex() == 2 and self.cb_parametrs.currentText() and self.cb_size.currentText():
            self.view_file_label()
        self.save_change = []  # Переменная для запоминания изменений

    def ui_copy_parametr(self):
        self.copy_window = CopyParametr(self)
        self.copy_window.setModal(True)
        self.copy_window.show()
        id = self.copy_window.exec()
        if id < 0:
            return False
        else:
            for row in range(self.tw_operations.rowCount()):
                self.tw_operations.setRowHidden(row, True)
                for col in range(3):
                    self.tw_operations.item(row, col).setData(-1, "del")
            for row in range(self.tw_materials.rowCount()):
                self.tw_materials.setRowHidden(row, True)
                for col in range(4):
                    self.tw_materials.item(row, col).setData(-1, "del")
            self.set_parametr_info(id)
        self.calc()

    def ui_add_material(self):
        self.material_name = supply_material.MaterialName(self, True)
        self.material_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.material_name.show()

    def ui_dell_material(self):
        try:
            row = self.tw_materials.currentRow()
        except:
            QMessageBox.information(self, "Ошибка", "Выберете материал для удаления", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить материал?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            if self.tw_materials.item(row, 0).data(-1) == "new":
                self.tw_materials.removeRow(row)
            else:
                self.tw_materials.setRowHidden(row, True)
                for col in range(4):
                    self.tw_materials.item(row, col).setData(-1, "del")
            self.calc()

    def ui_change_material(self):
        try:
            row = self.tw_materials.currentRow()
        except:
            QMessageBox.information(self, "Ошибка", "Выберете материал для изменения", QMessageBox.Ok)
            return False
        if row == -1:
            QMessageBox.information(self, "Ошибка", "Выберете материал для изменения", QMessageBox.Ok)
            return False
        self.ui_double_click_material(row)

    def ui_double_click_material(self, row):
        item = self.tw_materials.item(row, 0)
        variant = "material" if (item.background().color().red() == 153) else "accessories"
        name = item.text()
        id_material = item.data(5)
        sql_id = item.data(-2)
        if item.data(-1) == "new":
            sql_status = "new"
        else:
            sql_status = "upd"
        value = float(self.tw_materials.item(row, 1).text())

        self.change_material = ChangeMaterial(variant)
        self.change_material.le_material.setText(name)
        self.change_material.le_material.setWhatsThis(str(id_material))
        self.change_material.sb_value.setValue(value)
        self.change_material.setModal(True)
        self.change_material.show()

        id = self.change_material.exec()

        if id == -1:
            return False

        value = self.change_material.sb_value.value()
        material = self.change_material.le_material.text()
        if variant == "material":
            query = """SELECT material_name.Id, material_supplyposition.Price
                    FROM material_name LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                    LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                    LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                    WHERE material_name.Name =%s AND material_balance.BalanceWeight > 0 ORDER BY material_supply.Data LIMIT 1"""

            sql_info = my_sql.sql_select(query, (material,))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql поиск цены материала", sql_info.msg, QMessageBox.Ok)
                return False
            elif not sql_info:
                query = "SELECT Id, 0 FROM material_name WHERE Name = %s"
                sql_info = my_sql.sql_select(query, (material,))
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql поиск ID материала", sql_info.msg, QMessageBox.Ok)
                    return False
            brush = QBrush(QColor(153, 221, 255, 255))
        else:
            query = """SELECT accessories_name.Id, accessories_supplyposition.Price
                    FROM accessories_name LEFT JOIN accessories_supplyposition ON accessories_name.Id = accessories_supplyposition.accessories_NameId
                    LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.accessories_SupplyPositionId
                    LEFT JOIN accessories_supply ON accessories_supplyposition.accessories_SupplyId = accessories_supply.Id
                    WHERE accessories_name.Name = %s AND accessories_balance.BalanceValue > 0 ORDER BY accessories_supply.Data LIMIT 1"""

            sql_info = my_sql.sql_select(query, (material,))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql поиск цены аксесуара", sql_info.msg, QMessageBox.Ok)
                return False
            elif not sql_info:
                query = "SELECT Id, 0 FROM accessories_name WHERE Name = %s"
                sql_info = my_sql.sql_select(query, (material,))
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql поиск ID аксесуара", sql_info.msg, QMessageBox.Ok)
                    return False
            brush = QBrush(QColor(252, 163, 255, 255))

        item = QTableWidgetItem(material)
        item.setData(5, sql_info[0][0])
        item.setData(-1, sql_status)
        item.setData(-2, sql_id)
        item.setBackground(brush)
        self.tw_materials.setItem(row, 0, item)
        item = QTableWidgetItem(str(value))
        item.setData(5, sql_info[0][0])
        item.setData(-1, sql_status)
        item.setData(-2, sql_id)
        item.setBackground(brush)
        self.tw_materials.setItem(row, 1, item)
        item = QTableWidgetItem(str(sql_info[0][1]))
        item.setData(5, sql_info[0][0])
        item.setData(-1, sql_status)
        item.setData(-2, sql_id)
        item.setBackground(brush)
        self.tw_materials.setItem(row, 2, item)
        item = QTableWidgetItem(str(round(value * float(sql_info[0][1]), 4)))
        item.setData(5, sql_info[0][0])
        item.setData(-1, sql_status)
        item.setData(-2, sql_id)
        item.setBackground(brush)
        self.tw_materials.setItem(row, 3, item)
        self.calc()

    def ui_add_accessories(self):
        self.accessories_name = supply_accessories.AccessoriesName(self, True)
        self.accessories_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.accessories_name.show()

    def ui_add_operation(self):
        self.operation_name = operation.OperationList(self, True)
        self.operation_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.operation_name.show()

    def ui_change_operation(self):
        try:
            row = self.tw_operations.currentRow()
            self.ui_double_click_operation(row)
        except:
            QMessageBox.information(self, "Ошибка", "Выберете операцию для изменения", QMessageBox.Ok)
            return False

    def ui_dell_operation(self):
        try:
            row = self.tw_operations.currentRow()
        except:
            QMessageBox.information(self, "Ошибка", "Выберете операцию для удаления", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить операцию?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            if self.tw_operations.item(row, 0).data(-1) == "new":
                self.tw_operations.removeRow(row)
            else:
                self.tw_operations.setRowHidden(row, True)
                for col in range(3):
                    self.tw_operations.item(row, col).setData(-1, "del")

            for row in range(row + 1, self.tw_operations.rowCount()):
                for col in range(3):
                    self.tw_operations.item(row, col).setData(-1, "upd")
            self.calc()

    def ui_up_operation(self):
        try:
            select_row = self.tw_operations.currentRow()
        except:
            QMessageBox.information(self, "Ошибка", "Выберите операцию которую хотите передвинуть", QMessageBox.Ok)
            return False

        if select_row == 0:
            QMessageBox.information(self, "Ошибка", "Выше уже некуда", QMessageBox.Ok)
            return False

        for col in range(3):
            up_item = self.tw_operations.item(select_row, col)
            down_item = self.tw_operations.item(select_row - 1, col)

            try:
                set_up_item = QTableWidgetItem(up_item.text())
                set_up_item.setData(5, up_item.data(5))
                if up_item.data(-1) == "set" or up_item.data(-1) == "upd":
                    set_up_item.setData(-1, "upd")
                    set_up_item.setData(-2, up_item.data(-2))
                elif up_item.data(-1) == "new":
                    set_up_item.setData(-1, "new")

                set_down_item = QTableWidgetItem(down_item.text())
                set_down_item.setData(5, down_item.data(5))
                if down_item.data(-1) == "set" or down_item.data(-1) == "upd":
                    set_down_item.setData(-1, "upd")
                    set_down_item.setData(-2, down_item.data(-2))
                elif down_item.data(-1) == "new":
                    set_down_item.setData(-1, "new")

                self.tw_operations.setItem(select_row - 1, col, set_up_item)
                self.tw_operations.setItem(select_row, col, set_down_item)
                self.tw_operations.setCurrentCell(select_row - 1, 0)
            except:
                QMessageBox.information(self, "Ошибка", "Выберите операцию которую хотите передвинуть", QMessageBox.Ok)
                return False

    def ui_down_operation(self):
        try:
            select_row = self.tw_operations.currentRow()
        except:
            QMessageBox.information(self, "Ошибка", "Выберите операцию которую хотите передвинуть", QMessageBox.Ok)
            return False

        if select_row == self.tw_operations.rowCount() - 1:
            QMessageBox.information(self, "Ошибка", "Ниже уже некуда", QMessageBox.Ok)
            return False

        for col in range(3):
            try:
                down_item = self.tw_operations.item(select_row, col)
                up_item = self.tw_operations.item(select_row + 1, col)

                set_down_item = QTableWidgetItem(down_item.text())
                set_down_item.setData(5, down_item.data(5))
                if down_item.data(-1) == "set" or down_item.data(-1) == "upd":
                    set_down_item.setData(-1, "upd")
                    set_down_item.setData(-2, down_item.data(-2))
                elif down_item.data(-1) == "new":
                    set_down_item.setData(-1, "new")

                set_up_item = QTableWidgetItem(up_item.text())
                set_up_item.setData(5, up_item.data(5))
                if up_item.data(-1) == "set" or up_item.data(-1) == "upd":
                    set_up_item.setData(-1, "upd")
                    set_up_item.setData(-2, up_item.data(-2))
                elif up_item.data(-1) == "new":
                    set_up_item.setData(-1, "new")

                self.tw_operations.setItem(select_row + 1, col, set_down_item)
                self.tw_operations.setItem(select_row, col, set_up_item)
                self.tw_operations.setCurrentCell(select_row + 1, 0)
            except:
                QMessageBox.information(self, "Ошибка", "Выберите операцию которую хотите передвинуть", QMessageBox.Ok)
                return False

    def ui_double_click_operation(self, row):
        item = self.tw_operations.item(row, 0)
        self.change_operation = ChangeOperation()
        self.change_operation.le_operation.setText(item.text())
        self.change_operation.le_operation.setWhatsThis(str(item.data(5)))
        self.change_operation.setModal(True)
        self.change_operation.show()
        id = self.change_operation.exec()
        if id <= 0:
            return False
        if not self.change_operation.new_operation:
            return False

        elif id == item.data(5):
            item.setText(self.change_operation.new_operation[1])
        else:
            sql_id = item.data(-2)
            if item.data(-1) == "new":
                sql_status = "new"
            else:
                sql_status = "upd"
            item = self.change_operation.new_operation
            for col in range(1, len(item)):
                new_item = QTableWidgetItem(item[col])
                new_item.setData(5, item[0])
                new_item.setData(-1, sql_status)
                new_item.setData(-2, sql_id)
                self.tw_operations.setItem(row, col - 1, new_item)
        self.calc()

    def ui_print(self):
        head = "%s (%s) %s   %s" % (self.le_article.text(), self.cb_size.currentText(), self.cb_parametrs.currentText(), self.tw_materials.text())

        up_html = """
          <table>
          <caption>#caption#</caption>
          <tr>
          <th>Название клиента</th><th>Штрих-код</th><th>Код клиента</th><th>PCB</th>
          </tr>
          <tr>
          <td>#cl_name#</td><td>#barcode#</td><td>#cl_code#</td><td>#pcb#</td>
          </tr>
          <tr>
          <th>Цена</th><th>НДС</th><th>Цена без НДС</th><th>Себестоймость</th>
          </tr>
          <tr>
          <td>#price#</td><td>#nds#</td><td>#price_no_nds#</td><td>#sibestoimost#</td>
          </tr>
          </table>
          <table>
          <tr>
          <th>Описание товара</th>
          </tr>
          <tr>
          <td>#product_note#</td>
          </tr>
          </table>
          <table>
          <tr>
          <th>Описание кроя</th>
          </tr>
          <tr>
          <td>#cut_note#</td>
          </tr>
          </table>
          """

        if self.rb_nds_1.isChecked():
            nds = 18
        else:
            nds = 10

        up_html = up_html.replace("#caption#", head)
        up_html = up_html.replace("#cl_name#", self.le_client_name.text())
        up_html = up_html.replace("#barcode#", self.le_barcode.text())
        up_html = up_html.replace("#cl_code#", self.le_client_code.text())
        up_html = up_html.replace("#pcb#", self.le_in_on_place.text())
        up_html = up_html.replace("#price#", self.le_price.text())
        up_html = up_html.replace("#nds#", str(nds))
        up_html = up_html.replace("#price_no_nds#", str(self.sb_no_nds.value()))
        up_html = up_html.replace("#sibestoimost#", self.le_cost_price.text())
        up_html = up_html.replace("#product_note#", self.pe_product_note.toPlainText())
        up_html = up_html.replace("#cut_note#", self.pe_cut_note.toPlainText())

        html = table_to_html.tab_html(self.tw_operations, up_template=up_html)
        html = table_to_html.tab_html(self.tw_materials, up_template=html)

        self.print_class = print_qt.PrintHtml(self, html)

    def ui_calc_nds(self):
        try:
            price = float(self.le_price.text().replace(",", "."))
        except:
            price = 0
        if self.rb_nds_1.isChecked():
            nds = 18
        else:
            nds = 10
        self.sb_no_nds.setValue(round(price - (price * nds) / (100 + nds), 4))

    def ui_acc(self):

        if not self.dc_select:
            if self.save_sql():
                self.close()
                self.destroy()
                self.main.set_table_info()
        else:
            if self.rb_nds_1.isChecked():
                nds = 18
            else:
                nds = 10
            article_info = {"article_id": self.le_article.whatsThis(),
                            "article": self.le_article.text(),
                            "size": self.cb_size.currentText(),
                            "parametr": self.cb_parametrs.currentText(),
                            "parametr_id": self.cb_parametrs.currentData(),
                            "price": self.le_price.text(),
                            "in on place": self.le_in_on_place.text(),
                            "nds": nds,
                            "client_Name": self.le_client_name.text()}
            self.main.of_tree_select_article(article_info)
            self.close()
            self.destroy()

    def ui_cancel(self):
        if self.save_change and self.access_save_sql:
            result = QMessageBox.question(self, "Сохранить?", "Сохранить изменение перед выходом?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == 16384:
                self.save_sql()
        self.close()
        self.destroy()
        if not self.dc_select:
            self.main.ui_update_table()

    def ui_save_change_article(self):
        if "article" not in self.save_change:
            self.save_change.append("article")

    def ui_save_change_parametr(self):
        if "parametr" not in self.save_change:
            self.save_change.append("parametr")

    def ui_save_change_material(self):
        if "material" not in self.save_change:
            self.save_change.append("material")

    def ui_save_change_operation(self):
        if "operation" not in self.save_change:
            self.save_change.append("operation")

    def ui_check_show(self):
        self.set_size_parametr()

    def ui_change_curent(self, curent):
        if curent == 2:
            self.view_file_label()

    def ui_print_label(self, item):
        data = {"article": self.le_article.text(),
                "article_size": self.cb_size.currentText(),
                "article_parametr": self.cb_parametrs.currentText()}

        query = 'SELECT `Values` FROM program_settings_path WHERE Name = "Путь корень бирки"'
        info_sql = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(info_sql)):
                    QMessageBox.critical(self, "Ошибка sql", info_sql.msg, QMessageBox.Ok)
                    return False

        path = info_sql[0][0] + "/" + self.le_article.text() + " " + self.cb_size.currentText() + " " + self.cb_parametrs.currentText() + "/" + item.text()
        self.print_label = print_label.LabelSettings(path, data)
        self.print_label.setWindowModality(True)
        self.print_label.show()

    def key_up(self):
        index = self.cb_size.currentIndex()
        if index == 0:
            self.cb_size.setCurrentIndex(self.cb_size.count()-1)
        else:
            self.cb_size.setCurrentIndex(index-1)

    def key_down(self):
        index = self.cb_size.currentIndex()
        if index == self.cb_size.count()-1:
            self.cb_size.setCurrentIndex(0)
        else:
            self.cb_size.setCurrentIndex(index+1)

    def key_left(self):
        index = self.cb_parametrs.currentIndex()
        if index == self.cb_parametrs.count()-1:
            self.cb_parametrs.setCurrentIndex(0)
        else:
            self.cb_parametrs.setCurrentIndex(index+1)

    def key_right(self):
        index = self.cb_parametrs.currentIndex()
        if index == 0:
            self.cb_parametrs.setCurrentIndex(self.cb_parametrs.count()-1)
        else:
            self.cb_parametrs.setCurrentIndex(index-1)

    def save_sql(self):

        try:
            int(self.le_in_on_place.text())
        except ValueError:
            QMessageBox.information(self, "Ошибка PCB", "Не верное значение поля 'В одном месте'", QMessageBox.Ok)
            return False

        try:
            float(self.le_price.text())
        except ValueError:
            QMessageBox.information(self, "Ошибка Цены", "Не верное значение поля 'Цена'", QMessageBox.Ok)
            return False

        if not self.cb_parametrs.currentText():
            QMessageBox.information(self, "Ошибка названия", "Недопустимое название параметра", QMessageBox.Ok)
            return False

        if "article" in self.save_change:
            query = """UPDATE product_article SET Article = %s, Name = %s WHERE Id = %s"""
            sql_info = my_sql.sql_change(query, (self.le_article.text(), self.le_name.text(), self.id))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql изменения артикула", sql_info.msg, QMessageBox.Ok)
                return False

        if not self.select_parametr_id:
            parametr_id = self.cb_parametrs.currentData()
            if not parametr_id:
                QMessageBox.critical(self, "Ошибка", "Нету id у параметра, это не нормально позовите администратора", QMessageBox.Ok)
                return False
        else:
            parametr_id = self.select_parametr_id

        if "parametr" in self.save_change:
            query = """UPDATE product_article_parametrs SET Client_Name = %s, Barcode = %s,
                      Client_code = %s, In_On_Place = %s, Price = %s, Product_Note = %s, Cut_Note = %s, NDS = %s WHERE Id = %s"""
            if self.rb_nds_1.isChecked():
                nds = 18
            else:
                nds = 10
            sql_param = (self.le_client_name.text(), self.le_barcode.text(), self.le_client_code.text(), self.le_in_on_place.text().replace(",", "."),
                         self.le_price.text().replace(",", "."), self.pe_product_note.toPlainText(), self.pe_cut_note.toPlainText(), nds, parametr_id)
            sql_info = my_sql.sql_change(query, sql_param)
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql изменения параметров", sql_info.msg, QMessageBox.Ok)
                return False

        if "operation" in self.save_change:
            position_operation = 1
            for row in range(self.tw_operations.rowCount()):
                table_item = self.tw_operations.item(row, 0)
                if self.tw_operations.isRowHidden(row):
                    if table_item.data(-1) == "del" and table_item.data(-2):
                        query = "DELETE FROM product_article_operation WHERE Id = %s"
                        sql_info = my_sql.sql_change(query, (table_item.data(-2),))
                        if "mysql.connector.errors" in str(type(sql_info)):
                            QMessageBox.critical(self, "Ошибка sql удаление операции", sql_info.msg, QMessageBox.Ok)
                            return False

                elif table_item.data(-1) == "new":
                    query = "INSERT INTO product_article_operation (Product_Article_Parametrs_Id, Operation_Id, Position) VALUES (%s, %s, %s)"
                    sql_info = my_sql.sql_change(query, (parametr_id, table_item.data(5), position_operation))
                    position_operation += 1
                    if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql добавление операции", sql_info.msg, QMessageBox.Ok)
                        return False

                elif table_item.data(-1) == "upd" and table_item.data(-2):
                    query = "UPDATE product_article_operation SET Operation_Id = %s, Position = %s WHERE Id = %s"
                    sql_info = my_sql.sql_change(query, (table_item.data(5), position_operation, table_item.data(-2)))
                    position_operation += 1
                    if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql добавление операции", sql_info.msg, QMessageBox.Ok)
                        return False

                elif table_item.data(-1) == "set":
                    position_operation += 1

                else:
                    QMessageBox.critical(self, "Ошибка", "Строка операций не подошла в if при сохранении, это не нормально позовите администратора", QMessageBox.Ok)
                    return False

        if "material" in self.save_change:
            for row in range(self.tw_materials.rowCount()):
                table_item = self.tw_materials.item(row, 1)
                color_r = table_item.background().color().red()
                if color_r == 153:
                    material_id = table_item.data(5)
                    accessories_id = None
                elif color_r == 252:
                    material_id = None
                    accessories_id = table_item.data(5)
                else:
                    QMessageBox.critical(self, "Ошибка", "Не подошел цвет материала в if, это не нормально позовите администратора", QMessageBox.Ok)
                    return False

                if self.tw_materials.isRowHidden(row):
                    if table_item.data(-1) == "del" and table_item.data(-2):
                        query = "DELETE FROM product_article_material WHERE Id = %s"
                        sql_info = my_sql.sql_change(query, (table_item.data(-2),))
                        if "mysql.connector.errors" in str(type(sql_info)):
                            QMessageBox.critical(self, "Ошибка sql удаление материала", sql_info.msg, QMessageBox.Ok)
                            return False
                    else:
                        QMessageBox.critical(self, "Ошибка", "Нету id у материала при удалении, это не нормально позовите администратора", QMessageBox.Ok)
                        return False

                elif table_item.data(-1) == "new":
                    query = "INSERT INTO product_article_material (Product_Article_Parametrs_Id, Material_Id, Accessories_Id, Value) VALUES (%s, %s, %s, %s)"
                    sql_info = my_sql.sql_change(query, (parametr_id, material_id, accessories_id, table_item.text()))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql добавлении материала", sql_info.msg, QMessageBox.Ok)
                        return False

                elif table_item.data(-1) == "upd" and table_item.data(-2):
                    query = "UPDATE product_article_material SET Material_Id = %s, Accessories_Id = %s, Value = %s WHERE Id = %s"
                    sql_info = my_sql.sql_change(query, (material_id, accessories_id, table_item.text(), table_item.data(-2)))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql изменение материала", sql_info.msg, QMessageBox.Ok)
                        return False

                elif table_item.data(-1) == "set":
                    pass

                else:
                    QMessageBox.critical(self, "Ошибка", "Строка материала не подошла в if при сохранении, это не нормально позовите администратора", QMessageBox.Ok)
                    return False

        self.save_change = []
        return True

    def set_enabled(self, en_bool):
        self.le_client_name.setEnabled(en_bool)
        self.le_barcode.setEnabled(en_bool)
        self.le_client_code.setEnabled(en_bool)
        self.le_in_on_place.setEnabled(en_bool)
        self.le_price.setEnabled(en_bool)
        self.pe_product_note.setEnabled(en_bool)
        self.pe_cut_note.setEnabled(en_bool)
        self.tab_widget.setEnabled(en_bool)
        self.pb_acc.setEnabled(en_bool)

    def set_all_enabled(self, en_bool):
        self.le_client_name.setEnabled(en_bool)
        self.le_barcode.setEnabled(en_bool)
        self.le_client_code.setEnabled(en_bool)
        self.le_in_on_place.setEnabled(en_bool)
        self.le_price.setEnabled(en_bool)
        self.pe_product_note.setEnabled(en_bool)
        self.pe_cut_note.setEnabled(en_bool)
        self.toolButton_7.setEnabled(en_bool)
        self.toolButton_11.setEnabled(en_bool)
        self.pb_dell_param.setEnabled(en_bool)
        self.pb_show_param.setEnabled(en_bool)
        self.toolButton_10.setEnabled(en_bool)
        self.toolButton_9.setEnabled(en_bool)
        self.toolButton_2.setEnabled(en_bool)
        self.toolButton_3.setEnabled(en_bool)
        self.toolButton.setEnabled(en_bool)
        self.pb_up.setEnabled(en_bool)
        self.pb_down.setEnabled(en_bool)
        self.toolButton_4.setEnabled(en_bool)
        self.toolButton_8.setEnabled(en_bool)
        self.toolButton_5.setEnabled(en_bool)
        self.toolButton_6.setEnabled(en_bool)
        self.tw_materials.setEnabled(en_bool)
        self.tw_operations.setEnabled(en_bool)

    def calc(self):
        price_all_operations = 0.0
        price_all_material = 0.0
        for row in range(self.tw_operations.rowCount()):
            if not self.tw_operations.isRowHidden(row):
                price_all_operations += float(self.tw_operations.item(row, 1).text())

        for row in range(self.tw_materials.rowCount()):
            if not self.tw_materials.isRowHidden(row):
                price_all_material += float(self.tw_materials.item(row, 3).text())

        all_price = price_all_material + price_all_operations
        self.le_cost_price.setText(str(round(all_price, 4)))

    def view_file_label(self):
        if self.cb_parametrs.currentText() and self.cb_size.currentText():
            dir_name = self.le_article.text() + " " + self.cb_size.currentText() + " " + self.cb_parametrs.currentText()
            self.inspection_files(dir_name, "Путь корень бирки")

    def inspection_path(self, dir_name, sql_dir_name):  # Находим путь работника
        if not hasattr(self, 'path_work'):
            query = 'SELECT `Values` FROM program_settings_path WHERE Name = "%s"' % sql_dir_name
            info_sql = my_sql.sql_select(query)
            if "mysql.connector.errors" in str(type(info_sql)):
                        QMessageBox.critical(self, "Ошибка sql", info_sql.msg, QMessageBox.Ok)
                        return False
            self.path_wor = info_sql[0][0]
            if not path.isdir("%s/%s" % (self.path_wor, dir_name)):
                try:
                    mkdir("%s/%s" % (self.path_wor, dir_name))
                    return "%s/%s" % (self.path_wor, dir_name)
                except:
                    QMessageBox.critical(self, "Ошибка файлы", "Нет доступа к корневому диалогу, файлы недоступны", QMessageBox.Ok)
                    return False
            else:
                return "%s/%s" % (self.path_wor, dir_name)

    def inspection_files(self, dir_name, sql_dir_name):   # Проверяем файлы и даем иконки
        self.path = self.inspection_path(dir_name, sql_dir_name)
        if self.path:
            self.lw_label.clear()
            files = listdir("%s/%s" % (self.path_wor, dir_name))
            for file in files:
                if "~" not in file:
                    r = path.splitext(file)  # Получаем название и расширение
                    if "xlsx" in r[1][1:] or "xlsm" in r[1] or "xls" in r[1] or "xlt" in r[1]:
                        ico = "xlsx"
                    elif "xml" in r[1][1:] or "docx" in r[1] or "doc" in r[1] or "docm" in r[1]:
                        ico = "xml"
                    elif "png" in r[1].lower() or "jpg" in r[1] or "jpeg" in r[1] or "jpe" in r[1] or "gif" in r[1] or "bmp" in r[1]:
                        ico = "image"
                    elif "pdf" in r[1]:
                        ico = "pdf"
                    elif "btw" in r[1]:
                        ico = "btw"
                    else:
                        ico = "other"

                    list_item = QListWidgetItem(r[0] + r[1])
                    list_item.setIcon(QIcon(getcwd() + "/images/%s.ico" % ico))
                    self.lw_label.addItem(list_item)

    def of_tree_select_operation(self, item):
        self.tw_operations.insertRow(self.tw_operations.rowCount())
        for col in range(1, len(item)):
            new_item = QTableWidgetItem(item[col])
            new_item.setData(5, item[0])
            new_item.setData(-1, "new")
            self.tw_operations.setItem(self.tw_operations.rowCount() - 1, col - 1, new_item)
        self.calc()

    def of_list_material_name(self, material):  # Внешняя функция добавления материала
        query = """SELECT material_name.Id, material_supplyposition.Price
                    FROM material_name LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                    LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                    LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                    WHERE material_name.Id =%s AND material_balance.BalanceWeight > 0 ORDER BY material_supply.Data LIMIT 1"""

        value = QInputDialog.getDouble(self, "Количество", "Введите требуемое количество матриала", decimals=4)
        if value[0] == 0 or value[1] == False:
            return False
        value = value[0]

        sql_info = my_sql.sql_select(query, (material[0],))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql поиск цены материала", sql_info.msg, QMessageBox.Ok)
            return False
        elif not sql_info:
            sql_info = ((material[0], "0"), )

        self.tw_materials.insertRow(self.tw_materials.rowCount())
        item = QTableWidgetItem(material[1])
        item.setData(5, sql_info[0][0])
        item.setData(-1, "new")
        item.setBackground(QBrush(QColor(153, 221, 255, 255)))
        self.tw_materials.setItem(self.tw_materials.rowCount() - 1, 0, item)
        item = QTableWidgetItem(str(value))
        item.setData(5, sql_info[0][0])
        item.setData(-1, "new")
        item.setBackground(QBrush(QColor(153, 221, 255, 255)))
        self.tw_materials.setItem(self.tw_materials.rowCount() - 1, 1, item)
        item = QTableWidgetItem(str(sql_info[0][1]))
        item.setData(5, sql_info[0][0])
        item.setData(-1, "new")
        item.setBackground(QBrush(QColor(153, 221, 255, 255)))
        self.tw_materials.setItem(self.tw_materials.rowCount() - 1, 2, item)
        item = QTableWidgetItem(str(round(value * float(sql_info[0][1]), 4)))
        item.setData(5, sql_info[0][0])
        item.setData(-1, "new")
        item.setBackground(QBrush(QColor(153, 221, 255, 255)))
        self.tw_materials.setItem(self.tw_materials.rowCount() - 1, 3, item)
        self.calc()

    def of_list_accessories_name(self, accessories):
        query = """SELECT accessories_name.Id, accessories_supplyposition.Price
                    FROM accessories_name LEFT JOIN accessories_supplyposition ON accessories_name.Id = accessories_supplyposition.accessories_NameId
                    LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.accessories_SupplyPositionId
                    LEFT JOIN accessories_supply ON accessories_supplyposition.accessories_SupplyId = accessories_supply.Id
                    WHERE accessories_name.Id = %s AND accessories_balance.BalanceValue > 0 ORDER BY accessories_supply.Data LIMIT 1"""

        value = QInputDialog.getDouble(self, "Количество", "Введите требуемое количество аксесуара", decimals=4)
        if value[0] == 0 or value[1] == False:
            return False
        value = value[0]

        sql_info = my_sql.sql_select(query, (accessories[0],))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql поиск цены аксесуара", sql_info.msg, QMessageBox.Ok)
            return False
        elif not sql_info:
            sql_info = ((accessories[0], "0"), )

        self.tw_materials.insertRow(self.tw_materials.rowCount())
        item = QTableWidgetItem(accessories[1])
        item.setData(5, sql_info[0][0])
        item.setData(-1, "new")
        item.setBackground(QBrush(QColor(252, 163, 255, 255)))
        self.tw_materials.setItem(self.tw_materials.rowCount() - 1, 0, item)
        item = QTableWidgetItem(str(value))
        item.setData(5, sql_info[0][0])
        item.setData(-1, "new")
        item.setBackground(QBrush(QColor(252, 163, 255, 255)))
        self.tw_materials.setItem(self.tw_materials.rowCount() - 1, 1, item)
        item = QTableWidgetItem(str(sql_info[0][1]))
        item.setData(5, sql_info[0][0])
        item.setData(-1, "new")
        item.setBackground(QBrush(QColor(252, 163, 255, 255)))
        self.tw_materials.setItem(self.tw_materials.rowCount() - 1, 2, item)
        item = QTableWidgetItem(str(round(value * float(sql_info[0][1]), 4)))
        item.setData(5, sql_info[0][0])
        item.setData(-1, "new")
        item.setBackground(QBrush(QColor(252, 163, 255, 255)))
        self.tw_materials.setItem(self.tw_materials.rowCount() - 1, 3, item)
        self.calc()


class ArticleFilter(QDialog, article_filter):
    def __init__(self, main):
        super(ArticleFilter, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        self.access()

    def access(self):
        for item in User().access_list(self.__class__.__name__):
            a = getattr(self, item["atr1"])
            if item["atr2"]:
                a = getattr(a, item["atr2"])

            if item["value"]:
                a(item["value"])
            else:
                a()

    def ui_acc(self):
        where = ""

        # Блок условий артикула
        if self.le_article.text() != '':
            where = self.add_filter(where, "(product_article.Article LIKE '%s')" % ("%" + self.le_article.text() + "%", ))

        # Блок условий названия артикула
        if self.le_article_name.text() != '':
            where = self.add_filter(where, "(product_article.Name LIKE '%s')" % ("%" + self.le_article_name.text() + "%",))

        # Блок условий цены
        # if self.le_article_price.isChecked():
        #     sql_date = "(product_article_parametrs.Price >= '%s' AND product_article_parametrs.Price <= '%s')" % \
        #                (self.le_article_price_from.text(), self.le_article_price_to.text())
        #     where = self.add_filter(where, sql_date)

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


class ChangeOperation(QDialog, article_change_operation_class):
    def __init__(self):
        super(ChangeOperation, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.access()
        self.new_operation = None

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

    def ui_view_list_operation(self):
        self.operation_name = operation.OperationList(self, True, int(self.le_operation.whatsThis()))
        self.operation_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.operation_name.show()

    def ui_acc(self):
        id = self.le_operation.whatsThis()
        self.done(int(id))
        self.close()
        self.destroy()

    def ui_cancel(self):
        self.done(-1)
        self.close()
        self.destroy()

    def of_tree_select_operation(self, item):
        self.new_operation = item
        self.le_operation.setText(item[1])
        self.le_operation.setWhatsThis(str(item[0]))


class ChangeMaterial(QDialog, article_change_material_class):
    def __init__(self, variant):
        super(ChangeMaterial, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.variant = variant

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

    def ui_view_list_material(self):
        if self.variant == "material":
            self.material_name = supply_material.MaterialName(self, True)
            self.material_name.setWindowModality(QtCore.Qt.ApplicationModal)
            self.material_name.show()
        elif self.variant == "accessories":
            self.accessories_name = supply_accessories.AccessoriesName(self, True)
            self.accessories_name.setWindowModality(QtCore.Qt.ApplicationModal)
            self.accessories_name.show()

    def ui_acc(self):
        id = self.le_material.whatsThis()
        self.done(int(id))
        self.close()
        self.destroy()

    def ui_cancel(self):
        self.done(-1)
        self.close()
        self.destroy()

    def of_list_material_name(self, item):
        self.le_material.setText(item[1])
        self.le_material.setWhatsThis(str(1))

    def of_list_accessories_name(self, item):
        self.le_material.setText(item[1])
        self.le_material.setWhatsThis(str(1))


class CopyParametr(QDialog, article_copy_parametr):
    def __init__(self, main):
        super(CopyParametr, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.main = main
        self.set_size_parametr()

        self.access()

    def access(self):
        for item in User().access_list(self.__class__.__name__):
            a = getattr(self, item["atr1"])
            if item["atr2"]:
                a = getattr(a, item["atr2"])

            if item["value"]:
                a(item["value"])
            else:
                a()

    def set_size_parametr(self):
        self.cb_size.clear()
        for size in self.main.article_size:
            self.cb_size.addItem(size[3], size[2])

    def set_size(self):
        self.cb_parametrs.clear()
        select_size_id = self.cb_size.currentData()

        if hasattr(self.main, 'article_parametrs'):
            for param in self.main.article_parametrs:
                if select_size_id == param[0] and param[10] == 1:
                    self.cb_parametrs.addItem(param[2], param[1])
                elif select_size_id == param[0] and param[10] == 0:
                    icon = QIcon(getcwd() + "/images/eye.ico")
                    self.cb_parametrs.addItem(icon, param[2], param[1])

    def set_parametr(self):
        self.le_client_name.clear()
        self.le_barcode.clear()
        self.le_client_code.clear()
        self.le_in_on_place.setText("0")
        self.le_price.setText("0")
        self.pe_product_note.clear()
        self.pe_cut_note.clear()
        select_param_id = self.cb_parametrs.currentData()
        if select_param_id is None:
            return False
        for param_info in self.main.article_parametrs:
            if select_param_id == param_info[1]:
                self.le_client_name.setText(param_info[3])
                self.le_barcode.setText(param_info[4])
                self.le_client_code.setText(param_info[5])
                in_on_place = param_info[6] if (param_info[6] is not None) else "0"
                self.le_in_on_place.setText(str(in_on_place))
                price = param_info[7] if (param_info[7] is not None) else "0"
                self.le_price.setText(str(price))
                self.pe_product_note.appendPlainText(param_info[8])
                self.pe_cut_note.appendPlainText(param_info[9])
                break

    def ui_acc(self):
        id = self.cb_parametrs.currentData()
        self.done(int(id))
        self.close()
        self.destroy()

    def ui_cancel(self):
        self.done(-1)
        self.close()
        self.destroy()
