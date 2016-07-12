from os import getcwd
from form.templates import tree
from form import operation, material_provider, accessories_provider
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QMainWindow, QInputDialog, QTableWidgetItem
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from function import my_sql

article_class = loadUiType(getcwd() + '/ui/article.ui')[0]
article_change_operation_class = loadUiType(getcwd() + '/ui/article_change_operation.ui')[0]
article_change_material_class = loadUiType(getcwd() + '/ui/article_change_material.ui')[0]
article_copy_parametr = loadUiType(getcwd() + '/ui/article_copy_parametr.ui')[0]


class ArticleList(tree.TreeList):
    def set_settings(self):
        self.setWindowTitle("Список артикулов")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(167, 183, 255);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Артикул", 70), ("Название", 150), ("Размеры", 120))

        self.query_tree_select = "SELECT Id, Parent_Id, Name FROM product_tree"
        self.query_tree_add = "INSERT INTO product_tree (Parent_Id, Name) VALUES (%s, %s)"
        self.query_tree_change = "UPDATE product_tree SET Name = %s WHERE Id = %s"
        self.query_tree_del = "DELETE FROM product_tree WHERE Id = %s"

        #  нулевой элемент должен быть ID а первый Parent_ID (ID категории)
        self.query_table_select = """SELECT product_article.Id, product_article.Tree_Id, product_article.Article, product_article.Name,
                                    GROUP_CONCAT(product_article_size.Size ORDER BY product_article_size.Size) FROM product_article
                                    LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id
                                    GROUP BY product_article.Article"""
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


class Article(QMainWindow, article_class):
    def __init__(self, main, id=False, tree_id=False):
        super(Article, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.main = main
        self.id = id
        self.tree_id = tree_id
        self.view_show = False
        self.show_complete = False  # Переменная показывает что страница загружена
        self.save_change = []  # Переменная для запоминания изменений
        self.pb_up.setIcon(QIcon(getcwd() + "/images/up.ico"))
        self.pb_down.setIcon(QIcon(getcwd() + "/images/down.ico"))
        self.set_start_settings()
        self.show_complete = True  # Переменная показывает что страница загружена

    def set_start_settings(self):
        # Ширина материалов
        self.tw_materials.horizontalHeader().resizeSection(0, 240)
        self.tw_materials.horizontalHeader().resizeSection(1, 80)
        self.tw_materials.horizontalHeader().resizeSection(2, 80)
        self.tw_materials.horizontalHeader().resizeSection(3, 80)
        # Ширина операций
        self.tw_operations.horizontalHeader().resizeSection(0, 250)
        self.tw_operations.horizontalHeader().resizeSection(1, 80)
        self.tw_operations.horizontalHeader().resizeSection(2, 80)

        if not self.id and self.tree_id:  # Если новый артикул
            self.set_enabled(False)  # закрываем поля
            self.gb_parametrs.setEnabled(False)

        if self.id:
            self.set_start_sql_info()

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
                  FROM product_article LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id WHERE product_article.Id = %s"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения размера", sql_info.msg, QMessageBox.Ok)
            return False
        self.article_size = sql_info

        query = """SELECT product_article_parametrs.Product_Article_Size_Id, product_article_parametrs.Id, product_article_parametrs.Name,
                product_article_parametrs.Client_Name, product_article_parametrs.Barcode, product_article_parametrs.Client_code, product_article_parametrs.In_On_Place,
                product_article_parametrs.Price, product_article_parametrs.Product_Note, product_article_parametrs.Cut_Note, product_article_parametrs.`Show`
                FROM product_article LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id
                LEFT JOIN product_article_parametrs ON product_article_size.Id = product_article_parametrs.Product_Article_Size_Id WHERE product_article.Id = %s"""
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
                    LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                    LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                    WHERE product_article.Id = %s AND product_article_material.Material_Id IS NOT NULL GROUP BY product_article_material.Id"""
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
                    LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.accessories_SupplyPositionId
                    LEFT JOIN accessories_supply ON accessories_supplyposition.Accessories_SupplyId = accessories_supply.Id
                    WHERE product_article.Id = %s AND product_article_material.Accessories_Id IS NOT NULL GROUP BY product_article_material.Id"""
        sql_info = my_sql.sql_select(query, (self.id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения аксесуаров", sql_info.msg, QMessageBox.Ok)
            return False
        self.article_accessories = sql_info

        return True

    def set_size_parametr(self):
        self.cb_parametrs.clear()
        select_size_id = self.cb_size.currentData()

        if hasattr(self, 'article_parametrs'):
            for param in self.article_parametrs:
                if select_size_id == param[0] and param[10] == 1:
                    self.cb_parametrs.addItem(param[2], param[1])

        if self.cb_show.isChecked():
            icon = QIcon(getcwd() + "/images/eye.ico")
            for param in self.article_parametrs:
                if select_size_id == param[0] and param[10] == 0:
                    self.cb_parametrs.addItem(icon, param[2], param[1])

    def set_parametr_info(self, other_param_id=False):
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
                    new_item.setData(5, material[2])
                    new_item.setData(-1, status_sql)
                    new_item.setData(-2, material[1])
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

        new_size = QInputDialog.getInt(self, "Размер", "Введите размер")
        if not new_size[1] or new_size[0] == 0:
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
        self.save_change = []  # Переменная для запоминания изменений

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
            query = "DELETE FROM product_article_parametrs WHERE Id = %s"
            sql_info = my_sql.sql_change(query, (param_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql удаление параметра", sql_info.msg, QMessageBox.Ok)
                return False
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
        self.material_name = MaterialName(self, True)
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
        self.ui_double_click_material(row)

    def ui_double_click_material(self, row):
        item = self.tw_materials.item(row, 0)
        variant = "material" if (item.background().color().red() == 153) else "accessories"
        name = item.text()
        id_material = item.data(5)
        sql_id = item.data(-2)
        value = float(self.tw_materials.item(row, 1).text())

        self.change_material = ChangeMaterial(variant)
        self.change_material.le_material.setText(name)
        self.change_material.le_material.setWhatsThis(str(id_material))
        self.change_material.sb_value.setValue(value)
        self.change_material.setModal(True)
        self.change_material.show()

        id = self.change_material.exec()

        if id != -1:
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
        item.setData(-1, "upd")
        item.setData(-2, sql_id)
        item.setBackground(brush)
        self.tw_materials.setItem(row, 0, item)
        item = QTableWidgetItem(str(value))
        item.setData(5, sql_info[0][0])
        item.setData(-1, "upd")
        item.setData(-2, sql_id)
        item.setBackground(brush)
        self.tw_materials.setItem(row, 1, item)
        item = QTableWidgetItem(str(sql_info[0][1]))
        item.setData(5, sql_info[0][0])
        item.setData(-1, "upd")
        item.setData(-2, sql_id)
        item.setBackground(brush)
        self.tw_materials.setItem(row, 2, item)
        item = QTableWidgetItem(str(round(value * float(sql_info[0][1]), 4)))
        item.setData(5, sql_info[0][0])
        item.setData(-1, "upd")
        item.setData(-2, sql_id)
        item.setBackground(brush)
        self.tw_materials.setItem(row, 3, item)
        self.calc()

    def ui_add_accessories(self):
        self.accessories_name = AccessoriesName(self, True)
        self.accessories_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.accessories_name.show()

    def ui_add_operation(self):
        self.operation_name = operation.OperationList(self, True)
        self.operation_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.operation_name.show()

    def ui_change_operation(self):
        try:
            row = self.tw_operations.currentRow()
        except:
            QMessageBox.information(self, "Ошибка", "Выберете операцию для изменения", QMessageBox.Ok)
            return False
        self.ui_double_click_operation(row)

    def ui_dell_operation(self):
        try:
            row = self.tw_operations.currentRow()
        except:
            QMessageBox.information(self, "Ошибка", "Выберете операцию для удаления", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить операцию?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
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
        if id <= 0 or id == item.data(5):
            return False
        else:
            sql_id = item.data(-2)
            item = self.change_operation.new_operation
            for col in range(1, len(item)):
                new_item = QTableWidgetItem(item[col])
                new_item.setData(5, item[0])
                new_item.setData(-1, "upd")
                new_item.setData(-2, sql_id)
                self.tw_operations.setItem(row, col - 1, new_item)
        self.calc()

    def ui_acc(self):
        self.save_sql()
        self.close()
        self.destroy()

    def ui_cancel(self):
        if self.save_change:
            result = QMessageBox.question(self, "Сохранить?", "Сохранить изменение перед выходом?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == 16384:
                self.save_sql()
        self.close()
        self.destroy()

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

    def save_sql(self):
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
                      Client_code = %s, In_On_Place = %s, Price = %s, Product_Note = %s, Cut_Note = %s WHERE Id = %s"""
            sql_param = (self.le_client_name.text(), self.le_barcode.text(), self.le_client_code.text(), self.le_in_on_place.text().replace(",", "."),
                         self.le_price.text().replace(",", "."), self.pe_product_note.toPlainText(), self.pe_cut_note.toPlainText(), parametr_id)
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
                    else:
                        QMessageBox.critical(self, "Ошибка", "Нету id у операции при удалении, это не нормально позовите администратора", QMessageBox.Ok)
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
                    QMessageBox.critical(self, "Ошибка", "Строка операций не подошла в if при созранении, это не нормально позовите администратора", QMessageBox.Ok)
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
                    position_operation += 1
                    if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql изменение материала", sql_info.msg, QMessageBox.Ok)
                        return False

                elif table_item.data(-1) == "set":
                    pass

                else:
                    QMessageBox.critical(self, "Ошибка", "Строка материала не подошла в if при созранении, это не нормально позовите администратора", QMessageBox.Ok)
                    return False

        self.save_change = []

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

    def of_tree_select_operation(self, item):
        self.tw_operations.insertRow(self.tw_operations.rowCount())
        for col in range(1, len(item)):
            new_item = QTableWidgetItem(item[col])
            new_item.setData(5, item[0])
            new_item.setData(-1, "new")
            self.tw_operations.setItem(self.tw_operations.rowCount() - 1, col - 1, new_item)
        self.calc()

    def of_set_material_name(self, material):  # Внешняя функция добавления материала
        query = """SELECT material_name.Id, material_supplyposition.Price
                    FROM material_name LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                    LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                    LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                    WHERE material_name.Name =%s AND material_balance.BalanceWeight > 0 ORDER BY material_supply.Data LIMIT 1"""

        value = QInputDialog.getDouble(self, "Количество", "Введите требуемое количество матриала", decimals=4)
        if value[0] == 0 or value[1] == False:
            return False
        value = value[0]

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

        self.tw_materials.insertRow(self.tw_materials.rowCount())
        item = QTableWidgetItem(material)
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

    def of_set_accessories_name(self, accessories):
        query = """SELECT accessories_name.Id, accessories_supplyposition.Price
                    FROM accessories_name LEFT JOIN accessories_supplyposition ON accessories_name.Id = accessories_supplyposition.accessories_NameId
                    LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.accessories_SupplyPositionId
                    LEFT JOIN accessories_supply ON accessories_supplyposition.accessories_SupplyId = accessories_supply.Id
                    WHERE accessories_name.Name = %s AND accessories_balance.BalanceValue > 0 ORDER BY accessories_supply.Data LIMIT 1"""

        value = QInputDialog.getDouble(self, "Количество", "Введите требуемое количество аксесуара", decimals=4)
        if value[0] == 0 or value[1] == False:
            return False
        value = value[0]

        sql_info = my_sql.sql_select(query, (accessories,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql поиск цены аксесуара", sql_info.msg, QMessageBox.Ok)
            return False
        elif not sql_info:
            query = "SELECT Id, 0 FROM accessories_name WHERE Name = %s"
            sql_info = my_sql.sql_select(query, (accessories,))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql поиск ID аксесуара", sql_info.msg, QMessageBox.Ok)
                return False

        self.tw_materials.insertRow(self.tw_materials.rowCount())
        item = QTableWidgetItem(accessories)
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


class ChangeOperation(QDialog, article_change_operation_class):
    def __init__(self):
        super(ChangeOperation, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

    def ui_view_list_operation(self):
        self.operation_name = operation.OperationList(self, True)
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

    def ui_view_list_material(self):
        if self.variant == "material":
            self.material_name = MaterialName(self, True)
            self.material_name.setWindowModality(QtCore.Qt.ApplicationModal)
            self.material_name.show()
        elif self.variant == "accessories":
            self.accessories_name = AccessoriesName(self, True)
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

    def of_set_material_name(self, item):
        self.le_material.setText(item)
        self.le_material.setWhatsThis(str(-1))

    def of_set_accessories_name(self, item):
        self.le_material.setText(item)
        self.le_material.setWhatsThis(str(-1))


class CopyParametr(QDialog, article_copy_parametr):
    def __init__(self, main):
        super(CopyParametr, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.main = main
        self.set_size_parametr()

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


class AccessoriesName(accessories_provider.AccessoriesName):  # Обновленный клас для добавления аксесуаров
    def double_click_provider(self, select_prov):
        self.m_class.of_set_accessories_name(select_prov.text())
        self.close()
        self.destroy()


class MaterialName(material_provider.MaterialName):  # Обновленный клас для добавления Ткани
    def double_click_provider(self, select_prov):
        self.m_class.of_set_material_name(select_prov.text())
        self.close()
        self.destroy()
