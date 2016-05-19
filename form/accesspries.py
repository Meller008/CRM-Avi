from form import material, accessories_provider
from PyQt5 import QtCore
from function import my_sql
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from decimal import Decimal


class Accessories(material.Material):
    def view_supply(self):
        query = """SELECT accessories_supply.Id, DATE_FORMAT(accessories_supply.Data, '%d.%m.%Y'), accessories_provider.Name,
                  ROUND((SELECT  SUM(Value) FROM accessories_supplyposition WHERE accessories_supply.Id = accessories_supplyposition.accessories_SupplyId),4) AS Width,
                  ROUND((SELECT  SUM(accessories_supplyposition.Price * accessories_supplyposition.Value) FROM accessories_supplyposition WHERE accessories_supply.Id = accessories_supplyposition.accessories_SupplyId) +
                  (SELECT  IFNULL(SUM(comparing_supplyposition.Value * comparing_supplyposition.Price), 0) FROM comparing_supplyposition WHERE accessories_supply.Id = comparing_supplyposition.Accessories_SupplyId), 4) AS sum,
                  accessories_supply.Note
                  FROM accessories_supply LEFT JOIN accessories_provider ON accessories_supply.accessories_ProviderId = accessories_provider.Id"""
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

    def double_click(self, row, column):
        id = self.tw_supply_material.item(row, 0).text()
        self.change = AccessoriesChangeSupply(id, self)
        settings = {"WinTitle": "Редактирование прихода фурнитуры",
                    "WinColor": "(251, 110, 255)",
                    "pb_add_material": "Добавить фурнитуру"}
        self.change.set_settings(settings)
        self.change.setWindowModality(QtCore.Qt.ApplicationModal)
        self.change.show()

    def dell_material(self):
        select_supply = self.tw_supply_material.item(self.tw_supply_material.selectedItems()[0].row(), 0).text()
        query = """ SELECT accessories_supply.Id AS suplly_ID, accessories_supplyposition.Id AS position_ID, accessories_supplyposition.Value AS width_position,
                accessories_balance.accessories_SupplyPositionId AS ID_position, accessories_balance.BalanceValue AS width_balance, accessories_name.Name
                FROM accessories_supply LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.accessories_SupplyId
                LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.accessories_SupplyPositionId
                LEFT JOIN accessories_name ON accessories_supplyposition.accessories_NameId = accessories_name.Id WHERE accessories_supply.Id = %s """
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
            self.warning = material.MaterialWarning(self)
            self.warning.set_list_widget(warning_position)
        else:
            self.warning = material.MaterialWarning(self)
            self.warning.set_text("Нельзя удалить!Позиции пошли в работу!", "ОК")
            self.warning.set_list_widget(width_error)

    def delete_supply(self):
        query = "DELETE FROM accessories_supply WHERE Id = %s"
        id = self.tw_supply_material.item(self.tw_supply_material.selectedItems()[0].row(), 0).text()
        answer_sql = my_sql.sql_change(query, (id, ))
        if "mysql.connector.errors" in str(type(answer_sql)):
            QMessageBox.critical(self, "Ошибка sql", answer_sql.msg, QMessageBox.Ok)
        self.view_supply()

    def set_settings(self):
        self.setWindowTitle("Приход фурнитуры")
        self.toolBar.setStyleSheet("background-color: rgb(251, 110, 255);")
        item = self.tw_supply_material.horizontalHeaderItem(3)
        item.setText("Количество")

    def add_material(self):
        self.add_mat = AddAccessories(self)
        self.add_mat.set_settings()
        self.add_mat.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_mat.show()


class AddAccessories(material.AddMaterial):
    def set_settings(self):
        self.toolBar.setStyleSheet("background-color: rgb(251, 110, 255);")
        self.pb_add_material.setText("Добавить фурнитуру")
        item = self.tw_position.horizontalHeaderItem(0)
        item.setText("Фурнитура")

    def add_materia_pozition(self):
        if not self.save:
            self.save = True
        self.add_mat_poz = AddAccessoriesPosition(self)
        set_win = {"WinTitle": "Добавление фурнитуры",
                   "WinColor": "(251, 110, 255)",
                   "lb_value": "Кол-во",
                   "lb_name": "Фурнитура"}
        self.add_mat_poz.set_settings(set_win)
        self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_mat_poz.show()

    def double_click(self, i):
        if not self.save:
            self.save = True
        collor = self.tw_position.item(i, 0).background().color().red()
        name = self.tw_position.item(i, 0).text()
        value = self.tw_position.item(i, 1).text()
        price = self.tw_position.item(i, 2).text()
        summ = self.tw_position.item(i, 3).text()

        if collor == 252:
            self.add_mat_poz = AddAccessoriesPosition(self)
            set_win = {"WinTitle": "Добавление фурнитуры",
                   "WinColor": "(251, 110, 255)",
                   "lb_value": "Кол-во",
                   "lb_name": "Фурнитура"}
            self.add_mat_poz.set_settings(set_win)
            self.add_mat_poz.set_meaning((name, value, price, summ), i)
            self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
            self.add_mat_poz.show()
        elif collor == 221:
            self.add_mat_poz = material.AddComparingPosition(self)
            self.add_mat_poz.set_settings("Редактирование прочих растрат", "Изменить")
            self.add_mat_poz.set_meaning((name, value, price, summ), i)
            self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
            self.add_mat_poz.show()

    def view_name_provider(self):
        if not self.save:
            self.save = True
        self.view_provider = accessories_provider.AccessoriesProvider(self, True)
        self.view_provider.setWindowModality(QtCore.Qt.ApplicationModal)
        self.view_provider.show()

    def add_material_sql(self):
        query = "INSERT INTO avi_crm.accessories_supply (Accessories_ProviderId, Data, Note) SELECT Id, %s, %s FROM avi_crm.accessories_provider WHERE Name=%s"
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
            if color == 252:
                self.material.append((self.id_supply, self.value, self.price, self.name))
            elif color == 221:
                self.comparing.append((self.id_supply, self.value, self.price, self.name))

        if self.material:
            query = "INSERT INTO avi_crm.accessories_supplyposition (Accessories_SupplyId, Accessories_NameId, Value, Price) SELECT %s, Id, %s, %s FROM accessories_name WHERE Name = %s"
            sql_ret = my_sql.sql_many(query, self.material)
            if "mysql.connector.errors" in str(type(sql_ret)):
                QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)

        if self.comparing:
            query = "INSERT INTO avi_crm.comparing_supplyposition (Accessories_SupplyId, Comparing_NameId, Value, Price) SELECT %s, Id, %s, %s FROM comparing_name WHERE Name = %s"
            sql_ret = my_sql.sql_many(query, self.comparing)
            if "mysql.connector.errors" in str(type(sql_ret)):
                QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)

        if self.save:
            self.save = False
        self.close()
        self.destroy()
        self.main.view_supply()


class AccessoriesChangeSupply(material.ChangeSupply, AddAccessories):
    def set_supply_info(self):
        query = """SELECT accessories_supply.Id, accessories_provider.Name, Data, Note,  accessories_SupplyPosition.Id, accessories_name.Name,
                accessories_supplyposition.Price, accessories_supplyposition.Value, accessories_balance.BalanceValue
                FROM accessories_supply LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.accessories_SupplyId
                LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.accessories_SupplyPositionId
                LEFT JOIN accessories_name ON accessories_supplyposition.accessories_NameId = accessories_name.Id
                LEFT JOIN accessories_provider ON accessories_supply.accessories_ProviderId = accessories_provider.Id WHERE accessories_supply.Id =  %s"""
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
                color = (252, 163, 255)

            elif row[8] == 0:
                color = (254, 123, 123)

            else:
                color = (255, 255, 127)

            self.add_pozition(position, color)

        query = """SELECT IFNULL(comparing_supplyposition.Id, 'SQL_Пуст'), comparing_name.Name, comparing_supplyposition.Price, comparing_supplyposition.Value
                FROM accessories_supply LEFT JOIN comparing_supplyposition ON accessories_supply.Id = comparing_supplyposition.accessories_SupplyId
                LEFT JOIN comparing_name ON comparing_supplyposition.Comparing_NameId = comparing_name.Id WHERE accessories_supply.Id =  %s"""
        supply_comparing = my_sql.sql_select(query, (self.id_supply, ))
        if "mysql.connector.errors" in str(type(supply_comparing)):
            QMessageBox.critical(self, "Ошибка sql", supply_comparing.msg, QMessageBox.Ok)

        if "SQL_Пуст" not in supply_comparing[0]:
            for row in supply_comparing:
                position = [row[1], row[3], row[2], round(row[3]*row[2], 4), row[3], row[0]]
                color = (221, 255, 204)
                self.add_pozition(position, color)
        self.save = False

    def add_material_sql(self):
        query = """SELECT accessories_provider.Name, accessories_supply.Data, accessories_supply.Note
                FROM accessories_supply LEFT JOIN accessories_provider ON accessories_supply.accessories_ProviderId = accessories_provider.Id
                WHERE accessories_supply.Id = %s"""
        supply = my_sql.sql_select(query, (self.id_supply, ))
        if "mysql.connector.errors" in str(type(supply)):
            QMessageBox.critical(self, "Ошибка sql", supply.msg, QMessageBox.Ok)

        query = """SELECT CAST(accessories_supplyposition.Id AS CHAR(11)), accessories_name.Name, accessories_supplyposition.Value, accessories_supplyposition.Price
                FROM accessories_supply LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.accessories_SupplyId
                LEFT JOIN accessories_name ON accessories_supplyposition.accessories_NameId = accessories_name.Id WHERE accessories_supply.Id = %s"""
        supply_material = my_sql.sql_select(query, (self.id_supply, ))
        if "mysql.connector.errors" in str(type(supply_material)):
            QMessageBox.critical(self, "Ошибка sql", supply_material.msg, QMessageBox.Ok)

        query = """SELECT IFNULL(comparing_supplyposition.Id, 'Пустой_SQL'), comparing_name.Name, comparing_supplyposition.Value, comparing_supplyposition.Price
                FROM accessories_supply LEFT JOIN comparing_supplyposition ON accessories_supply.Id = comparing_supplyposition.accessories_SupplyId
                LEFT JOIN comparing_name ON comparing_supplyposition.Comparing_NameId = comparing_name.Id WHERE accessories_supply.Id =  %s"""
        supply_comparing = my_sql.sql_select(query, (self.id_supply, ))
        if "mysql.connector.errors" in str(type(supply_comparing)):
            QMessageBox.critical(self, "Ошибка sql", supply_comparing.msg, QMessageBox.Ok)

        if self.le_provider.text() != supply[0][0] or self.de_data.date() != supply[0][1] or self.le_note.text() != supply[0][2]:
            query = "SELECT Id FROM accessories_provider WHERE Name = %s"
            provider = my_sql.sql_select(query, (self.le_provider.text(), ))
            if "mysql.connector.errors" in str(type(provider)):
                QMessageBox.critical(self, "Ошибка sql", provider.msg, QMessageBox.Ok)

            query = "UPDATE  accessories_supply SET accessories_ProviderId = %s, Data = %s, Note = %s WHERE Id = %s"
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
                                    query = "SELECT BalanceValue FROM accessories_balance WHERE accessories_SupplyPositionId = %s"
                                    balance = my_sql.sql_select(query, (sypply_position[0], ))
                                    if "mysql.connector.errors" in str(type(balance)):
                                        QMessageBox.critical(self, "Ошибка sql", balance.msg, QMessageBox.Ok)
                                        flag_break = True
                                        break
                                    query = """UPDATE accessories_supplyposition SET
                                    Accessories_NameId = (SELECT Id FROM avi_crm.accessories_name WHERE Name = %s),
                                    Value = %s, Price = %s WHERE Id = %s"""
                                    sql_re = my_sql.sql_change(query, (sypply_position[1], sypply_position[2],
                                                                       sypply_position[3], sypply_position[0]))
                                    if "mysql.connector.errors" in str(type(sql_re)):
                                        QMessageBox.critical(self, "Ошибка sql", sql_re.msg, QMessageBox.Ok)
                                        flag_break = True
                                        break

                                    query = """UPDATE accessories_balance SET BalanceValue = %s
                                               WHERE accessories_SupplyPositionId = %s """
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
                            query = """INSERT INTO avi_crm.accessories_supplyposition (accessories_SupplyId, accessories_NameId, Value, Price)
                                        SELECT %s, Id, %s, %s FROM accessories_name WHERE Name = %s"""
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
                            query = """INSERT INTO avi_crm.comparing_supplyposition (accessories_SupplyId, Comparing_NameId, Value, Price)
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
                elif item[0] == 252:
                    query = "DELETE FROM accessories_supplyposition WHERE Id = %s"
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

    def double_click(self, i):
        if not self.save:
            self.save = True
        collor = self.tw_position.item(i, 0).background().color().red()
        name = self.tw_position.item(i, 0).text()
        value = self.tw_position.item(i, 1).text()
        price = self.tw_position.item(i, 2).text()
        summ = self.tw_position.item(i, 3).text()

        if collor == 221:
            self.add_mat_poz = material.AddComparingPosition(self)
            self.add_mat_poz.set_settings("Редактирование прочих растрат", "Изменить")
            self.add_mat_poz.set_meaning((name, value, price, summ), i)
            self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
            self.add_mat_poz.show()
        else:
            self.add_mat_poz = AddAccessoriesPosition(self)
            set_win = {"WinTitle": "Добавление фурнитуры",
                   "WinColor": "(251, 110, 255)",
                   "lb_value": "Кол-во",
                   "lb_name": "Фурнитура"}
            self.add_mat_poz.set_settings(set_win)
            self.add_mat_poz.set_meaning((name, value, price, summ), i)
            self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
            self.add_mat_poz.show()


class AddAccessoriesPosition(material.AddMaterialPosition):
    def view_material_name(self):
        self.mat_name = accessories_provider.AccessoriesName(self, True)
        self.mat_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.mat_name.show()

    def set_settings(self, setting):
        self.collor = (252, 163, 255)
        for name, value in setting.items():
            if name == "WinTitle":
                self.setWindowTitle(value)
            elif name == "WinColor":
                self.widget.setStyleSheet("background-color: rgb%s;" % value)
            else:
                getattr(self, name).setText(value)
