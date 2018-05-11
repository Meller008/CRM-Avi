from os import getcwd
from form.templates import tree, table
from form.templates import list
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from function import my_sql
from classes.my_class import User


class OperationList(tree.TreeList):
    def set_settings(self):
        self.resize(1050, 400)
        self.setWindowTitle("Список операций")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(85, 255, 255);")  # Цвет бара
        self.pb_other.setText("Артикула")

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Название", 300), ("Цена", 70), ("Машинка", 120), ("Заметка", 300))

        self.query_tree_select = "SELECT Id, Parent_Id, Name FROM operation_tree ORDER BY Parent_Id, Position"
        self.query_tree_add = "INSERT INTO operation_tree (Parent_Id, Name, Position) VALUES (%s, %s, %s)"
        self.query_tree_change = "UPDATE operation_tree SET Name = %s, Position = %s WHERE Id = %s"
        self.query_tree_del = "DELETE FROM operation_tree WHERE Id = %s"

        self.filter = None
        self.query_table_all = "SELECT operations.Id, operations.Tree_Id, operations.Name, operations.Price, sewing_machine.Name, operations.Note2  " \
                                  "FROM operations LEFT JOIN sewing_machine ON operations.Sewing_Machine_Id = sewing_machine.Id"

        #  нулевой элемент должен быть ID а первый Parent_ID (ID категории)
        self.query_table_select = "SELECT operations.Id, operations.Tree_Id, operations.Name, operations.Price, sewing_machine.Name, operations.Note2  " \
                                  "FROM operations LEFT JOIN sewing_machine ON operations.Sewing_Machine_Id = sewing_machine.Id"
        self.query_transfer_item = "UPDATE operations SET Tree_Id = %s WHERE Id = %s"
        self.query_table_dell = "DELETE FROM operations WHERE Id = %s"

        # Настройки окна добавления и редактирования дерева
        self.set_new_win_tree = {"WinTitle": "Добавление категории",
                                 "WinColor": "(85, 255, 255)",
                                 "lb_name": "Название категории"}

        # Настройки окна переноса элементов
        self.set_transfer_win = {"WinTitle": "Изменение категории",
                                 "WinColor": "(85, 255, 255)"}

    def ui_add_table_item(self):  # Добавить предмет
        try:
            tree_id = self.tree_widget.selectedItems()[0].data(0, 5)
        except:
            QMessageBox.critical(self, "Ошибка ", "Выделите элемент дерева куда добавлять предмет", QMessageBox.Ok)
            return False
        if tree_id < 0:
            QMessageBox.critical(self, "Ошибка ", "Вы выбрали неправильный элемент", QMessageBox.Ok)
            return False

        self.new_operation = Operation(self, False, tree_id)
        self.new_operation.setModal(True)
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

        self.select_item = item_id

        self.new_operation = Operation(self, item_id)
        self.new_operation.setModal(True)
        self.new_operation.show()

    def ui_double_item_table(self):  # Дублирование строки
        try:
            item_id = self.table_widget.selectedItems()[0].data(5)
        except:
            QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите дублировать", QMessageBox.Ok)
            return False
        result = QMessageBox.question(self, "Дублирование", "Точно хотите дублировать операцию?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            query = "INSERT INTO operations (Tree_Id, Name, Price, Sewing_Machine_Id, Note) " \
                    "(SELECT Tree_Id, CONCAT(Name, '-К'), Price, Sewing_Machine_Id, Note FROM operations WHERE Id = %s)"
            sql_info = my_sql.sql_change(query, (item_id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql дублирование строки", sql_info.msg, QMessageBox.Ok)
                return False
            self.set_table_info()

    def ui_double_click_table_item(self, item):  # Двойной клик по элементу
        if not self.dc_select:
            self.ui_change_table_item(item.data(5))
        else:
            row = item.row()
            item = (item.data(5), self.table_widget.item(row, 0).text(), self.table_widget.item(row, 1).text(), self.table_widget.item(row, 2).text())
            self.main.of_tree_select_operation(item)
            self.close()
            self.destroy()

    def ui_filter_table(self):
        if self.filter is None:
            self.filter = OperationFilter(self)
        self.filter.of_set_sql_query(self.query_table_all)
        self.filter.setWindowModality(Qt.ApplicationModal)
        self.filter.show()

    def ui_other(self):
        try:
            item_id = self.table_widget.selectedItems()[0].data(5)
        except:
            QMessageBox.critical(self, "Ошибка ", "Выделите операцию", QMessageBox.Ok)
            return False

        query = """SELECT CONCAT(product_article.Article, ' ', product_article_size.Size, ' ', product_article_parametrs.Name) FROM operations
                        LEFT JOIN product_article_operation ON operations.Id = product_article_operation.Operation_Id
                        LEFT JOIN product_article_parametrs ON product_article_operation.Product_Article_Parametrs_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE operations.Id = %s"""
        sql_art = my_sql.sql_select(query, (item_id, ))
        if "mysql.connector.errors" in str(type(sql_art)):
                QMessageBox.critical(self, "Ошибка sql получения зависимости", sql_art.msg, QMessageBox.Ok)
                return False

        text = ""
        count_art = 0
        for art in sql_art:
            if art[0] is None:
                text = "Нет совпадений"
                break
            text += art[0] + "\n"
            count_art += 1

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Совпадения")
        msg.setText("Найдено %s совпадений" % count_art)
        msg.setDetailedText(text)
        msg.exec()

    def of_set_filter(self, sql):
        self.query_table_select = sql

        self.ui_update_table()


class Operation(QDialog):
    def __init__(self, main, id=False, tree_id=False):
        super(Operation, self).__init__()
        loadUi(getcwd() + '/ui/operation_change.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.main = main
        self.id = id
        self.tree_id = tree_id
        if self.id:
            self.set_sql_info()

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

    def set_sql_info(self):
        query = """SELECT operations.Name, operations.Price, sewing_machine.Name, sewing_machine.Id, operations.Note, operations.Note2
                    FROM operations LEFT JOIN sewing_machine ON operations.Sewing_Machine_Id = sewing_machine.Id WHERE operations.Id = %s"""
        sql_info = my_sql.sql_select(query, (self.id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение информации", sql_info.msg, QMessageBox.Ok)
            return False
        self.le_name.setText(sql_info[0][0])
        self.le_price.setText(str(sql_info[0][1]))
        self.le_machine.setText(sql_info[0][2])
        self.le_machine.setWhatsThis(str(sql_info[0][3]))
        self.pe_note.appendPlainText(sql_info[0][4])
        self.le_note_2.setText(sql_info[0][5])

    def ui_view_machine(self):
        self.machine = MachineName(self, True)
        self.machine.setWindowModality(Qt.ApplicationModal)
        self.machine.show()

    def of_list_insert(self, item):
        self.le_machine.setText(item[1])
        self.le_machine.setWhatsThis(str(item[0]))

    def ui_add(self):
        if self.le_name.text() == "" or self.le_machine.text() == "" or self.le_price.text() == "":
            QMessageBox.critical(self, "Ошибка сохранения", "Не заполнены обязательные поля.", QMessageBox.Ok)
            return False
        try:
            price = float(self.le_price.text().replace(",", "."))
        except:
            QMessageBox.critical(self, "Ошибка цены", "Не правильно введена цена.", QMessageBox.Ok)
            return False

        if self.id:
            query = "UPDATE operations SET Name = %s, Sewing_Machine_Id = %s, Price = %s, Note = %s, Note2 = %s WHERE Id = %s"
            sql_info = my_sql.sql_change(query, (self.le_name.text(), self.le_machine.whatsThis(), price, self.pe_note.toPlainText(), self.le_note_2.text(), self.id))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql обновление информации", sql_info.msg, QMessageBox.Ok)
                return False
        elif self.tree_id:
            query = "INSERT INTO operations (Tree_Id, Name, Price, Sewing_Machine_Id, Note, Note2) VALUES (%s, %s, %s, %s, %s, %s)"
            sql_info = my_sql.sql_change(query, (self.tree_id, self.le_name.text(), price, self.le_machine.whatsThis(), self.pe_note.toPlainText(), self.le_note_2.text()))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql добавление информации", sql_info.msg, QMessageBox.Ok)
                return False
        else:
            QMessageBox.critical(self, "Ошибка", "Нету ни Id, ни Tree_Id", QMessageBox.Ok)

        self.close()
        self.destroy()
        self.main.set_table_info()

    def ui_cancel(self):
        result = QMessageBox.question(self, "Выход", "Точно хотите выйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            self.close()
            self.destroy()


class OperationFilter(QDialog,):
    def __init__(self, main):
        super(OperationFilter, self).__init__()
        loadUi(getcwd() + '/ui/operation_filter.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main

    def ui_view_machine(self):
        self.machine = MachineName(self, True)
        self.machine.setWindowModality(Qt.ApplicationModal)
        self.machine.show()

    def ui_del_machine(self):
        self.le_machine.setWhatsThis("")
        self.le_machine.setText("")

    def ui_acc(self):
        where = ""

        # Блок условий названия операции
        if self.le_name.text() != '':
            where = self.add_filter(where, "(operations.Name LIKE '%s')" % ("%" + self.le_name.text() + "%",))

        # Блок  условий выбора машинки
        if self.le_machine.whatsThis() != '':
            where = self.add_filter(where, "(operations.Sewing_Machine_Id = %s)" % self.le_machine.whatsThis())

        if where:
            self.sql_query_all = self.sql_query_all + " WHERE " + where

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

    def of_list_insert(self, item):
        self.le_machine.setText(item[1])
        self.le_machine.setWhatsThis(str(item[0]))


class MachineName(list.ListItems):
    def set_settings(self):
        self.setWindowTitle("Список машинок")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(85, 255, 255);")  # Цвет бара
        self.title_new_window = "Машинка"  # Имя вызываемых окон

        self.sql_list = "SELECT Id, Name FROM sewing_machine"
        self.sql_add = "INSERT INTO sewing_machine (Name, Note) VALUES (%s, %s)"
        self.sql_change_select = "SELECT Name, Note FROM sewing_machine WHERE Id = %s"
        self.sql_update_select = 'UPDATE sewing_machine SET Name = %s, Note = %s WHERE Id = %s'
        self.sql_dell = "DELETE FROM sewing_machine WHERE Id = %s"

        self.set_new_win = {"WinTitle": "Машинка",
                            "WinColor": "(85, 255, 255)",
                            "lb_name": "Название",
                            "lb_note": "Заметка"}


class OperationAddList(table.TableList):
    def set_settings(self):
        self.resize(820, 300)
        self.setWindowTitle("Список дополнительных операций")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(85, 255, 255);")  # Цвет бара

        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.pb_change.deleteLater()
        self.pb_filter.deleteLater()

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Название", 300), ("Цена", 70), ("Машинка", 120), ("Заметка", 300))

        self.query_table_all = """SELECT add_operation_list.Id, operations.Name, operations.Price, sewing_machine.Name, operations.Note2
                                    FROM add_operation_list
                                      LEFT JOIN operations ON add_operation_list.Id = operations.Id
                                      LEFT JOIN sewing_machine ON operations.Sewing_Machine_Id = sewing_machine.Id"""

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT add_operation_list.Id, operations.Name, operations.Price, sewing_machine.Name, operations.Note2
                                        FROM add_operation_list
                                          LEFT JOIN operations ON add_operation_list.Id = operations.Id
                                          LEFT JOIN sewing_machine ON operations.Sewing_Machine_Id = sewing_machine.Id"""

        self.query_table_dell = "DELETE FROM add_operation_list WHERE Id = %s"

    def ui_add_table_item(self):  # Добавить предмет
        self.new_operation = OperationList(self, dc_select=True)
        self.new_operation.setWindowModality(Qt.ApplicationModal)
        self.new_operation.show()

    def ui_dell_table_item(self):
        result = QMessageBox.question(self, "Удаление", "Точно удалить элемент?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            try:
                id_item = self.table_widget.selectedItems()
            except:
                QMessageBox.critical(self, "Ошибка Удаления", "Выделите элемент который хотите удалить", QMessageBox.Ok)
                return False
            for id in id_item:
                sql_info = my_sql.sql_change(self.query_table_dell, (id.data(5), ))
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql удаления элемента таблицы", sql_info.msg, QMessageBox.Ok)
                    return False
        self.set_table_info()

    def ui_double_click_table_item(self, item):  # Двойной клик по элементу
        if not self.dc_select:
            self.ui_change_table_item(item.data(5))
        else:
            # что хотим получить ставим всместо 0
            item = (self.table_widget.item(item.row(), 0).text(), item.data(5))
            self.main.of_tree_select_add_operation(item)
            self.close()
            self.destroy()

    def of_tree_select_operation(self, item):
        query = "INSERT INTO add_operation_list (Id) VALUES (%s)"
        sql_info = my_sql.sql_change(query, (item[0],))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql добавления операции", sql_info.msg, QMessageBox.Ok)
            return False

        self.ui_update()