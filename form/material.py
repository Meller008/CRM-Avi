from os import getcwd
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5 import QtCore
from function import my_sql
from form import material_provider, comparing
from decimal import Decimal
import re

material_class, material_base_class = loadUiType(getcwd() + '/ui/material.ui')
add_material_class, add_material_base_class = loadUiType(getcwd() + '/ui/add_material.ui')
add_material_pozition_class, add_material_pozition_base_class = loadUiType(getcwd() + '/ui/add_material_pozition.ui')
material_warning_class, material_warning_base_class = loadUiType(getcwd() + '/ui/material_waring.ui')


class MaterialWarning(QDialog, material_warning_class):
    def __init__(self, *args):
        super(MaterialWarning, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.main = args[0]
        self.setModal(True)
        self.show()

    def set_list_widget(self, items):
        self.lw_pozition.clear()
        for item in items:
            self.lw_pozition.addItem(item)

    def set_text(self, lb_text, pb_text):
        self.lb_warning.setText(lb_text)
        self.pb_ok.setText(pb_text)

    def push_button(self):
        if self.pb_ok.text() == "Удалить":
            self.close()
            self.destroy()
            self.main.delete_supply()
        else:
            self.close()
            self.destroy()


class AddComparingName(comparing.ComparingName):
    def double_click_provider(self, select_prov):
        self.m_class.le_name.setText(select_prov.text())
        self.close()
        self.destroy()


class MaterialNameSelect(material_provider.MaterialName):
    def set_sql_query(self):
        self.sql_list = "SELECT material_name.Name FROM material_name"
        self.sql_add = "INSERT INTO material_name (Name, Information) VALUES (%s, %s)"
        self.sql_change_select = "SELECT material_name.Name, material_name.Information FROM material_name WHERE  Name = %s"
        self.sql_update_select = 'UPDATE material_name SET material_name.Name = %s, material_name.Information = %s ' \
                                 'WHERE material_name.Name = %s'
        self.sql_dell = "DELETE FROM material_name WHERE material_name.Name = %s"

    def set_settings(self):
        self.setWindowTitle("Названия тканей")
        self.toolBar.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.add_title = "Добавить ткань"
        self.change_title = "Изменить ткань"

    def double_click_provider(self, select_prov):
        self.m_class.set_material_name(select_prov.text())
        self.close()
        self.destroy()


class MaterialProviderName(material_provider.MaterialProvider):
    def double_click_provider(self, select_prov):
        self.m_class.le_provider.setText(select_prov.text())
        self.close()
        self.destroy()


class Material(QMainWindow, material_class):
    def __init__(self, *args):
        super(Material, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.view_supply()

    def add_material(self):
        self.add_mat = AddMaterial(self)
        self.add_mat.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_mat.show()

    def view_supply(self):
        query = """SELECT material_supply.Id, DATE_FORMAT(material_supply.Data, '%d.%m.%Y'), material_provider.Name,
                  ROUND((SELECT  SUM(Weight) FROM material_supplyposition WHERE material_supply.Id = material_supplyposition.Material_SupplyId),4) AS Width,
                  ROUND((SELECT  SUM(material_supplyposition.Price * material_supplyposition.Weight) FROM material_supplyposition WHERE material_supply.Id = material_supplyposition.Material_SupplyId) +
                  (SELECT  IFNULL(SUM(comparing_supplyposition.Value * comparing_supplyposition.Price), 0) FROM comparing_supplyposition WHERE material_supply.Id = comparing_supplyposition.Material_SupplyId), 4) AS sum,
                  material_supply.Note
                  FROM material_supply LEFT JOIN material_provider ON material_supply.Material_ProviderId = material_provider.Id"""
        supply = my_sql.sql_select(query)

        if "mysql.connector.errors" in str(type(supply)):
            QMessageBox.critical(self, "Ошибка sql", supply.msg, QMessageBox.Ok)

        self.tw_supply_material.clearContents()
        self.tw_supply_material.setRowCount(len(supply))
        for row in range(len(supply)):
            for column in range(6):
                a = supply[row][column]
                item = QTableWidgetItem(str(a))
                self.tw_supply_material.setItem(row, column, item)

        self.tw_supply_material.horizontalHeader().resizeSection(0, 20)
        self.tw_supply_material.horizontalHeader().resizeSection(1, 75)
        self.tw_supply_material.horizontalHeader().resizeSection(2, 130)
        self.tw_supply_material.horizontalHeader().resizeSection(3, 80)
        self.tw_supply_material.horizontalHeader().resizeSection(4, 100)
        self.tw_supply_material.horizontalHeader().resizeSection(5, 250)
        self.tw_supply_material.horizontalHeader().setSectionHidden(0, True)

    def dell_material(self):
        select_supply = self.tw_supply_material.item(self.tw_supply_material.selectedItems()[0].row(), 0).text()
        query = """ SELECT material_supply.Id AS suplly_ID, material_supplyposition.Id AS position_ID, material_supplyposition.Weight AS width_position,
                material_balance.Material_SupplyPositionId AS ID_position, material_balance.BalanceWeight AS width_balance, material_name.Name
                FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id WHERE material_supply.Id = %s """
        supply = my_sql.sql_select(query, (select_supply, ))
        if "mysql.connector.errors" in str(type(supply)):
            QMessageBox.critical(self, "Ошибка sql", supply.msg, QMessageBox.Ok)

        width_error = []
        for position in supply:
            if position[1] == position[3]:
                if position[2] != position[4]:
                    width_error.append(position[5])
            else:
                QMessageBox.critical(self, "Ошибка обработки заказа", "Не совпали ID позиции и ID баланса")

        if not width_error:
            warning_position = []
            for item in supply:
                warning_position.append(item[5])
            self.warning = MaterialWarning(self)
            self.warning.set_list_widget(warning_position)
        else:
            self.warning = MaterialWarning(self)
            self.warning.set_text("Нельзя удалить!Позиции пошли в работу!", "ОК")
            self.warning.set_list_widget(width_error)

    def delete_supply(self):
        query = "DELETE FROM material_supply WHERE Id = %s"
        id = self.tw_supply_material.item(self.tw_supply_material.selectedItems()[0].row(), 0).text()
        answer_sql = my_sql.sql_change(query, (id, ))
        if "mysql.connector.errors" in str(type(answer_sql)):
            QMessageBox.critical(self, "Ошибка sql", answer_sql.msg, QMessageBox.Ok)
        self.view_supply()

    def double_click(self, row, column):
        id = self.tw_supply_material.item(row, 0).text()
        self.change = ChangeSupply(id, self)
        self.change.setWindowModality(QtCore.Qt.ApplicationModal)
        self.change.show()


class AddMaterial(QMainWindow, add_material_class):
    def __init__(self, *args):
        self.main = args[0]
        super(AddMaterial, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.de_data.setDate(QtCore.QDate.currentDate())
        self.save = False

    def add_comparing_pozition(self):
        if not self.save:
            self.save = True
        self.add_comp_poz = AddComparingPosition(self)
        self.add_comp_poz.set_settings("Добавление прочих растрат", "Добавить")
        self.add_comp_poz.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_comp_poz.show()

    def view_name_provider(self):
        if not self.save:
            self.save = True
        self.view_provider = MaterialProviderName(self)
        self.view_provider.setWindowModality(QtCore.Qt.ApplicationModal)
        self.view_provider.show()

    def add_materia_pozition(self):
        if not self.save:
            self.save = True
        self.add_mat_poz = AddMaterialPosition(self)
        self.add_mat_poz.set_settings("Добавление ткани", "Добавить")
        self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_mat_poz.show()

    def calculation(self):
        self.weight = 0
        self.summ_material = 0
        self.summ = 0
        for row in range(self.tw_position.rowCount()):
            color = self.tw_position.item(row, 0).background().color().red()
            weight_position = float(self.tw_position.item(row, 1).text())
            summ_position = float(self.tw_position.item(row, 3).text())
            if color != 221:
                self.weight += weight_position
                self.summ_material += summ_position
            self.summ += summ_position

            self.la_sum_weight.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str("%s %.4f" % (re.findall(r'^\D+[\=]', self.la_sum_weight.text())[0], self.weight))))
            self.la_sum_material.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str("Сумма материала = %.4f" % self.summ_material)))
            self.la_sum.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str("Сумма всего = %.4f" % self.summ)))

    def add_pozition(self, mat_poz, collor, row=False):
        self.j = 0
        if row is False:
            self.tw_position.setRowCount(self.tw_position.rowCount() + 1)
            row = self.tw_position.rowCount()-1
        for i in mat_poz:
            item = QTableWidgetItem(str(i))
            brush = QBrush(QColor(collor[0], collor[1], collor[2], 255))
            item.setBackground(brush)
            self.tw_position.setItem(row, self.j, item)
            self.j += 1
        self.tw_position.horizontalHeader().resizeSection(0, 240)
        self.tw_position.horizontalHeader().resizeSection(1, 75)
        self.tw_position.horizontalHeader().resizeSection(2, 65)
        self.tw_position.horizontalHeader().resizeSection(3, 95)
        self.calculation()

    def double_click(self, i):
        if not self.save:
            self.save = True
        collor = self.tw_position.item(i, 0).background().color().red()
        name = self.tw_position.item(i, 0).text()
        value = self.tw_position.item(i, 1).text()
        price = self.tw_position.item(i, 2).text()
        summ = self.tw_position.item(i, 3).text()

        if collor == 153:
            self.add_mat_poz = AddMaterialPosition(self)
            self.add_mat_poz.set_settings("Редактирование ткани", "Изменить")
            self.add_mat_poz.set_meaning((name, value, price, summ), i)
            self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
            self.add_mat_poz.show()
        elif collor == 221:
            self.add_mat_poz = AddComparingPosition(self)
            self.add_mat_poz.set_settings("Редактирование прочих растрат", "Изменить")
            self.add_mat_poz.set_meaning((name, value, price, summ), i)
            self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
            self.add_mat_poz.show()

    def add_material_sql(self):
        query = "insert into avi_crm.material_supply (Material_ProviderId, Data, Note) select Id, %s, %s from avi_crm.material_provider where Name=%s"
        data = self.de_data.date().toString("yyyy.MM.dd")
        parametr = (data, self.le_note.text(), self.le_provider.text())
        self.id_supply = my_sql.sql_change(query, parametr)
        if "mysql.connector.errors" in str(type(self.id_supply)):
            QMessageBox.critical(self, "Ошибка sql", self.id_supply.msg, QMessageBox.Ok)

        self.material = []
        self.comparing = []
        for row in range(self.tw_position.rowCount()):
            color = self.tw_position.item(row, 0).background().color().red()
            self.name = self.tw_position.item(row, 0).text()
            self.value = self.tw_position.item(row, 1).text()
            self.price = self.tw_position.item(row, 2).text()
            if color == 153:
                self.material.append((self.id_supply, self.value, self.price, self.name))
            elif color == 221:
                self.comparing.append((self.id_supply, self.value, self.price, self.name))

        if self.material:
            query = "INSERT INTO avi_crm.material_supplyposition (Material_SupplyId, Material_NameId, Weight, Price) SELECT %s, Id, %s, %s FROM material_name WHERE Name = %s"
            sql_ret = my_sql.sql_many(query, self.material)
            if "mysql.connector.errors" in str(type(sql_ret)):
                QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)

        if self.comparing:
            query = "INSERT INTO avi_crm.comparing_supplyposition (Material_SupplyId, Comparing_NameId, Value, Price) SELECT %s, Id, %s, %s FROM comparing_name WHERE Name = %s"
            sql_ret = my_sql.sql_many(query, self.comparing)
            if "mysql.connector.errors" in str(type(sql_ret)):
                QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)

        if self.save:
            self.save = False
        self.close()
        self.destroy()
        self.main.view_supply()

    def dell_row(self):
        if not self.save:
            self.save = True
        result = QMessageBox.question(self, "Удаление", "Точно удалить позицию?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            self.tw_position.removeRow(self.tw_position.selectedItems()[0].row())

    def change_line_edit(self):
        if not self.save:
            self.save = True

    def closeEvent(self, e):
        if self.save:
            result = QMessageBox.question(self, "Выйтиb?", "Сохранить изменения перед выходом?",
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if result == 16384:
                self.add_material_sql()
                e.accept()
            elif result == 65536:
                e.accept()
            elif result == 4194304:
                e.ignore()
        else:

            e.accept()


class ChangeSupply(AddMaterial):
    def __init__(self, *args):
        super(AddMaterial, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Редактирование прихода ткани")
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.pb_add.setText("Сохранить изменения")
        self.save = False
        self.main = args[1]
        self.id_supply = args[0]
        self.set_supply_info()
        self.queue_dell = []

    def set_supply_info(self):
        query = """SELECT material_supply.Id, material_provider.Name, Data, Note,  Material_SupplyPosition.Id, material_name.Name,
                material_supplyposition.Price, material_supplyposition.Weight, material_balance.BalanceWeight
                FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                LEFT JOIN material_provider ON material_supply.Material_ProviderId = material_provider.Id WHERE material_supply.Id =  %s"""
        supply = my_sql.sql_select(query, (self.id_supply, ))
        if "mysql.connector.errors" in str(type(supply)):
            QMessageBox.critical(self, "Ошибка sql", supply.msg, QMessageBox.Ok)

        self.le_provider.setText(supply[0][1])
        self.de_data.setDate(supply[0][2])
        self.le_note.setText(supply[0][3])

        self.tw_position.setColumnCount(6)
        column_name = QTableWidgetItem("Остаток")
        self.tw_position.setHorizontalHeaderItem(4, column_name)
        self.tw_position.horizontalHeader().setSectionHidden(5, True)

        for row in supply:
            position = [row[5], row[7], row[6], round(row[7]*row[6], 4), row[8], row[4]]
            if row[7] == row[8]:
                color = (153, 221, 255)

            elif row[8] == 0:
                color = (255, 123, 123)

            else:
                color = (255, 255, 127)

            self.add_pozition(position, color)

        query = """SELECT IFNULL(comparing_supplyposition.Id, 'SQL_Пуст'), comparing_name.Name, comparing_supplyposition.Price, comparing_supplyposition.Value
                FROM material_supply LEFT JOIN comparing_supplyposition ON material_supply.Id = comparing_supplyposition.Material_SupplyId
                LEFT JOIN comparing_name ON comparing_supplyposition.Comparing_NameId = comparing_name.Id WHERE material_supply.Id =  %s"""
        supply_comparing = my_sql.sql_select(query, (self.id_supply, ))
        if "mysql.connector.errors" in str(type(supply_comparing)):
            QMessageBox.critical(self, "Ошибка sql", supply_comparing.msg, QMessageBox.Ok)

        if "SQL_Пуст" not in supply_comparing[0]:
            for row in supply_comparing:
                position = [row[1], row[3], row[2], round(row[3]*row[2], 4), row[3], row[0]]
                color = (221, 255, 204)
                self.add_pozition(position, color)
        self.save = False

    def double_click(self, i):
        if not self.save:
            self.save = True
        collor = self.tw_position.item(i, 0).background().color().red()
        name = self.tw_position.item(i, 0).text()
        value = self.tw_position.item(i, 1).text()
        price = self.tw_position.item(i, 2).text()
        summ = self.tw_position.item(i, 3).text()

        if collor == 221:
            self.add_mat_poz = AddComparingPosition(self)
            self.add_mat_poz.set_settings("Редактирование прочих растрат", "Изменить")
            self.add_mat_poz.set_meaning((name, value, price, summ), i)
            self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
            self.add_mat_poz.show()
        else:
            self.add_mat_poz = AddMaterialPosition(self)
            self.add_mat_poz.set_settings("Редактирование ткани", "Изменить")
            self.add_mat_poz.set_meaning((name, value, price, summ), i)
            self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
            self.add_mat_poz.show()

    def add_material_sql(self):
        query = """SELECT material_provider.Name, material_supply.Data, material_supply.Note
                FROM material_supply LEFT JOIN material_provider ON material_supply.Material_ProviderId = material_provider.Id
                WHERE material_supply.Id = %s"""
        supply = my_sql.sql_select(query, (self.id_supply, ))
        if "mysql.connector.errors" in str(type(supply)):
            QMessageBox.critical(self, "Ошибка sql", supply.msg, QMessageBox.Ok)

        query = """SELECT CAST(material_supplyposition.Id AS CHAR(11)), material_name.Name, material_supplyposition.Weight, material_supplyposition.Price
                FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id WHERE material_supply.Id = %s"""
        supply_material = my_sql.sql_select(query, (self.id_supply, ))
        if "mysql.connector.errors" in str(type(supply_material)):
            QMessageBox.critical(self, "Ошибка sql", supply_material.msg, QMessageBox.Ok)

        query = """SELECT IFNULL(comparing_supplyposition.Id, 'Пустой_SQL'), comparing_name.Name, comparing_supplyposition.Value, comparing_supplyposition.Price
                FROM material_supply LEFT JOIN comparing_supplyposition ON material_supply.Id = comparing_supplyposition.Material_SupplyId
                LEFT JOIN comparing_name ON comparing_supplyposition.Comparing_NameId = comparing_name.Id WHERE material_supply.Id =  %s"""
        supply_comparing = my_sql.sql_select(query, (self.id_supply, ))
        if "mysql.connector.errors" in str(type(supply_comparing)):
            QMessageBox.critical(self, "Ошибка sql", supply_comparing.msg, QMessageBox.Ok)

        if self.le_provider.text() != supply[0][0] or self.de_data.date() != supply[0][1] or self.le_note.text() != supply[0][2]:
            query = "SELECT Id FROM material_provider WHERE Name = %s"
            provider = my_sql.sql_select(query, (self.le_provider.text(), ))
            if "mysql.connector.errors" in str(type(provider)):
                QMessageBox.critical(self, "Ошибка sql", provider.msg, QMessageBox.Ok)

            query = "UPDATE  material_supply SET Material_ProviderId = %s, Data = %s, Note = %s WHERE Id = %s"
            sql_re = my_sql.sql_change(query, (provider[0][0], self.de_data.date().toString("yyyy.MM.dd"), self.le_note.text(), self.id_supply))
            if "mysql.connector.errors" in str(type(sql_re)):
                QMessageBox.critical(self, "Ошибка sql", sql_re.msg, QMessageBox.Ok)

        flag_break = False
        for row in range(self.tw_position.rowCount()):
            if not flag_break:
                sypply_position = []
                try:
                    sypply_position.append(self.tw_position.item(row, 5).text())
                except:
                    sypply_position.append("None")
                sypply_position.append(self.tw_position.item(row, 0).text())
                sypply_position.append(Decimal(self.tw_position.item(row, 1).text()))
                sypply_position.append(Decimal(self.tw_position.item(row, 2).text()))

                if self.tw_position.item(row, 0).background().color().red() != 221:
                    for item in supply_material:
                        if item[0] == sypply_position[0]:
                            if item != tuple(sypply_position):  # Строки не совпали
                                balance = item[2] - Decimal(self.tw_position.item(row, 4).text())
                                if balance <= sypply_position[2]:  # Изменение нормально
                                    query = "SELECT BalanceWeight FROM material_balance WHERE Material_SupplyPositionId = %s"
                                    balance = my_sql.sql_select(query, (sypply_position[0], ))
                                    if "mysql.connector.errors" in str(type(balance)):
                                        QMessageBox.critical(self, "Ошибка sql", balance.msg, QMessageBox.Ok)
                                        flag_break = True
                                        break
                                    query = """UPDATE material_supplyposition SET
                                    Material_NameId = (SELECT Id FROM avi_crm.material_name WHERE Name = %s),
                                    Weight = %s, Price = %s WHERE Id = %s"""
                                    sql_re = my_sql.sql_change(query, (sypply_position[1], sypply_position[2],
                                                                       sypply_position[3], sypply_position[0]))
                                    if "mysql.connector.errors" in str(type(sql_re)):
                                        QMessageBox.critical(self, "Ошибка sql", sql_re.msg, QMessageBox.Ok)
                                        flag_break = True
                                        break

                                    query = """UPDATE material_balance SET BalanceWeight = %s
                                               WHERE Material_SupplyPositionId = %s """
                                    new_balance = balance[0][0] + (sypply_position[2] - item[2])
                                    sql_re = my_sql.sql_change(query, (new_balance, sypply_position[0]))
                                    if "mysql.connector.errors" in str(type(sql_re)):
                                        QMessageBox.critical(self, "Ошибка sql", sql_re.msg, QMessageBox.Ok)
                                        flag_break = True
                                        break
                                    break

                                else:  # Неправильный вес
                                    balance = item[2] - Decimal(self.tw_position.item(row, 4).text())
                                    QMessageBox.warning(self, "Неправильное количество",
                                                        """Невозможно изменить позицию <<%s>> \nОстаток = %s, значит приход должен быть не менее %s""" %
                                                        (sypply_position[1], self.tw_position.item(row, 4).text(), balance))
                                    flag_break = True
                                    break

                        elif sypply_position[0] == "None":  # Добавление строки
                            query = """INSERT INTO avi_crm.material_supplyposition (Material_SupplyId, Material_NameId, Weight, Price)
                                        SELECT %s, Id, %s, %s FROM material_name WHERE Name = %s"""
                            sql_ret = my_sql.sql_change(query, (self.id_supply, sypply_position[2], sypply_position[3], sypply_position[1]))
                            if "mysql.connector.errors" in str(type(sql_ret)):
                                QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)
                                flag_break = True
                                break
                            break
                else:
                    for item in supply_comparing:
                        if item[0] == sypply_position[0]:
                            if item != tuple(sypply_position):  # Мзменение прочих растрат
                                query = """UPDATE comparing_supplyposition SET
                                    Comparing_NameId = (SELECT Id FROM comparing_name WHERE Name = %s),
                                    Value = %s, Price = %s WHERE Id = %s"""
                                sql_re = my_sql.sql_change(query, (sypply_position[1], sypply_position[2],
                                                                       sypply_position[3], sypply_position[0]))
                                if "mysql.connector.errors" in str(type(sql_re)):
                                    QMessageBox.critical(self, "Ошибка sql", sql_re.msg, QMessageBox.Ok)
                                    flag_break = True
                                    break
                                break
                        elif sypply_position[0] == "None":  # Доьавление прочих растрат
                            query = """INSERT INTO avi_crm.comparing_supplyposition (Material_SupplyId, Comparing_NameId, Value, Price)
                                        SELECT %s, Id, %s, %s FROM comparing_name WHERE Name = %s"""
                            sql_ret = my_sql.sql_change(query, (self.id_supply, sypply_position[2], sypply_position[3], sypply_position[1]))
                            if "mysql.connector.errors" in str(type(sql_ret)):
                                QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)
                                flag_break = True
                                break
                            break
        if self.queue_dell:  # Удаление позиций
            for item in self.queue_dell:
                if item[0] == 221:
                    query = "DELETE FROM comparing_supplyposition WHERE Id = %s"
                elif item[0] == 153:
                    query = "DELETE FROM material_supplyposition WHERE Id = %s"
                else:
                    QMessageBox.critical(self, "Ошибка при удалении", "Нельзя удалить позицию которая пошла в работу")
                    break

                sql_ret = my_sql.sql_change(query, (item[1], ))
                if "mysql.connector.errors" in str(type(sql_ret)):
                    QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)
                    flag_break = True
                    break

        if self.save:
            self.save = False
        self.close()
        self.destroy()
        self.main.view_supply()

    def dell_row(self):
        if not self.save:
            self.save = True
        result = QMessageBox.question(self, "Удаление", "Точно удалить позицию?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            color_r = self.tw_position.selectedItems()[0].background().color().red()
            if color_r == 221 or color_r == 153 or color_r == 252:
                self.queue_dell.append((color_r, int(self.tw_position.item(self.tw_position.selectedItems()[0].row(), 5).text())))
                self.tw_position.removeRow(self.tw_position.selectedItems()[0].row())
            else:
                QMessageBox.critical(self, "Ошибка при добавлении в очередь удаления", "Нельзя удалить позицию которая пошла в работу", QMessageBox.Ok)

    def closeEvent(self, e):
        if self.save:
            result = QMessageBox.question(self, "Выйтиb?", "Сохранить изменения перед выходом?",
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if result == 16384:
                self.add_material_sql()
                e.accept()
            elif result == 65536:
                e.accept()
            elif result == 4194304:
                e.ignore()

        else:
            e.accept()

    def set_settings(self, setting):
        for name, value in setting.items():
            if name == "WinTitle":
                self.setWindowTitle(value)
            elif name == "WinColor":
                try:
                    self.widget.setStyleSheet("background-color: rgb%s;" % value)
                except:
                    self.toolBar.setStyleSheet("background-color: rgb%s;" % value)
            else:
                getattr(self, name).setText(value)


class AddMaterialPosition(QDialog, add_material_pozition_class):
    def __init__(self, *args):
        super(AddMaterialPosition, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.main = args[0]
        self.i = False

    def set_settings(self, title, butt):
        self.collor = (153, 221, 255)
        self.setWindowTitle(title)
        self.pushButton.setText(butt)

    def set_meaning(self, meaning, i):
        self.i = i
        self.le_name.setText(meaning[0])
        self.le_price.setText(meaning[2])
        self.le_value.setText(meaning[1])

    def view_material_name(self):
        self.mat_name = MaterialNameSelect(self)
        self.mat_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.mat_name.show()

    def set_material_name(self, change_material):
        self.le_name.setText(change_material)

    def change_price(self):
        if self.le_price.text():
            try:
                self.price = round(float(self.le_price.text().replace(",", ".")), 4)

            except ValueError as error:
                self.price = 0
                QMessageBox.information(self, "Ошибка ввода", "Не верно введена цена, скорее всего вы ввели символ. "
                                                              "\n Ошибка: %s" % error, QMessageBox.Ok)
        else:
            self.price = 0

        if self.le_value.text():
            try:
                self.value = round(float(self.le_value.text().replace(",", ".")), 4)

            except ValueError as error:
                self.value = 0
                QMessageBox.information(self, "Ошибка ввода", "Не верно введено количество, скорее всего вы ввели символ."
                                                              "\n Ошибка: %s" % error, QMessageBox.Ok)
        else:
                self.value = 0

        if self.price != 0 and self.value != 0:
            self.lb_summ.setText("Сумма=%s" % str(round(self.price * self.value, 4)))
        else:
            self.lb_summ.setText("Сумма=")

    def add_material_line(self):
        if not self.le_name.text():
            QMessageBox.information(self, "Ошибка ввода", "Вы заполнили не все поля", QMessageBox.Ok)
        else:
            try:
                par = (self.le_name.text(), round(float(self.le_value.text().replace(",", ".")), 4),
                       round(float(self.le_price.text().replace(",", ".")), 4), self.lb_summ.text().replace("Сумма=", ""))

                self.close()
                self.destroy()
                self.main.add_pozition(par, self.collor, self.i)
            except:
                QMessageBox.information(self, "Ошибка ввода", "Вы заполнили не все поля", QMessageBox.Ok)


class AddComparingPosition(AddMaterialPosition):
    def set_settings(self, title, butt):
        self.setWindowTitle(title)
        self.pushButton.setText(butt)
        self.lb_name.setText("Название")
        self.widget.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.lb_value.setText("Кол-во")

    def view_material_name(self):
        self.mat_name = AddComparingName(self)
        self.mat_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.mat_name.show()

    def add_material_line(self):
        par = (self.le_name.text(), self.le_value.text(), self.le_price.text(), self.lb_summ.text().replace("Сумма=", ""))
        collor = (221, 255, 204)
        self.close()
        self.destroy()
        self.main.add_pozition(par, collor, self.i)

