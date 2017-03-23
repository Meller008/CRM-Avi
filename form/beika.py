from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from decimal import Decimal
from math import fabs

from function import my_sql
from form.templates import table, list
from form import supply_accessories, supply_material, staff


beika_settings = loadUiType(getcwd() + '/ui/beika_settings.ui')[0]
beika = loadUiType(getcwd() + '/ui/beika.ui')[0]

# ID поставщика Авидевелопмент в фурнитуре
SUPPLY_PROVIDER_ID = 9


class BeikaList(table.TableList):
    def set_settings(self):

        self.setWindowTitle("Нарезка бейки")  # Имя окна
        self.resize(700, 270)
        self.pb_copy.deleteLater()
        self.pb_filter.deleteLater()
        self.pb_other.setText("Настройки")
        self.toolBar.setStyleSheet("background-color: rgb(255, 203, 219);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("№", 40), ("Швея", 170), ("Материал", 190), ("Кол-во", 80), ("Дата", 80), ("Одобрено", 70))

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT beika.Id, beika.Id, CONCAT(w.Last_Name, ' ', w.First_Name), material_name.Name, beika.Value, beika.Date,
                                        IF(beika.Finished = 1, 'Да', 'Нет')
                                      FROM beika LEFT JOIN material_name ON beika.Material_Id = material_name.Id
                                        LEFT JOIN staff_worker_info AS w ON beika.Worker_Id = w.Id"""

        self.query_table_dell = "DELETE FROM beika WHERE Id = %s"

    def ui_add_table_item(self):  # Добавить предмет
        self.beika = Beika(self)
        self.beika.setModal(True)
        self.beika.show()

    def ui_double_click_table_item(self, item):  # Двойной клик по элементу
        if not self.dc_select:
            self.ui_change_table_item(item.data(5))
        else:
            # что хотим получить ставим всместо 0
            item = (self.table_widget.item(item.row(), 4).text(), item.data(5))
            self.main.of_tree_select_order(item)
            self.close()
            self.destroy()

    def ui_change_table_item(self, id=False):  # изменить элемент
        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите элемент который хотите изменить", QMessageBox.Ok)
                return False

        self.order = Beika(self, item_id)
        self.order.setModal(True)
        self.order.show()

    def ui_other(self):
        self.settings = BeikaSettings()
        self.settings.setModal(True)
        self.settings.show()


class BeikaSettings(QDialog, beika_settings):
    def __init__(self):
        super(BeikaSettings, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        query = "SELECT Id, Name FROM accessories_name WHERE For_Beika = 1"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения разрешеной фурнитуры", sql_info.msg, QMessageBox.Ok)
            return False

        if len(sql_info) > 1:
            QMessageBox.critical(self, "Ошибка фурнитуры", "Выбрано 2 фурнитуры! Это не правильно!", QMessageBox.Ok)
            self.close()
            self.destroy()
            return False

        elif len(sql_info) == 1:
            self.le_accessories_name.setWhatsThis(str(sql_info[0][0]))
            self.le_accessories_name.setText(str(sql_info[0][1]))

        elif len(sql_info) == 0:
            self.le_accessories_name.setWhatsThis("None")
            self.le_accessories_name.setText("None")

        query = "SELECT Id, Name FROM material_name WHERE For_Beika = 1 ORDER BY Name"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения разрешеной ткани", sql_info.msg, QMessageBox.Ok)
            return False

        self.lw_material_name.clear()

        for material in sql_info:
            item = QListWidgetItem(material[1])
            item.setData(-1, material[0])
            self.lw_material_name.addItem(item)

    def ui_view_accessories_name(self):
        self.accessories_name = supply_accessories.AccessoriesName(self, True)
        self.accessories_name.setWindowModality(Qt.ApplicationModal)
        self.accessories_name.show()

    def ui_add_material(self):
        self.material_name = supply_material.MaterialName(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_del_material(self):
        id = self.lw_material_name.selectedItems()[0].data(-1)
        query = "UPDATE material_name SET For_Beika = 0 WHERE Id = %s"
        sql_info = my_sql.sql_change(query, (id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql удаления ткани", sql_info.msg, QMessageBox.Ok)
            return False

        self.set_start_settings()

    def ui_acc(self):
        self.close()
        self.destroy()

    def of_list_accessories_name(self, accessories):
        if self.le_accessories_name.whatsThis() != "None":
            query = "UPDATE accessories_name SET For_Beika = 0 WHERE Id = %s"
            sql_info = my_sql.sql_change(query, (self.le_accessories_name.whatsThis(), ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql удаления разрешеной фурнитуры", sql_info.msg, QMessageBox.Ok)
                return False

        query = "UPDATE accessories_name SET For_Beika = 1 WHERE Id = %s"
        sql_info = my_sql.sql_change(query, (accessories[0], ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql добавления разрешеной фурнитуры", sql_info.msg, QMessageBox.Ok)
            return False

        self.le_accessories_name.setText(str(accessories[1]))
        self.le_accessories_name.setWhatsThis(str(accessories[0]))

    def of_list_material_name(self, item):
        query = "UPDATE material_name SET For_Beika = 1 WHERE Id = %s"
        sql_info = my_sql.sql_change(query, (item[0],))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql добавления ткани", sql_info.msg, QMessageBox.Ok)
            return False

        self.set_start_settings()


class Beika(QDialog, beika):
    def __init__(self, main, id=False):
        super(Beika, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        self.id = id
        self.change = False

        self.set_start_settings()
        self.change = False

    def set_start_settings(self):
        if self.id:
            query = """SELECT staff_worker_info.Id, staff_worker_info.Last_Name, material_name.Id, material_name.Name, accessories_name.Id,
                            accessories_name.Name, beika.Value, beika.Date, beika.Finished
                          FROM beika LEFT JOIN material_name ON beika.Material_Id = material_name.Id
                            LEFT JOIN accessories_name ON beika.Accessories_Id = accessories_name.Id
                            LEFT JOIN staff_worker_info ON beika.Worker_Id = staff_worker_info.Id
                          WHERE beika.Id = %s"""
            sql_info = my_sql.sql_select(query, (self.id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения информации о нарезке", sql_info.msg, QMessageBox.Ok)
                return False

            self.le_worker.setWhatsThis(str(sql_info[0][0]))
            self.le_worker.setText(sql_info[0][1])

            self.le_material.setWhatsThis(str(sql_info[0][2]))
            self.le_material.setText(sql_info[0][3])

            self.le_accessories_name.setWhatsThis(str(sql_info[0][4]))
            self.le_accessories_name.setText(sql_info[0][5])

            self.le_value.setText(str(sql_info[0][6]))

            self.de_date.setDate(sql_info[0][7])

            if sql_info[0][8] == 1:
                self.cb_ok.setChecked(True)
                self.sql_finish = True
                self.toolButton_2.setEnabled(False)
                self.toolButton.setEnabled(False)
                self.le_value.setEnabled(False)
                self.de_date.setEnabled(False)

            else:
                self.sql_finish = False

        else:
            query = "SELECT Id, Name FROM accessories_name WHERE For_Beika = 1"
            sql_info = my_sql.sql_select(query)
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения разрешеной фурнитуры", sql_info.msg, QMessageBox.Ok)
                return False

            if len(sql_info) > 1:
                QMessageBox.critical(self, "Ошибка фурнитуры", "Выбрано 2 фурнитуры! Это не правильно!", QMessageBox.Ok)
                self.close()
                self.destroy()
                return False

            elif len(sql_info) == 1:
                self.le_accessories_name.setWhatsThis(str(sql_info[0][0]))
                self.le_accessories_name.setText(str(sql_info[0][1]))

            elif len(sql_info) == 0:
                QMessageBox.critical(self, "Ошибка фурнитуры", "Не выбрана стандартная фернитура!", QMessageBox.Ok)
                self.close()
                self.destroy()
                return False

            self.de_date.setDate(QDate.currentDate())

            self.sql_finish = False

    def ui_view_worker(self):
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_view_material(self):
        self.material_name = MaterialBeika(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_change_beika(self):
        self.change = True

    def ui_acc(self):
        if self.change:
            if not self.id:
                query = """INSERT INTO beika (Material_Id, Accessories_Id, Date, Value, Finished, Worker_Id)
                            VALUES (%s, %s, %s, %s, %s, %s)"""
                sql_value = (self.le_material.whatsThis(), self.le_accessories_name.whatsThis(), self.de_date.date().toString(Qt.ISODate),
                             self.le_value.text(), 0, self.le_worker.whatsThis())
                sql_info = my_sql.sql_change(query, sql_value)
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql при добавлении нарезки бейки", sql_info.msg, QMessageBox.Ok)
                    return False

                self.id = sql_info

            else:
                query = """UPDATE beika SET Material_Id = %s, Accessories_Id = %s, Date = %s, Value = %s, Worker_Id = %s WHERE Id = %s"""
                sql_value = (self.le_material.whatsThis(), self.le_accessories_name.whatsThis(), self.de_date.date().toString(Qt.ISODate),
                             self.le_value.text(), self.le_worker.whatsThis(), self.id)
                sql_info = my_sql.sql_change(query, sql_value)
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql при изменении нарезки бейки", sql_info.msg, QMessageBox.Ok)
                    return False

        if self.id and self.sql_finish != self.cb_ok.isChecked():
            if not self.sql_finish and self.cb_ok.isChecked():
                # Нарезку подтвердили
                # Проверим остаток склада
                query = """SELECT SUM(material_balance.BalanceWeight)
                                FROM material_balance
                                  LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                WHERE material_supplyposition.Material_NameId = %s"""
                sql_info = my_sql.sql_select(query, (self.le_material.whatsThis(), ))
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql при получении остатка склада", sql_info.msg, QMessageBox.Ok)
                    return False

                if sql_info[0][0] is None or Decimal(self.le_value.text()) > sql_info[0][0]:
                    QMessageBox.critical(self, "Ошибка", "Не хватает ткани на складе для нарезки", QMessageBox.Ok)
                    return False

                sql_connect_transaction = my_sql.sql_start_transaction()
                material_id = int(self.le_material.whatsThis())
                change_value = Decimal(self.le_value.text())
                price_list = []
                while change_value > 0:
                    # получим первый остаток на складе
                    # Проверяем первое кол-во на складе
                    query = """SELECT material_balance.Id, material_balance.BalanceWeight, MIN(material_supply.Data), material_supplyposition.Price
                                    FROM material_balance
                                      LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                      LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                    WHERE material_supplyposition.Material_NameId = %s AND material_balance.BalanceWeight > 0"""
                    sql_balance_material = my_sql.sql_select_transaction(sql_connect_transaction, query, (material_id, ))
                    if "mysql.connector.errors" in str(type(sql_balance_material)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        QMessageBox.critical(self, "Ошибка сохранения ткани", "Не смог получить остаток ткани на балансе (Это плохо к админу)", QMessageBox.Ok)
                        return False

                    if sql_balance_material[0][1] > change_value:
                        # Если в этом балансе больше чем нам надо
                        take_material_value = change_value
                        change_value = 0
                    else:
                        # Если в этом балансе меньше чем нам надо
                        take_material_value = sql_balance_material[0][1]
                        change_value -= sql_balance_material[0][1]

                    # Забираем возможное кол-во
                    query = "UPDATE material_balance SET BalanceWeight = BalanceWeight - %s WHERE Id = %s"
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (take_material_value, sql_balance_material[0][0]))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        QMessageBox.critical(self, "Ошибка сохранения ткани", "Не смог забрать ткань с баланса (Это плохо к админу)", QMessageBox.Ok)
                        return False

                    # Делаем запись о заборе ткани с баланса склада
                    query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Beika_Id)
                                  VALUES (%s, %s, SYSDATE(), %s, %s)"""
                    txt_note = "На нарезку бейки №%s" % self.id
                    sql_values = (sql_balance_material[0][0], -take_material_value, txt_note, self.id)
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        QMessageBox.critical(self, "Ошибка сохранения ткани", "Не смог добавить запись при заборе ткани (Это плохо к админу)", QMessageBox.Ok)
                        return False

                    price_list.append((take_material_value, sql_balance_material[0][3]))

                # если ткань забрали успешно то начнем забивать приход
                # Узнаем среднюю цену avg = (p*v) + (p2*v2) + ... / v + v1 ...
                up = 0
                down = 0
                for item in price_list:
                    up += item[0] * item[1]
                    down += item[0]

                avg_price = up / down

                # Добавим приход фурнитуры
                query = "INSERT INTO accessories_supply (Accessories_ProviderId, Data, Note) VALUES (%s, NOW(), %s)"
                txt_note = "Приход с нарезки бейки №%s" % self.id
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (SUPPLY_PROVIDER_ID, txt_note))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка сохранения прихода", "Не смог сделать приход фурнитуры", QMessageBox.Ok)
                    return False

                supply_id = sql_info
                if not supply_id:
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка сохранения прихода", "Не получил id прихода фурнитуры", QMessageBox.Ok)
                    return False

                query = "INSERT INTO accessories_supplyposition (Accessories_SupplyId, Accessories_NameId, Value, Price) VALUES (%s, %s, %s, %s)"
                sql_value = (supply_id, self.le_accessories_name.whatsThis(), down, avg_price)
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка сохранения прихода", "Не смог сделать позицию прихода", QMessageBox.Ok)
                    return False

                supply_position_id = sql_info
                if not supply_id:
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка сохранения прихода", "Не получил id позиции прихода фурнитуры", QMessageBox.Ok)
                    return False

                # Получим ID баланса через ID позиции прихода
                query = """SELECT accessories_balance.Id
                                FROM accessories_balance
                                  LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                                WHERE accessories_supplyposition.Id = %s"""
                sql_info = my_sql.sql_select_transaction(sql_connect_transaction, query, (supply_position_id, ))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка сохранения прихода", "Не смог получить ID баланса через позицию прихода", QMessageBox.Ok)
                    return False

                query = """INSERT INTO transaction_records_accessories (Supply_Balance_Id, Balance, Date, Note, Pack_Accessories_Id)
                                  VALUES (%s, %s, SYSDATE(), %s, NULL)"""
                txt_note = "Нарезка бейки №%s" % self.id
                sql_value = (sql_info[0][0], down, txt_note)
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка сохранения прихода", "Не смог сделать позицию прихода", QMessageBox.Ok)
                    return False

                query = """UPDATE beika SET Finished = %s, Supply_Id = %s WHERE Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (1, supply_id, self.id))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при изменении строки принятия в нарезке бейки", sql_info.msg, QMessageBox.Ok)
                    return False

                my_sql.sql_commit_transaction(sql_connect_transaction)

            elif self.sql_finish and not self.cb_ok.isChecked():
                # Нарезку отменили
                # Проверим не трогался ли ее баланс
                query = """SELECT beika.Value, accessories_supplyposition.Value, accessories_balance.BalanceValue
                              FROM beika LEFT JOIN accessories_supply ON beika.Supply_Id = accessories_supply.Id
                                LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.Accessories_SupplyId
                                LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.Accessories_SupplyPositionId
                              WHERE beika.Id = %s"""
                sql_info = my_sql.sql_select(query, (self.id,))
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql при получении баланса это нарезки", sql_info.msg, QMessageBox.Ok)
                    return False

                if sql_info[0][0] == sql_info[0][1] == sql_info[0][2]:
                    pass
                else:
                    QMessageBox.critical(self, "Ошибка", "Не равны балансы, скорее всего бейка в работе", QMessageBox.Ok)
                    return False

                # Получим Id Supply + Id Supply_position + Balance_Id
                query = """SELECT accessories_supply.Id, accessories_supplyposition.Id, accessories_balance.Id
                              FROM beika LEFT JOIN accessories_supply ON beika.Supply_Id = accessories_supply.Id
                                LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.Accessories_SupplyId
                                LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.Accessories_SupplyPositionId
                              WHERE beika.Id = %s"""
                sql_info_id = my_sql.sql_select(query, (self.id,))
                if "mysql.connector.errors" in str(type(sql_info_id)):
                    QMessageBox.critical(self, "Ошибка sql при получении ID баланса", sql_info_id.msg, QMessageBox.Ok)
                    return False

                sql_connect_transaction = my_sql.sql_start_transaction()

                # Удалим все упоминания о этой нарезке бейки!
                query = """DELETE FROM transaction_records_accessories WHERE Supply_Balance_Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (sql_info_id[0][2],))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при Удалении записей баланмса фурнитуры", sql_info.msg, QMessageBox.Ok)
                    return False

                query = """DELETE FROM accessories_balance WHERE Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (sql_info_id[0][2],))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при Удалении баланса фурнитуры", sql_info.msg, QMessageBox.Ok)
                    return False

                query = """DELETE FROM accessories_supplyposition WHERE Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (sql_info_id[0][1],))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при Удалении позиции прихода фурнитуры", sql_info.msg, QMessageBox.Ok)
                    return False

                query = """DELETE FROM accessories_supply WHERE Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (sql_info_id[0][0],))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при Удалении прихода фурнитуры", sql_info.msg, QMessageBox.Ok)
                    return False

                # Вернем ткань
                # Берем сумму списаний сгрупированную по id баланса
                query = """SELECT SUM(transaction_records_material.Balance), transaction_records_material.Supply_Balance_Id, material_supplyposition.Material_NameId
                                 FROM transaction_records_material
                                   LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                                   LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                 WHERE transaction_records_material.Beika_Id = %s
                                 GROUP BY transaction_records_material.Supply_Balance_Id"""
                sql_info = my_sql.sql_select_transaction(sql_connect_transaction, query, (self.id,))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql Не смог получить сумму списаний сгрупированную по id баланса при удалении", sql_info.msg, QMessageBox.Ok)
                    return False

                if sql_info[0][0] is not None:
                    transaction_list = sql_info
                else:
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Нету суммы списаний сгрупированной по id баланса при удалении", sql_info.msg, QMessageBox.Ok)
                    return False

                # Начинаем перебор списка списаний
                return_material = 0
                for transaction_id_all in transaction_list:
                    if transaction_id_all[0] != 0:
                        # возвращаем фурнитуру на баланс склада
                        query = "UPDATE material_balance SET BalanceWeight = BalanceWeight + %s WHERE Id = %s"
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (-transaction_id_all[0], transaction_id_all[1]))
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql Не смог вернуть ткань на баланс склада при удалении", sql_info.msg, QMessageBox.Ok)
                            return False

                        # Делаем запись о возырате ткани на баланс склада
                        query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Beika_Id)
                                         VALUES (%s, %s, SYSDATE(), %s, %s)"""
                        txt_note = "Отмена нарезки бейки №%s" % self.id
                        sql_values = (transaction_id_all[1], -transaction_id_all[0], txt_note, self.id)
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql Не смог добавить запись при возврате ткани удаление", sql_info.msg, QMessageBox.Ok)
                            return False

                        return_material += -transaction_id_all[0]

                if fabs(return_material - Decimal(self.le_value.text())) > Decimal(str(0.0005)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql Возвратная ткань не равна сумме кроя", sql_info.msg, QMessageBox.Ok)
                    return False

                query = """UPDATE beika SET Finished = %s, Supply_Id = %s WHERE Id = %s"""
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (0, None, self.id))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    QMessageBox.critical(self, "Ошибка sql при изменении строки принятия при отмене нарезки", sql_info.msg, QMessageBox.Ok)
                    return False

                my_sql.sql_commit_transaction(sql_connect_transaction)

        self.main.ui_update()
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()

    def of_list_worker(self, item):
        self.le_worker.setWhatsThis(str(item[0]))
        self.le_worker.setText(item[1])

    def of_list_insert_material_beika(self, item):
        self.le_material.setWhatsThis(str(item[0]))
        self.le_material.setText(item[1])


class MaterialBeika(list.ListItems):
    def set_settings(self):
        self.setWindowTitle("Список тканей")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(255, 203, 219);")  # Цвет бара
        self.title_new_window = "Предмет"  # Имя вызываемых окон

        self.pb_add.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_change.deleteLater()

        self.sql_list = "SELECT Id, Name FROM material_name WHERE For_Beika = 1 ORDER BY Name"
        self.sql_add = "Вставляем Имя + Заметку"
        self.sql_change_select = "Получаем Имя + заметку через ID"
        self.sql_update_select = 'Меняем Имя + заметку через ID'
        self.sql_dell = "Удаляем строку через ID"

        self.set_new_win = {"WinTitle": "Предмет",
                            "WinColor": "(255, 255, 255)",
                            "lb_name": "Название",
                            "lb_note": "Заметка"}

    def ui_double_click_item(self, select_prov):
        if not self.dc_select:
            pass
        else:
            item = (select_prov.data(3), select_prov.text())
            self.m_class.of_list_insert_material_beika(item)
            self.close()
            self.destroy()