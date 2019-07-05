from function import my_sql
from PyQt5.QtCore import QDate
from datetime import datetime
from decimal import *
from math import fabs


class Cut:
    def __init__(self, id_сut=None):
        self.__id = None
        self.__date_cut = None
        self.__worker_id = None
        self.__worker_name = None
        self.__weight = 0
        self.__weight_rest = 0
        self.__weight_rest_old = 0
        self.__weight_all = None
        self.__percent_rest = 0
        self.__note = None
        self.__complete = None
        self.__pack_id_dict = None
        self.__material_id = None
        self.__material_id_old_sql = None
        self.__material_name = None
        self.__material_price = None
        self.__number = None
        self.__print_passport = False
        self.__pack_value = 0

        self.__save_sql_info = False

        self.__change_cut_weight = True  # Показывает можно ли менять вес ткани в этом крое
        self.__error_value_material = False
        if id_сut is not None:
            self.take_sql_info(int(id_сut))

    # sql функции
    def take_sql_info(self, sql_id=None):
        if sql_id is None and self.__id is None:
            print("Не верный ID")
            return False
        query = """SELECT cut.Id, cut.Date_Cut, cut.Worker_Id, staff_worker_info.Last_Name, Weight_Pack_All, cut.Weight_Rest, cut.Note,
                        CASE
                          WHEN SUM(IF(pack.Date_Coplete IS NULL, 1, 0)) > 0 THEN '0'
                          ELSE '1'
                        END,
                        Material_Id, material_name.Name, cut.Print_passport, Pack_Value, Rest_Percent
                      FROM cut
                        LEFT JOIN pack ON cut.Id = pack.Cut_Id
                        LEFT JOIN material_name ON cut.Material_Id = material_name.Id
                        LEFT JOIN staff_worker_info ON cut.Worker_Id = staff_worker_info.Id
                      WHERE cut.Id = %s"""
        sql_info = my_sql.sql_select(query, (sql_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить данные кроя")
            return False

        self.__id = sql_info[0][0]
        self.__number = sql_info[0][0]
        self.__date_cut = sql_info[0][1]
        self.__worker_id = sql_info[0][2]
        self.__worker_name = sql_info[0][3]
        self.__weight = sql_info[0][4] if sql_info[0][4] is not None else 0
        self.__weight_rest = sql_info[0][5]
        self.__weight_rest_old = sql_info[0][5]
        self.__note = sql_info[0][6]
        if sql_info[0][7] == '1':
            self.__complete = True
        else:
            self.__complete = False
        self.__material_id = sql_info[0][8]
        self.__material_id_old_sql = sql_info[0][8]
        self.__material_name = sql_info[0][9]
        self.__print_passport = sql_info[0][10]
        self.__pack_value = sql_info[0][11]
        self.__percent_rest = sql_info[0][12]

        self.take_material_price()
        self.calc_width()

        return True

    def take_pack_sql(self):
        if self.__id is None:
            print("Не верный ID 1")
            return False
        query = """SELECT pack.Id
                    FROM cut
                      LEFT JOIN pack ON cut.Id = pack.Cut_Id
                    WHERE cut.Id = %s"""
        sql_info = my_sql.sql_select(query, (self.__id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить id пачек в крое")
            return False

        self.__pack_id_dict = {}
        if sql_info[0][0] is not None:
            for id_pack in sql_info:
                self.__pack_id_dict[id_pack[0]] = Pack(id_pack[0])

        return True

    def take_new_number(self):
        query = """SELECT `AUTO_INCREMENT` FROM  INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'avi_crm' AND TABLE_NAME   = 'cut';"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог получить новый номер кроя")
        self.__number = sql_info[0][0]
        return sql_info[0][0]

    def take_material_price(self):
        query = """SELECT  ROUND(SUM(-transaction_records_material.Balance * material_supplyposition.Price) / SUM(-transaction_records_material.Balance), 4)
                      FROM transaction_records_material
                      LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                      LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Cut_Material_Id = %s"""
        sql_info = my_sql.sql_select(query, (self.__id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить данные кроя")
            return False
        if sql_info[0][0] is not None:
            self.__material_price = sql_info[0][0]
        else:
            self.__material_price = 0

    def new_save(self):
        if self.__material_id is None:
            raise RuntimeError("Не выбрана ткань для сохранения кроя!")
        sql_values = (self.__date_cut, self.__worker_id, 0, self.__note, self.__material_id, self.__material_price, self.__weight, self.__pack_value, self.__percent_rest)
        query = """INSERT INTO cut (Date_Cut, Worker_Id, Weight_Rest, Note, Material_Id, Material_Price, Print_passport, Weight_Pack_All, Pack_Value, Rest_Percent) VALUES
                                  (%s, %s, %s, %s, %s, %s, 0, %s, %s, %s)"""
        sql_info = my_sql.sql_change(query, sql_values)
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог сохранить пустой крой!")

        self.__id = sql_info
        return sql_info

    def save_sql(self):
        if self.__save_sql_info:
            if self.__material_id is None:
                raise RuntimeError("Не выбрана ткань для сохранения кроя!")
            if self.__id is None:
                # Это новый крой
                sql_values = (self.__date_cut, self.__worker_id, 0, self.__note, self.__material_id, self.__material_price, self.print_passport_int(),
                              self.__weight, self.__pack_value, self.__percent_rest)
                query = """INSERT INTO cut (Date_Cut, Worker_Id, Weight_Rest, Note, Material_Id, Material_Price, Print_passport, Weight_Pack_All, Pack_Value, Rest_Percent) VALUES
                                          (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                sql_info = my_sql.sql_change(query, sql_values)
                if "mysql.connector.errors" in str(type(sql_info)):
                    return [False, "Не смог сохранить новый крой"]
                self.__id = sql_info
            else:
                # Это старый крой
                sql_values = (self.__date_cut, self.__worker_id, self.__note, self.__material_price, self.print_passport_int(), self.__weight,
                              self.__pack_value, self.__percent_rest, self.__id)
                query = """UPDATE cut
                              SET Date_Cut = %s, Worker_Id = %s, Note = %s, Material_Price = %s, Print_passport = %s, Weight_Pack_All = %s, Pack_Value = %s, Rest_Percent = %s
                              WHERE Id = %s"""
                sql_info = my_sql.sql_change(query, sql_values)
                if "mysql.connector.errors" in str(type(sql_info)):
                    return [False, "Не смог изменить крой"]

            # Сохраним изменения обрези
            if not self.__error_value_material:
                save_note = self.new_material_weight()
                if not save_note[0]:
                    return [False, save_note[1]]

            # Сохраним изменение вида ткани
            if self.__material_id != self.__material_id_old_sql:
                save_note = self.new_material_name()
                if not save_note[0]:
                    return [False, save_note[1]]
            else:
                query = """UPDATE cut
                              SET Material_Id = %s
                          WHERE Id = %s"""
                sql_info = sql_info = my_sql.sql_change(query, (self.__material_id, self.__id))
                if "mysql.connector.errors" in str(type(sql_info)):
                    return [False, "Не смог изменить вид ткани в крое"]
        else:
            return [True, "Крой не требуется сохранять"]

        return [True, "Крой сохранен"]

    def new_material_weight(self):
        # # Проверим сколько всего списано
        # query = """SELECT SUM(Balance) FROM transaction_records_material WHERE Cut_Material_Id = %s"""
        # sql_info = my_sql.sql_select(query, (self.__id, ))
        # if "mysql.connector.errors" in str(type(sql_info)):
        #     return [False, "Не смог получить сумму списаний ткани (Это плохо к админу)"]
        #
        # if sql_info[0][0] is not None:
        #     sum_transaction = sql_info[0][0]
        # else:
        #     sum_transaction = 0
        #
        # # Проверим Новый вес Кроя через веса пачки + обрезь
        # query = """SELECT SUM(pack.Weight) + cut.Weight_Rest
        #               FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
        #               WHERE pack.Cut_Id = %s"""
        # sql_info = my_sql.sql_select(query, (self.__id, ))
        # if "mysql.connector.errors" in str(type(sql_info)):
        #     return [False, "Не смог получить общий вес кроя (Это плохо к админу)"]
        #
        # if sql_info[0][0] is None:
        #     cut_weight = 0
        # else:
        #     cut_weight = sql_info[0][0]

        # смотрим разницу нового и старого веса обрези
        change_value = Decimal(str(self.__weight_rest)) - self.__weight_rest_old
        change_rest = change_value

        sql_connect_transaction = my_sql.sql_start_transaction()
        if change_value > 0:
            # Ткани стало больше будем забирать!
            while change_value > 0:
                # получим первый остаток на складе
                # Проверяем первое кол-во на складе
                query = """SELECT material_balance.Id, material_balance.BalanceWeight, MIN(material_supply.Data)
                              FROM material_balance
                                LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                              WHERE material_supplyposition.Material_NameId = %s AND material_balance.BalanceWeight > 0"""
                sql_balance_material = my_sql.sql_select_transaction(sql_connect_transaction, query, (self.__material_id, ))
                if "mysql.connector.errors" in str(type(sql_balance_material)):
                    return [False, "Не смог получить остаток ткани на балансе (Это плохо к админу)"]
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
                    return [False, "Не смог забрать ткань с баланса (Это плохо к админу)"]
                # Делаем запись о заборе ткани с баланса склада
                query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                            VALUES (%s, %s, SYSDATE(), %s, %s, 130)"""
                txt_note = "%s - Увеличение обрези в крое" % self.__id
                sql_values = (sql_balance_material[0][0], -take_material_value, txt_note, self.__id)
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог добавить запись при увеличении обрези ткани (Это плохо к админу)"]

            query = "UPDATE rest_warehouse SET Weight = Weight + %s"
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (change_rest, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Не смог положить обрезь на склад (Это плохо к админу)"]

            txt_note = "%s - Увеличение обрези в крое" % self.__id
            query = "INSERT INTO transaction_records_rest (Cut_Id, Date, Balance, Note) VALUES (%s, NOW(), %s, %s)"
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__id, change_rest, txt_note))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Не смог записать добавление на склад обрези (Это плохо к админу)"]

        elif change_value < 0:
            change_value = -change_value
            # Ткани стало меньше будем возвращать
            # получим записаные расходы
            query = """SELECT transaction_records_material.id, transaction_records_material.Supply_Balance_Id, SUM(transaction_records_material.Balance),
                              transaction_records_material.Date
                          FROM transaction_records_material LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                            LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                          WHERE Cut_Material_Id = %s AND material_supplyposition.Material_NameId = %s
                          GROUP BY Supply_Balance_Id
                          ORDER BY Date DESC , transaction_records_material.Id DESC """
            sql_transaction = my_sql.sql_select_transaction(sql_connect_transaction, query, (self.__id, self.__material_id))
            if "mysql.connector.errors" in str(type(sql_transaction)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Не смог получить записи расходов при уменьшении ткани (Это плохо к админу)"]
            if not sql_transaction:
                # Если нету записей об удаляемой фурнитуре
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Нету записей расходов об уменьшаемой ткани (Это плохо к админу)"]

            # проверяем сумму расходов и уменьшаемой фурнитуры
            supply_value = 0
            for row_sql_info in sql_transaction:
                supply_value += row_sql_info[2]

            if -supply_value < change_value:
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "записей об удалении со склада меньше чем возвращаемое (Это плохо к админу)"]

            # Если все сошлось то начинаем возвращать фурнитуру на склад
            for supply_row in sql_transaction:
                if change_value <= 0:
                    break

                if supply_row[2] != 0:

                    if -supply_row[2] > change_value:
                        # Если в этом балансе больше чем нам надо
                        take_material_value = change_value
                        change_value = 0
                    else:
                        # Если в этом балансе меньше чем нам надо
                        take_material_value = -supply_row[2]
                        change_value -= -supply_row[2]

                    # возвращаем фурнитуру на баланс склада
                    query = "UPDATE material_balance SET BalanceWeight = BalanceWeight + %s WHERE Id = %s"
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (take_material_value, supply_row[1]))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог вернуть ткань на баланс склада при уменьшении ткани (Это плохо к админу)"]

                    # Делаем запись о возырате ткани на баланс склада
                    query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                VALUES (%s, %s, SYSDATE(), %s, %s, 131)"""
                    txt_note = "%s - Уменьшение обрези в крое" % self.__id
                    sql_values = (supply_row[1], take_material_value, txt_note, self.__id)
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог добавить запись при уменьшении ткани (Это плохо к админу)"]

            query = "UPDATE rest_warehouse SET Weight = Weight + %s"
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (change_rest,))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Не смог забрать обрезь со склада (Это плохо к админу)"]

            txt_note = "%s - Уменьшение обрези в крое" % self.__id
            query = "INSERT INTO transaction_records_rest (Cut_Id, Date, Balance, Note) VALUES (%s, NOW(), %s, %s)"
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__id, change_rest, txt_note))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Не смог забисать забор со склада обрези (Это плохо к админу)"]

        query = "UPDATE cut SET Weight_Rest = %s WHERE Id = %s"
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__weight_rest, self.__id))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "Не смог сохранить обрезь в строку пачки (Это плохо к админу)"]

        my_sql.sql_commit_transaction(sql_connect_transaction)
        return [True, "Вес сохранен"]

    def new_material_name(self):
        if self.__weight_all != 0 and self.__weight_all is not None:
            # Смотрим записаную сумму списаний
            query = """SELECT SUM(transaction_records_material.Balance)
                          FROM transaction_records_material
                          WHERE transaction_records_material.Cut_Material_Id = %s AND transaction_records_material.Note NOT LIKE '%доп. тк%'"""
            sql_info = my_sql.sql_select(query, (self.__id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                return [False, "Не смог получить сумму списаний ткани (изменение ткани)"]

            if sql_info[0][0] is not None:
                all_transaction_value = sql_info[0][0]
            else:
                return [False, "Нету суммы списаний ткани (изменение ткани)"]

            # Смотрим вес всего кроя
            query = """SELECT SUM(pack.Weight), cut.Weight_Rest
                          FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                          WHERE cut.Id = %s"""
            sql_info = my_sql.sql_select(query, (self.__id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                return [False, "Не смог получить сумму веса пачек и обрези (изменение ткани)"]

            if sql_info[0] is None and sql_info[0][1] is None:
                return [False, "Нету суммы веса пачек и обрези (изменение ткани)"]

            if sql_info[0][0] is None:
                all_weight = sql_info[0][1]
            else:
                all_weight = sql_info[0][0] + sql_info[0][1]

            if fabs(all_weight - -all_transaction_value) > Decimal(str(0.0005)):
                return [False, "Не сходятся вес кроя и записаный вес транзакций (изменение ткани)"]

            # Берем сумму списаний сгрупированную по id баланса
            query = """SELECT SUM(transaction_records_material.Balance), transaction_records_material.Supply_Balance_Id, material_supplyposition.Material_NameId
                          FROM transaction_records_material
                            LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                            LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                          WHERE transaction_records_material.Cut_Material_Id = %s AND transaction_records_material.Note NOT LIKE '%доп. тк%'
                          GROUP BY transaction_records_material.Supply_Balance_Id"""
            sql_info = my_sql.sql_select(query, (self.__id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                return [False, "Не смог получить сумму списаний сгрупированную по id баланса (изменение ткани)"]

            if sql_info[0][0] is not None:
                transaction_list = sql_info
            else:
                return [False, "Нету суммы списаний сгрупированной по id баланса (изменение ткани)"]

            # Начинаем транзакуию и перебор списка списаний
            return_material = 0
            sql_connect_transaction = my_sql.sql_start_transaction()
            for transaction_id_all in transaction_list:
                if transaction_id_all[0] != 0 and transaction_id_all[2] != self.__material_id:
                    # возвращаем ткань на баланс склада
                    query = "UPDATE material_balance SET BalanceWeight = BalanceWeight + %s WHERE Id = %s"
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (-transaction_id_all[0], transaction_id_all[1]))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог вернуть ткань на баланс склада (изменение ткани)"]

                    # Делаем запись о возырате ткани на баланс склада
                    query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                  VALUES (%s, %s, SYSDATE(), %s, %s, 134)"""
                    txt_note = "%s - Возврат ткани из за смены ткани" % self.__id
                    sql_values = (transaction_id_all[1], -transaction_id_all[0], txt_note, self.__id)
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог добавить запись при возврате ткани (изменение ткани)"]

                    return_material += -transaction_id_all[0]

            # Начинаем списывать новую ткань
            change_value = return_material
            while change_value > 0:
                # получим первый остаток на складе
                # Проверяем первое кол-во на складе
                query = """SELECT material_balance.Id, material_balance.BalanceWeight, MIN(material_supply.Data)
                                    FROM material_balance
                                      LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                      LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                    WHERE material_supplyposition.Material_NameId = %s AND material_balance.BalanceWeight > 0"""
                sql_balance_material = my_sql.sql_select_transaction(sql_connect_transaction, query, (self.__material_id, ))
                if "mysql.connector.errors" in str(type(sql_balance_material)):
                    return [False, "Не смог получить остаток ткани на балансе (изменение ткани)"]
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
                    return [False, "Не смог забрать ткань с баланса (изменение ткани)"]
                # Делаем запись о заборе ткани с баланса склада
                query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                  VALUES (%s, %s, SYSDATE(), %s, %s, 133)"""
                txt_note = "%s - Забор ткани из за смены ткани" % self.__id
                sql_values = (sql_balance_material[0][0], -take_material_value, txt_note, self.__id)
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог добавить запись при увеличении веса ткани (изменение ткани)"]

            query = """UPDATE cut
                          SET Material_Id = %s
                          WHERE Id = %s"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__material_id, self.__id))
            if "mysql.connector.errors" in str(type(sql_info)):
                return [False, "Не смог изменить вид ткани в крое (изменение ткани)"]

            my_sql.sql_commit_transaction(sql_connect_transaction)

        else:
            # Если это просто изменение ткани без веса кроя
            query = """UPDATE cut
                              SET Material_Id = %s
                          WHERE Id = %s"""
            sql_info = my_sql.sql_change(query, (self.__material_id, self.__id))
            if "mysql.connector.errors" in str(type(sql_info)):
                return [False, "Не смог изменить вид ткани в крое (изменение ткани)"]

        return [True, "Новая ткань сохранена"]

    def check_material_weight(self):
        query = """SELECT SUM(Weight) FROM pack WHERE Cut_Id = %s"""
        sql_info = my_sql.sql_select(query, (self.__id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            return [False, "Не смог получить сумму списаний ткани (Это плохо к админу)"]

        if self.__weight != sql_info[0][0]:
            self.__save_sql_info = True

        if sql_info[0][0] is not None:
            self.__weight = sql_info[0][0]
        else:
            self.__weight = 0
        self.calc_width()

    def check_pack_value(self):
        if self.__pack_value != len(self.__pack_id_dict):
            self.__save_sql_info = True
        self.__pack_value = len(self.__pack_id_dict)

    def take_new_number_pack(self):
        if not self.__pack_id_dict:
            return 1
        else:
            query = """SELECT MAX(Number) + 1 FROM pack WHERE Cut_Id = %s"""
            sql_info = my_sql.sql_select(query, (self.__id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                return [False, "Не смог получить номер для новой пачки (Это плохо к админу)"]
            return sql_info[0][0]

    def del_sql(self):
        query = """SELECT COUNT(*) FROM pack WHERE Cut_Id = %s"""
        sql_info = my_sql.sql_select(query, (self.__id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            return [False, "Не смог проверить кол-во пачек (удаление кроя)"]

        if sql_info[0][0] > 0:
            return [False, "Есть неудаленые пачки.\nУдалите сначало пачки!"]

        # Проверим сколько всего списано
        query = """SELECT SUM(Balance) FROM transaction_records_material WHERE Cut_Material_Id = %s"""
        sql_info = my_sql.sql_select(query, (self.__id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            return [False, "Не смог получить сумму списаний ткани при удалении (Это плохо к админу)"]

        if sql_info[0][0] is None or fabs(-sql_info[0][0] - self.__weight_all) > Decimal(str(0.0005)):
            return [False, "Списаный баланс и удаляемы не равны (Это плохо к админу)"]

        # Берем сумму списаний сгрупированную по id баланса
        query = """SELECT SUM(transaction_records_material.Balance), transaction_records_material.Supply_Balance_Id, material_supplyposition.Material_NameId
                        FROM transaction_records_material
                          LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                          LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                        WHERE transaction_records_material.Cut_Material_Id = %s
                        GROUP BY transaction_records_material.Supply_Balance_Id"""
        sql_info = my_sql.sql_select(query, (self.__id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            return [False, "Не смог получить сумму списаний сгрупированную по id баланса при удалении (Это плохо к админу)"]

        if sql_info[0][0] is not None:
            transaction_list = sql_info
        else:
            return [False, "Нету суммы списаний сгрупированной по id баланса при удалении (Это плохо к админу)"]

        # Начинаем транзакуию и перебор списка списаний
        return_material = 0
        sql_connect_transaction = my_sql.sql_start_transaction()
        for transaction_id_all in transaction_list:
            if transaction_id_all[0] != 0 and transaction_id_all[2] == self.__material_id:
                # возвращаем фурнитуру на баланс склада
                query = "UPDATE material_balance SET BalanceWeight = BalanceWeight + %s WHERE Id = %s"
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (-transaction_id_all[0], transaction_id_all[1]))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог вернуть ткань на баланс склада при удалении кроя (Это плохо к админу)"]

                # Делаем запись о возырате ткани на баланс склада
                query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                VALUES (%s, %s, SYSDATE(), %s, %s, 132)"""
                txt_note = "%s - Возврат ткани из за удаления кроя" % self.__id
                sql_values = (transaction_id_all[1], -transaction_id_all[0], txt_note, self.__id)
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог добавить запись при возврате ткани удаление (Это плохо к админу)"]

                return_material += -transaction_id_all[0]

        if fabs(return_material - self.__weight_all) > Decimal(str(0.0005)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "Возвратная ткань не равна сумме кроя (Это плохо к админу)"]

        query = "UPDATE rest_warehouse SET Weight = Weight - %s"
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__weight_all,))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "Не смог забрать обрезь со склада (Это плохо к админу)"]

        txt_note = "%s - Удаление кроя" % self.__id
        query = "INSERT INTO transaction_records_rest (Cut_Id, Date, Balance, Note) VALUES (%s, NOW(), %s, %s)"
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__id, -self.__weight_all, txt_note))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "Не смог забисать забор со склада обрези (Это плохо к админу)"]

        query = "DELETE FROM cut WHERE Id = %s"
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "Не смог удалить крой (Это плохо к админу)"]

        my_sql.sql_commit_transaction(sql_connect_transaction)
        return [True, "Вес сохранен"]

    # Получекние значений
    def id(self):
        if self.__id:
            return int(self.__id)
        else:
            return self.__id

    def number(self):
        return self.__number

    def pack(self, id_pack):
            pack = self.__pack_id_dict.get(id_pack)
            if pack is not None:
                return pack
            else:
                print("Нет пачки с таким ID в крое")
                return False

    def material_id(self):
        return self.__material_id

    def material_name(self):
        return self.__material_name

    def material_price(self):
        return self.__material_price

    def pack_list(self):
        return self.__pack_id_dict

    def pack_value(self):
        return self.__pack_value

    def date(self):
        return self.__date_cut

    def worker_id(self):
        return self.__worker_id

    def worker_name(self):
        return self.__worker_name

    def weight(self):
        return self.__weight

    def weight_rest(self):
        return self.__weight_rest

    def weight_rest_old(self):
        return self.__weight_rest_old

    def rest_in_pack(self):
        # Проверяем получали ли мы пачки, если нет то возьмем значение полученое при получении кроя
        if self.__pack_id_dict:
            return self.__weight_rest / len(self.__pack_id_dict)
        elif self.__pack_value:
            return self.__weight_rest / self.__pack_value
        else:
            return 0

    def weight_all(self):
        return self.__weight_all

    def rest_percent(self):
        return self.__percent_rest

    def percent_rest(self):
        return self.__percent_rest

    def note(self):
        return self.__note

    def error_material(self):
        return self.__error_value_material

    def change_cut_weight(self):
        return self.__change_cut_weight

    def need_save(self):
        return self.__save_sql_info

    def print_passport(self):
        return self.__print_passport

    def print_passport_int(self):
        if self.__print_passport:
            return 1
        else:
            return 0

    # Вставка заначений
    def set_id(self):
        pass

    def set_date(self, date):
        if self.__date_cut != date:
            if isinstance(date, QDate):
                self.__date_cut = datetime.strptime(date.toString(1), "%Y-%m-%d")
                if not self.__save_sql_info:
                    self.__save_sql_info = True
            elif isinstance(date, datetime):
                self.__date_cut = date
                if not self.__save_sql_info:
                    self.__save_sql_info = True
            else:
                raise RuntimeError("Не тот тип данных!")

    def set_material_id(self, id):
        if self.__material_id != int(id):
            self.__material_id = int(id)

            if not self.__save_sql_info:
                    self.__save_sql_info = True

            if self.__pack_id_dict or self.__weight_rest_old > 0:
                self.__change_cut_weight = False
                # self.__error_value_material = True  Не знаю зачем я менял эту переменную!

            query = """SELECT Price
                        FROM material_name
                          LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                          LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                          LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                        WHERE material_name.Id = %s AND BalanceWeight > 0
                        ORDER BY Data
                        LIMIT 1"""
            sql_info = my_sql.sql_select(query, (id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                raise RuntimeError("Не смог получить цену материала")
            if sql_info:
                self.__material_price = sql_info[0][0]
                return sql_info[0][0]
            else:
                return None

    def set_material_id_old(self, id):
        if self.__material_id_old_sql != int(id):
            self.__material_id_old_sql = int(id)

    def set_worker_id(self, id):
        if id == "None":
            self.__worker_id = None

        elif self.__worker_id != int(id):
            self.__worker_id = int(id)

            if not self.__save_sql_info:
                    self.__save_sql_info = True

    def set_note(self, note):
        if self.__note != str(note):
            self.__note = str(note)

            if not self.__save_sql_info:
                    self.__save_sql_info = True

    def set_weight_rest(self, weight):
        if weight == "":
            weight = "0"
        if self.__weight_rest != float(weight.replace(",", ".")):
            self.__weight_rest = float(weight.replace(",", "."))
            self.calc_width()

            if not self.__save_sql_info:
                    self.__save_sql_info = True

    def set_print_passport(self, bol):
        if self.__print_passport != bool(bol):
            self.__print_passport = bool(bol)

            if not self.__save_sql_info:
                    self.__save_sql_info = True

    # Разные функции
    def calc_width(self):
        self.__weight_all = round(self.__weight + Decimal(str(self.__weight_rest)), 4)
        if self.__weight_all != 0:
            self.__percent_rest = round((Decimal(str(self.__weight_rest)) * 100) / self.__weight_all, 4)
        else:
            self.__percent_rest = 0

        self.__save_sql_info = True

    def check_balance_material(self):
        if self.__material_id is not None:
            query = """SELECT SUM(material_balance.BalanceWeight) FROM material_balance
                              LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                              WHERE material_supplyposition.Material_NameId = %s"""
            sql_info = my_sql.sql_select(query, (self.__material_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                raise RuntimeError("Не смог получить баланс склада ткани")
            if sql_info[0][0] is None:
                self.__error_value_material = True
                return [False, "Нет на складе этой ткани"]
            elif sql_info[0][0] > (Decimal(str(self.__weight_rest)) - self.__weight_rest_old):
                self.__error_value_material = False
                return [True, "Ткани на складе хватит"]
            else:
                self.__error_value_material = True
                return [False, "Не хватит ткани на складе"]
        else:
            return [False, "Не выбрана ткань"]

    def check_balance_new_material(self, id):
        if self.__material_id != id:
            query = """SELECT SUM(material_balance.BalanceWeight) FROM material_balance
                                  LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                  WHERE material_supplyposition.Material_NameId = %s"""
            sql_info = my_sql.sql_select(query, (id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                raise RuntimeError("Не смог получить баланс новой ткани")

            if sql_info[0][0] is None:
                return [False, "Нету такой ткани на складе"]
            elif self.__weight_all is not None and sql_info[0][0] < self.__weight_all:
                return [False, "Этой ткани не хватит для изменения расходов"]
            elif self.__weight_all is None or sql_info[0][0] > self.__weight_all:
                return [True, "Новой ткани хватает"]
            else:
                return [False, "Что то не так при проверке новой ткани (Обратитесь к админу)"]
        else:
            return [True, "Ткань не изменилась"]


class Pack:
    def __init__(self, id=None):
        self.__id = None
        self.__cut_id = None
        self.__material_id = None
        self.__client_id = None
        self.__client_name = None
        self.__article_parametr = None
        self.__number_pack = None
        self.__number_cut = None
        self.__value_pieces = 0
        self.__value_damage = 0
        self.__value_all = 0
        self.__weight = 0
        self.__note = None
        self.__note_article = None
        self.__size = None
        self.__date_make = None
        self.__date_complete = None
        self.__order = None
        self.__article = None
        self.__article_id = None
        self.__article_size = None
        self.__article_parametr_name = None
        self.__print_label = 0

        self.__material_price = None
        self.__material_name = None
        self.__weight_old_sql = 0

        self.__save_sql_info = False

        self.__operation = []
        self.__accessories = []
        self.__add_material = []

        if id is not None:
            self.set_sql_info(id)

        self.__new_operation_count = -1
        self.__new_accessories_count = -1
        self.__new_add_material = -1

        # Учесть при сохранении
        self.__save_operation_sql = []
        self.__dell_operation_sql = []
        self.__save_accessories_sql = []
        self.__dell_accessories_sql = []
        self.__save_add_material_sql = []
        self.__dell_add_material_sql = []

        self.__error_value_accessories_id = []
        self.__error_value_material = False

    # sql функции
    def set_sql_info(self, sql_id=None):
        if sql_id is None and self.__id is None:
            print("Неверный id пачки")
            return False

        query = """SELECT pack.Id, pack.Article_Parametr_Id, pack.Cut_Id, pack.Order_Id, pack.Number, pack.Value_Pieces, pack.Value_Damage,
                        pack.Weight, pack.Note, pack.Size, pack.Client_Id, clients.Name, pack.Date_Make, pack.Date_Coplete, cut.Material_Id, product_article.Article,
                        product_article_size.Size, product_article_parametrs.Name, cut.Date_Cut, product_article.Name,
                        product_article_parametrs.Barcode, product_article.Id, product_article_parametrs.Id, product_article_parametrs.Product_Note,
                        product_article_parametrs.Client_Name, pack.Print, material_name.Name
                      FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
                      LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                      LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                      LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      LEFT JOIN clients ON pack.Client_Id = clients.Id
                      LEFT JOIN material_name ON cut.Material_Id = material_name.Id
                      WHERE pack.Id = %s"""
        sql_info = my_sql.sql_select(query, (sql_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить данные пачки")
            return False

        self.__id = sql_info[0][0]
        self.__article_parametr = sql_info[0][1]
        self.__cut_id = sql_info[0][2]
        self.__number_cut = sql_info[0][2]
        self.__order = sql_info[0][3]
        self.__number_pack = sql_info[0][4]
        self.__value_pieces = sql_info[0][5]
        self.__value_damage = sql_info[0][6]
        self.__weight = sql_info[0][7]
        self.__weight_old_sql = sql_info[0][7]
        self.__note = sql_info[0][8]
        self.__size = sql_info[0][9]
        self.__client_id = sql_info[0][10]
        self.__client_name = sql_info[0][11]
        self.__date_make = sql_info[0][12]
        self.__date_make_sql = sql_info[0][12]
        self.__date_complete = sql_info[0][13]
        self.__material_id = sql_info[0][14]
        self.__article = sql_info[0][15]
        self.__article_size = sql_info[0][16]
        self.__article_parametr_name = sql_info[0][17]
        self.__cut_date = sql_info[0][18]
        self.__article_name = sql_info[0][19]
        self.__article_barcode = sql_info[0][20]
        self.__article_id = sql_info[0][21]
        self.__article_parametr_id = sql_info[0][22]
        self.__note_article = sql_info[0][23]
        self.__article_client_name = sql_info[0][24]
        self.__print_label = sql_info[0][25]
        self.__material_name = sql_info[0][26]

        self.__value_all = self.__value_pieces - self.__value_damage
        self.__value_all_sql = self.__value_all
        return True

    def take_article_operations(self):
        if self.__article_parametr:
            query = """SELECT op_ar.Position, op_ar.Operation_Id, operations.Name, operations.Price
                        FROM product_article_parametrs
                          LEFT JOIN product_article_operation AS op_ar ON product_article_parametrs.Id = op_ar.Product_Article_Parametrs_Id
                          LEFT JOIN operations ON op_ar.Operation_Id = operations.Id
                        WHERE product_article_parametrs.Id = %s
                        ORDER BY op_ar.Position"""
            sql_info = my_sql.sql_select(query, (self.__article_parametr,))
            if "mysql.connector.errors" in str(type(sql_info)):
                raise RuntimeError("Не смог получить операции артикула")
            self.__operation = []
            for item in sql_info:
                operation = {"id": self.__new_operation_count,
                             "position": item[0],
                             "operation_id": item[1],
                             "name": item[2],
                             "worker_id": None,
                             "worker_name": None,
                             "date_make": None,
                             "date_input": None,
                             "value": self.__value_all,
                             "price": item[3],
                             "pay": 0}
                self.__save_operation_sql.append(self.__new_operation_count)
                self.__new_operation_count -= 1
                self.__operation.append(operation)
            return self.__operation
        else:
            print("Нету артикула")
            return False

    def take_article_accessories(self):
        if self.__article_parametr:
            query = """SELECT material.Accessories_Id, accessories_name.Name, accessories_supplyposition.Price, material.Value, MIN(Data)
                        FROM product_article_material as material
                          LEFT JOIN accessories_name ON material.Accessories_Id = accessories_name.Id
                          LEFT JOIN accessories_supplyposition ON accessories_name.Id = accessories_supplyposition.Accessories_NameId
                          LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.Accessories_SupplyPositionId
                          LEFT JOIN accessories_supply ON accessories_supplyposition.Accessories_SupplyId = accessories_supply.Id
                        WHERE material.Product_Article_Parametrs_Id = %s AND material.Accessories_Id IS NOT NULL
                              AND (accessories_balance.BalanceValue > 0 or accessories_balance.BalanceValue IS NULL)
                        GROUP BY material.Id"""
            sql_info = my_sql.sql_select(query, (self.__article_parametr,))
            if "mysql.connector.errors" in str(type(sql_info)):
                raise RuntimeError("Не смог получить фурнитуру артикула")
            self.__accessories = []
            for item in sql_info:
                accessories = {"id": self.__new_accessories_count,
                               "accessories_id": item[0],
                               "accessories_name": item[1],
                               "price": item[2],
                               "value": self.__value_all,
                               "value_thing": item[3],
                               "sql_value": None,
                               "sql_value_thing": item[3],
                               "sql_value_sum": None}
                self.__save_accessories_sql.append(self.__new_accessories_count)
                self.__new_accessories_count -= 1
                self.__accessories.append(accessories)
                self.__error_value_accessories_id = []
            return self.__accessories
        else:
            print("Нету артикула")
            return False

    def take_operation_pack(self):
        query = """SELECT pack_operation.Id, pack_operation.Position, pack_operation.Operation_id, pack_operation.Name, pack_operation.Worker_Id,
                          staff_worker_info.Last_Name, staff_worker_info.First_Name, pack_operation.Date_make, pack_operation.Date_Input,
                          pack_operation.Value, pack_operation.Price, pack_operation.Pay
                      FROM pack_operation
                        LEFT JOIN staff_worker_info ON pack_operation.Worker_Id = staff_worker_info.Id
                      WHERE pack_operation.Pack_Id = %s"""
        sql_info = my_sql.sql_select(query, (self.__id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог получить операции пачки")

        self.__operation = []
        for sql_operation in sql_info:

            worker_name = sql_operation[5] + " " + sql_operation[6] if sql_operation[5] is not None else None
            operation = {"id": sql_operation[0],
                         "position": sql_operation[1],
                         "operation_id": sql_operation[2],
                         "name": sql_operation[3],
                         "worker_id": sql_operation[4],
                         "worker_name": worker_name,
                         "date_make": sql_operation[7],
                         "date_input": sql_operation[8],
                         "value": sql_operation[9],
                         "price": sql_operation[10],
                         "pay": sql_operation[11]}
            self.__operation.append(operation)
        return self.__operation

    def take_accessories_pack(self):
        query = """SELECT pack_accessories.Id, pack_accessories.Accessories_Id, accessories_name.Name,
                        ROUND(SUM(-transaction_records_accessories.Balance * accessories_supplyposition.Price) / SUM(-transaction_records_accessories.Balance), 4),
                        pack_accessories.Value, pack_accessories.Value_Thing
                      FROM pack_accessories
                        LEFT JOIN transaction_records_accessories ON transaction_records_accessories.Pack_Accessories_Id = pack_accessories.Id
                        LEFT JOIN accessories_balance ON transaction_records_accessories.Supply_Balance_Id = accessories_balance.Id
                        LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                        LEFT JOIN accessories_name ON accessories_supplyposition.Accessories_NameId = accessories_name.Id
                      WHERE pack_accessories.Pack_Id = %s
                      GROUP BY pack_accessories.Id"""
        sql_info = my_sql.sql_select(query, (self.__id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог получить фурнитуру артикула")

        self.__accessories = []
        for sql_accessories in sql_info:
            accessories = {"id": sql_accessories[0],
                           "accessories_id": sql_accessories[1],
                           "accessories_name": sql_accessories[2],
                           "price": sql_accessories[3],
                           "value": sql_accessories[4],
                           "value_thing": sql_accessories[5],
                           "sql_value": sql_accessories[4],
                           "sql_value_thing": sql_accessories[5],
                           "sql_value_sum": sql_accessories[4] * sql_accessories[5]}
            self.__accessories.append(accessories)
        return self.__accessories

    def take_add_material(self):
        query = """SELECT pack_add_material.Id, pack_add_material.Material_Name_Id, material_name.Name, pack_add_material.Weight, pack_add_material.Weight_Rest,
                          pack_add_material.Price
                      FROM pack_add_material LEFT JOIN material_name ON pack_add_material.Material_Name_Id = material_name.Id
                      WHERE pack_add_material.Pack_Id = %s"""
        sql_info = my_sql.sql_select(query, (self.__id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог получить доп материал артикула")

        self.__add_material = []
        for material in sql_info:
            material_add = {"id": material[0],
                            "material_id": material[1],
                            "material_name": material[2],
                            "weight": material[3],
                            "weight_rest": material[4],
                            "price": material[5]}
            self.__add_material.append(material_add)
        return self.__add_material

    def save_sql(self, cut_id):
        if self.__cut_id is None and cut_id is None:
            return [False, "Нету номера кроя (К админу)"]
        elif self.__article_parametr is None:
            return [False, "Не выбран артикул"]
        elif self.__value_pieces == 0 or self.__value_pieces is None:
            return [False, "Не введено кол-во пачки"]
        elif self.__value_all == 0 or self.__value_all is None:
            return [False, "Не пощитано итоговое кол-во пачки (Если вы все ввели то к админу)"]
        elif self.__error_value_accessories_id:
            return [False, "Есть ошибки в фурнитуре (Если ошибок нет то к админу)"]
        elif self.__weight == 0 or self.__weight is None:
            return [False, "нету веса пачки (Введите вес)"]
        elif self.__error_value_material:
            return [False, "Не хватает ткани (Обратиться к руководству за тканью)"]

        sql_connect_transaction = my_sql.sql_start_transaction()
        # сохранение основной информации и ткани
        if self.__save_sql_info:
            if self.__id is None:
                # Сохранение новой пачки
                if cut_id is None:
                    # Если нету номера кроя для новой пачки
                    return [False, "Нету номера кроя для новой пачки!"]
                else:
                    # Если есть номер кроя для новой пачки
                    self.__cut_id = cut_id

                    query = """INSERT pack (Article_Parametr_Id, Cut_Id, Order_Id, Number, Value_Pieces, Value_Damage, Weight, Note, Size, Client_Id,
                                            Date_Make, Date_Coplete, Print)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    sql_values = (self.__article_parametr, self.__cut_id , self.__order, self.__number_pack, self.__value_pieces, self.__value_damage, self.__weight,
                                  self.__note, self.__size, self.__client_id, self.__date_make, self.__date_complete, self.__print_label)

                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог записать пачку"]
                    self.__id = sql_info

                    # Заберем ткань со склада
                    change_value = Decimal(str(self.__weight))
                    while change_value > 0:
                        # получим первый остаток на складе
                        # Проверяем первое кол-во на складе
                        query = """SELECT material_balance.Id, material_balance.BalanceWeight, MIN(material_supply.Data)
                                      FROM material_balance
                                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                        LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                      WHERE material_supplyposition.Material_NameId = %s AND material_balance.BalanceWeight > 0"""
                        sql_balance_material = my_sql.sql_select_transaction(sql_connect_transaction, query, (self.__material_id, ))
                        if "mysql.connector.errors" in str(type(sql_balance_material)):
                            return [False, "Не смог получить остаток ткани на балансе (Это плохо к админу)"]
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
                            return [False, "Не смог забрать ткань с баланса (Это плохо к админу)"]
                        # Делаем запись о заборе ткани с баланса склада
                        query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                    VALUES (%s, %s, SYSDATE(), %s, %s, 120)"""
                        txt_note = "%s/%s - Новая пачка в крое" % (self.__cut_id, self.__number_pack)
                        sql_values = (sql_balance_material[0][0], -take_material_value, txt_note, self.__cut_id)
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог добавить запись при увеличении веса ткани (Это плохо к админу)"]

                    if self.__date_make is not None:
                        query = "UPDATE product_article_warehouse SET Value_In_Warehouse = Value_In_Warehouse + %s WHERE Id_Article_Parametr = %s"
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__value_all, self.__article_parametr))
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог изменить баланс склада товара (Это плохо к админу)"]

                        txt_note = "%s/%s - Принята пачка" % (self.__cut_id, self.__number_pack)
                        query = """INSERT INTO transaction_records_warehouse (Article_Parametr_Id, Date, Balance, Note, Code)
                                                            VALUES (%s, %s, %s, %s, 320)"""
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__article_parametr, datetime.now(),
                                                                                                  self.__value_all, txt_note))
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог записать изменение баланса склада товара (Это плохо к админу)"]

            else:
                # Изменение информации о пачке
                query = """UPDATE pack
                              SET Article_Parametr_Id = %s, Cut_Id= %s, Order_Id= %s, Number= %s, Value_Pieces= %s, Value_Damage= %s, Weight= %s,
                                Note= %s, Size= %s, Client_Id= %s, Date_Make= %s, Date_Coplete= %s, Print = %s
                              WHERE Id = %s"""
                sql_values = (self.__article_parametr, self.__cut_id, self.__order, self.__number_pack, self.__value_pieces, self.__value_damage, self.__weight,
                              self.__note, self.__size, self.__client_id, self.__date_make, self.__date_complete, self.__print_label, self.__id)

                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог изменить пачку"]

                # Проверим принятие пачки на склад
                if self.__date_make_sql is not None and self.__date_make is not None:  # Если пачка уже была принята то провери измененое кол-во
                    change_value = self.__value_all - self.__value_all_sql
                    query = "UPDATE product_article_warehouse SET Value_In_Warehouse = Value_In_Warehouse + %s WHERE Id_Article_Parametr = %s"
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (change_value, self.__article_parametr))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог изменить баланс склада товара (Это плохо к админу)"]

                    if change_value != 0:
                        txt_note = "%s/%s - Изменено кол-во принятой пачки" % (self.__cut_id, self.__number_pack)
                        query = """INSERT INTO transaction_records_warehouse (Article_Parametr_Id, Date, Balance, Note, Code)
                                                                                    VALUES (%s, %s, %s, %s, 322)"""
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__article_parametr, datetime.now(),
                                                                                                  change_value, txt_note))
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог записать изменение баланса склада товара (Это плохо к админу)"]

                elif self.__date_make_sql is None and self.__date_make is not None:  # Если пачку принялм
                    # Если пачка проверилась
                    query = "UPDATE product_article_warehouse SET Value_In_Warehouse = Value_In_Warehouse + %s WHERE Id_Article_Parametr = %s"
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__value_all, self.__article_parametr))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог изменить баланс склада товара (Это плохо к админу)"]

                    txt_note = "%s/%s - Принята пачка" % (self.__cut_id, self.__number_pack)
                    query = """INSERT INTO transaction_records_warehouse (Article_Parametr_Id, Date, Balance, Note, Code)
                                                                                                    VALUES (%s, %s, %s, %s, 320)"""
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__article_parametr, datetime.now(),
                                                                                              self.__value_all, txt_note))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог записать изменение баланса склада товара (Это плохо к админу)"]

                elif self.__date_make_sql is not None and self.__date_make is None:  # Если отменили принятие пачки
                    # Если проверка убралась
                    query = "UPDATE product_article_warehouse SET Value_In_Warehouse = Value_In_Warehouse + %s WHERE Id_Article_Parametr = %s"
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (-self.__value_all_sql, self.__article_parametr))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог изменить баланс склада товара (Это плохо к админу)"]

                    txt_note = "%s/%s - Пачка вернулась со склада" % (self.__cut_id, self.__number_pack)
                    query = """INSERT INTO transaction_records_warehouse (Article_Parametr_Id, Date, Balance, Note, Code)
                                                                                                                        VALUES (%s, %s, %s, %s, 321)"""
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__article_parametr, datetime.now(),
                                                                                              -self.__value_all_sql, txt_note))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог записать изменение баланса склада товара (Это плохо к админу)"]

                # изменим кол-во ткани
                change_value = Decimal(str(self.__weight)) - self.__weight_old_sql
                if change_value > 0:
                    # Ткани стало больше будем забирать!
                    while change_value > 0:
                        # получим первый остаток на складе
                        # Проверяем первое кол-во на складе
                        query = """SELECT material_balance.Id, material_balance.BalanceWeight, MIN(material_supply.Data)
                                      FROM material_balance
                                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                        LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                      WHERE material_supplyposition.Material_NameId = %s AND material_balance.BalanceWeight > 0"""
                        sql_balance_material = my_sql.sql_select_transaction(sql_connect_transaction, query, (self.__material_id, ))
                        if "mysql.connector.errors" in str(type(sql_balance_material)):
                            return [False, "Не смог получить остаток ткани на балансе (Это плохо к админу)"]
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
                            return [False, "Не смог забрать ткань с баланса (Это плохо к админу)"]
                        # Делаем запись о заборе ткани с баланса склада
                        query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                    VALUES (%s, %s, SYSDATE(), %s, %s, 124)"""
                        txt_note = "%s/%s - Увеличение ткани в пачке" % (self.__cut_id, self.__number_pack)
                        sql_values = (sql_balance_material[0][0], -take_material_value, txt_note, self.__cut_id)
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог добавить запись при увеличении веса ткани (Это плохо к админу)"]

                elif change_value < 0:
                    change_value = -change_value
                    # Ткани стало меньше будем возвращать
                    # получим записаные расходы
                    query = """SELECT id, Supply_Balance_Id, SUM(Balance)
                                  FROM transaction_records_material
                                  WHERE Cut_Material_Id = %s
                                  GROUP BY Supply_Balance_Id
                                  ORDER BY Date DESC , transaction_records_material.Id DESC"""
                    sql_transaction = my_sql.sql_select_transaction(sql_connect_transaction, query, (self.__cut_id, ))
                    if "mysql.connector.errors" in str(type(sql_transaction)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог получить записи расходов при уменьшении ткани (Это плохо к админу)"]
                    if not sql_transaction:
                        # Если нету записей об удаляемой ткани
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Нету записей расходов об уменьшаемой ткани (Это плохо к админу)"]

                    # проверяем сумму расходов и уменьшаемой ткани
                    supply_value = 0
                    for row_sql_info in sql_transaction:
                        supply_value += row_sql_info[2]

                    if -supply_value < change_value:
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "записей об удалении со склада меньше чем возвращаемое (Это плохо к админу)"]

                    # Если все сошлось то начинаем возвращать ткань на склад
                    for supply_row in sql_transaction:
                        if change_value <= 0:
                            break

                        if supply_row[2] != 0:

                            if -supply_row[2] > change_value:
                                # Если в этом балансе больше чем нам надо
                                take_material_value = change_value
                                change_value = 0
                            else:
                                # Если в этом балансе меньше чем нам надо
                                take_material_value = -supply_row[2]
                                change_value -= -supply_row[2]

                            # возвращаем ткань на баланс склада
                            query = "UPDATE material_balance SET BalanceWeight = BalanceWeight + %s WHERE Id = %s"
                            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (take_material_value, supply_row[1]))
                            if "mysql.connector.errors" in str(type(sql_info)):
                                my_sql.sql_rollback_transaction(sql_connect_transaction)
                                return [False, "Не смог вернуть ткань на баланс склада при уменьшении ткани (Это плохо к админу)"]

                            # Делаем запись о возырате ткани на баланс склада
                            query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                        VALUES (%s, %s, SYSDATE(), %s, %s, 123)"""
                            txt_note = "%s/%s - Уменьшение ткани в пачке" % (self.__cut_id, self.__number_pack)
                            sql_values = (supply_row[1], take_material_value, txt_note, self.__cut_id)
                            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                            if "mysql.connector.errors" in str(type(sql_info)):
                                my_sql.sql_rollback_transaction(sql_connect_transaction)
                                return [False, "Не смог добавить запись при уменьшении ткани (Это плохо к админу)"]

        # Удаление фурнитуры
        if self.__dell_accessories_sql:
            # Если надо что то удалять
            for dell_accessories_id in self.__dell_accessories_sql:
                if dell_accessories_id > 0:
                    # Удаляемое ID больше 0 получим записаные расходы
                    query = """SELECT Id, Supply_Balance_Id, SUM(Balance) as balance FROM transaction_records_accessories
                                  WHERE Pack_Accessories_Id = %s
                                  GROUP BY Supply_Balance_Id"""
                    sql_transaction = my_sql.sql_select_transaction(sql_connect_transaction, query, (dell_accessories_id, ))
                    if "mysql.connector.errors" in str(type(sql_transaction)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог получить записи расходов при удалении фурнитуры"]

                    if not sql_transaction:
                        # Если нету записей об удаляемой фурнитуре
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Нету записей расходов об удаляемой фурнитуре"]

                    # проверяем сумму расходов и удаляемой фурнитуры
                    supply_value = 0
                    for row_sql_info in sql_transaction:
                        supply_value += row_sql_info[2]

                    query = """SELECT Value * Value_Thing FROM pack_accessories WHERE Id = %s"""
                    sum_accessories = my_sql.sql_select_transaction(sql_connect_transaction, query, (dell_accessories_id, ))
                    if "mysql.connector.errors" in str(type(sql_transaction)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог получить кол-во удаляемой фурнитуры из бызы"]

                    if sum_accessories[0][0] - -supply_value != 0:
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не равны сумма удаляемой фурнитуры и сумма расходов этой фурнитуры"]

                    # Если все сошлось то начинаем возвращать фурнитуру на склад
                    supply_value = 0
                    for supply_row in sql_transaction:
                        if supply_row[2] < 0:
                            # возвращаем фурнитуру на баланс склада
                            query = "UPDATE accessories_balance SET BalanceValue = BalanceValue + %s WHERE Id = %s"
                            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (-supply_row[2], supply_row[1]))
                            if "mysql.connector.errors" in str(type(sql_info)):
                                my_sql.sql_rollback_transaction(sql_connect_transaction)
                                return [False, "Не смог вернуть фурнитуру на баланс склада при удалении фурнитуры"]

                            # Делаем запись о возырате фурнитуры на баланс склада
                            query = """INSERT INTO transaction_records_accessories (Supply_Balance_Id, Balance, Date, Note, Pack_Accessories_Id, Code)
                                        VALUES (%s, %s, SYSDATE(), %s, %s, 222)"""
                            txt_note = "%s/%s - Удаление фурнитуры в пачке" % (self.__cut_id, self.__number_pack)
                            sql_values = (supply_row[1], -supply_row[2], txt_note, dell_accessories_id)
                            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                            if "mysql.connector.errors" in str(type(sql_info)):
                                my_sql.sql_rollback_transaction(sql_connect_transaction)
                                return [False, "Не смог добавить запись при удалении фурнитуры"]

                            supply_value += -supply_row[2]

                    if supply_value != sum_accessories[0][0]:
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Кол-во фурнитуры в пачке не сошлось с возвращаемой при удалении"]

                    # Если все успешно вернулось на склад то просто удаляем фурнитуру из пачки
                    query = """DELETE FROM pack_accessories WHERE Id = %s"""
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (dell_accessories_id, ))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог удалить фурнитуру из пачки"]

        # Добавление и изменение фурнитуры
        if self.__save_accessories_sql:
            for save_accessories_id in self.__save_accessories_sql:
                # проверяем нет ли этой фурнитуры в списке на удаление
                if save_accessories_id in self.__dell_accessories_sql:
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "фурнитура для сохранения находится в списке на удаление"]

                if save_accessories_id < 0:
                    # Это новая фурнитура будем ее сохранять
                    # Ищем фурнитуру по ID и запоминаем ее
                    for accessory in self.__accessories:
                        if accessory["id"] == save_accessories_id:
                            save_accessory = accessory
                            break
                    else:
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "фурнитура для сохранения не найдена в self.__accessories"]

                    # Посмотрим сколько всего этой фурнитуры на складе и хватит ли ее
                    query = """SELECT SUM(accessories_balance.BalanceValue) FROM accessories_balance
                                  LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                                  WHERE accessories_supplyposition.Accessories_NameId = %s"""
                    sql_info = my_sql.sql_select_transaction(sql_connect_transaction, query, (save_accessory["accessories_id"], ))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог получить количество на складе при добалении фурнитуры"]

                    if sql_info[0][0] < save_accessory["value"] * save_accessory["value_thing"]:
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не хватило фурнитуры на складе для добавления фурнитуры"]

                    # если фурнитуры хватает то начинаем ее добавлять
                    # Сначало добавим саму фурнитуру в пачку для получения ее айди
                    if not self.__id:
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Нет ID пачки для записи нововой фурнитуры"]

                    query = """INSERT INTO pack_accessories (Pack_Id, Accessories_Id, Value, Value_Thing) VALUES (%s, %s, %s, %s)"""
                    sql_values = (self.__id, save_accessory["accessories_id"], save_accessory["value"], save_accessory["value_thing"])
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог сохранить новую фурнитуру"]
                    save_accessory["id"] = sql_info

                    # возьмем требуемое кол-во и будем забирать со склада
                    accessory_value = Decimal(save_accessory["value"] * save_accessory["value_thing"])
                    while accessory_value > 0:
                        # Проверяем первое кол-во на складе
                        query = """SELECT accessories_balance.Id, accessories_balance.BalanceValue, MIN(accessories_supply.Data)
                                      FROM accessories_balance
                                        LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                                        LEFT JOIN accessories_supply ON accessories_supplyposition.Accessories_SupplyId = accessories_supply.Id
                                      WHERE accessories_supplyposition.Accessories_NameId = %s AND accessories_balance.BalanceValue > 0"""
                        sql_balance_accessories = my_sql.sql_select_transaction(sql_connect_transaction, query, (save_accessory["accessories_id"], ))
                        if "mysql.connector.errors" in str(type(sql_balance_accessories)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог получить первое количество на балансе при добавлении аксесуара"]

                        if sql_balance_accessories[0][1] > accessory_value:
                            # Если в этом балансе больше чем нам надо
                            take_accessory_value = accessory_value
                            accessory_value = 0
                        else:
                            # Если в этом балансе меньше чем нам надо
                            take_accessory_value = sql_balance_accessories[0][1]
                            accessory_value -= sql_balance_accessories[0][1]

                        # Забираем возможное кол-во
                        query = "UPDATE accessories_balance SET BalanceValue = BalanceValue - %s WHERE Id = %s"
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (take_accessory_value, sql_balance_accessories[0][0]))
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог забрать фурнитуру с баланса при добавлении фурнитуры"]

                        # Делаем запись о заборе фурнитуры на баланс склада
                        query = """INSERT INTO transaction_records_accessories (Supply_Balance_Id, Balance, Date, Note, Pack_Accessories_Id, Code)
                                    VALUES (%s, %s, SYSDATE(), %s, %s, 220)"""
                        txt_note = "%s/%s - Добавление фурнитуры в пачку" % (self.__cut_id, self.__number_pack)
                        sql_values = (sql_balance_accessories[0][0], -take_accessory_value, txt_note, save_accessory["id"])
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог добавить запись при добавлении фурнитуры"]

                else:
                    # Это старая фурнитура будем ее изменять
                    for accessory in self.__accessories:
                        if accessory["id"] == save_accessories_id:
                            change_accessory = accessory
                            break
                    else:
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "фурнитура для мзменеия не найдена в self.__accessories"]

                    # Проверяем какое было кол-во фурнитуры
                    query = """SELECT pack_accessories.Value, pack_accessories.Value_Thing FROM pack_accessories WHERE Id = %s"""
                    sql_info = my_sql.sql_select_transaction(sql_connect_transaction, query, (change_accessory["id"], ))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог получить старое кол во фурнитуры"]

                    # Узнаем больше или меньше фурнитуры
                    change_value = (change_accessory["value"] * Decimal(str(change_accessory["value_thing"]))) - (sql_info[0][0] * sql_info[0][1])

                    if change_value > 0:
                        # Кол-во фурнитуры увеличилось
                        # Посмотрим сколько всего этой фурнитуры на складе и хватит ли ее
                        query = """SELECT SUM(accessories_balance.BalanceValue) FROM accessories_balance
                                      LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                                      WHERE accessories_supplyposition.Accessories_NameId = %s"""
                        sql_info = my_sql.sql_select_transaction(sql_connect_transaction, query, (change_accessory["accessories_id"], ))
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог получить количество на складе при увеличении фурнитуры"]

                        if sql_info[0][0] < change_value:
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не хватило фурнитуры на складе для увеличения фурнитуры"]

                        while change_value > 0:
                            # получим первый остаток на складе
                            # Проверяем первое кол-во на складе
                            query = """SELECT accessories_balance.Id, accessories_balance.BalanceValue, MIN(accessories_supply.Data)
                                          FROM accessories_balance
                                            LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                                            LEFT JOIN accessories_supply ON accessories_supplyposition.Accessories_SupplyId = accessories_supply.Id
                                          WHERE accessories_supplyposition.Accessories_NameId = %s AND accessories_balance.BalanceValue > 0"""
                            sql_balance_accessories = my_sql.sql_select_transaction(sql_connect_transaction, query, (change_accessory["accessories_id"], ))
                            if "mysql.connector.errors" in str(type(sql_balance_accessories)):
                                my_sql.sql_rollback_transaction(sql_connect_transaction)
                                return [False, "Не смог получить первое количество на балансе при изменении аксесуара"]

                            if sql_balance_accessories[0][1] > change_value:
                                # Если в этом балансе больше чем нам надо
                                take_accessory_value = change_value
                                change_value = 0
                            else:
                                # Если в этом балансе меньше чем нам надо
                                take_accessory_value = sql_balance_accessories[0][1]
                                change_value -= sql_balance_accessories[0][1]

                            # Забираем возможное кол-во
                            query = "UPDATE accessories_balance SET BalanceValue = BalanceValue - %s WHERE Id = %s"
                            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (take_accessory_value, sql_balance_accessories[0][0]))
                            if "mysql.connector.errors" in str(type(sql_info)):
                                my_sql.sql_rollback_transaction(sql_connect_transaction)
                                return [False, "Не смог забрать фурнитуру с баланса при увеличении фурнитуры"]

                            # Делаем запись о заборе фурнитуры на баланс склада
                            query = """INSERT INTO transaction_records_accessories (Supply_Balance_Id, Balance, Date, Note, Pack_Accessories_Id, Code)
                                        VALUES (%s, %s, SYSDATE(), %s, %s, 224)"""
                            txt_note = "%s/%s - Увеличение фурнитуры в пачке" % (self.__cut_id, self.__number_pack)
                            sql_values = (sql_balance_accessories[0][0], -take_accessory_value, txt_note, change_accessory["id"])
                            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                            if "mysql.connector.errors" in str(type(sql_info)):
                                my_sql.sql_rollback_transaction(sql_connect_transaction)
                                return [False, "Не смог добавить запись при увеличении фурнитуры"]

                    elif change_value < 0:
                        change_value = -change_value
                        # Кол-во фурнитуры уменьшилось
                        # получим записаные расходы
                        query = """SELECT Id, Supply_Balance_Id, SUM(Balance) as balance, Date FROM transaction_records_accessories
                                    WHERE Pack_Accessories_Id = %s
                                    GROUP BY Supply_Balance_Id
                                    ORDER BY Date DESC , Id DESC """
                        sql_transaction = my_sql.sql_select_transaction(sql_connect_transaction, query, (change_accessory["id"], ))
                        if "mysql.connector.errors" in str(type(sql_transaction)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог получить записи расходов при уменьшении фурнитуры"]

                        if not sql_transaction:
                            # Если нету записей об удаляемой фурнитуре
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Нету записей расходов об уменьшаемой фурнитуре"]

                        # проверяем сумму расходов и уменьшаемой фурнитуры
                        supply_value = 0
                        for row_sql_info in sql_transaction:
                            supply_value += row_sql_info[2]

                        if -supply_value < change_value:
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "записей об удалении со склада меньше чем возвращаемое"]

                        # Если все сошлось то начинаем возвращать фурнитуру на склад
                        for supply_row in sql_transaction:
                            if change_value <= 0:
                                break

                            if -supply_row[2] > change_value:
                                # Если в этом балансе больше чем нам надо
                                take_accessory_value = change_value
                                change_value = 0
                            else:
                                # Если в этом балансе меньше чем нам надо
                                take_accessory_value = -supply_row[2]
                                change_value -= -supply_row[2]

                            # возвращаем фурнитуру на баланс склада
                            query = "UPDATE accessories_balance SET BalanceValue = BalanceValue + %s WHERE Id = %s"
                            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (take_accessory_value, supply_row[1]))
                            if "mysql.connector.errors" in str(type(sql_info)):
                                my_sql.sql_rollback_transaction(sql_connect_transaction)
                                return [False, "Не смог вернуть фурнитуру на баланс склада при уменьшении фурнитуры"]

                            # Делаем запись о возырате фурнитуры на баланс склада
                            query = """INSERT INTO transaction_records_accessories (Supply_Balance_Id, Balance, Date, Note, Pack_Accessories_Id, Code)
                                        VALUES (%s, %s, SYSDATE(), %s, %s, 223)"""
                            txt_note = "%s/%s - Уменьшение фурнитуры в пачке" % (self.__cut_id, self.__number_pack)
                            sql_values = (supply_row[1], take_accessory_value, txt_note, change_accessory["id"])
                            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                            if "mysql.connector.errors" in str(type(sql_info)):
                                my_sql.sql_rollback_transaction(sql_connect_transaction)
                                return [False, "Не смог добавить запись при уменьшении фурнитуры"]

                    else:
                        # Кол-во фурнитуры не изменилось просто сохраним ее
                        pass

                    # сохраним изменения в пачке
                    if not self.__id:
                        print("Нет ID пачки для записи нововой фурнитуры")
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return False
                    query = """UPDATE pack_accessories SET Pack_Id = %s, Accessories_Id = %s, Value = %s, Value_Thing = %s WHERE Id = %s"""
                    sql_values = (self.__id, change_accessory["accessories_id"], change_accessory["value"], change_accessory["value_thing"], change_accessory["id"])
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог сохранить измененя фурнитуры при увеличении"]

        # Удаление операций
        if self.__dell_operation_sql:
            for del_operation_id in self.__dell_operation_sql:
                if del_operation_id > 0:

                    # Посмотрим плаченм или нет операция
                    query = """SELECT Pay FROM  pack_operation WHERE Id = %s"""
                    del_operation = my_sql.sql_select_transaction(sql_connect_transaction, query, (del_operation_id, ))
                    if "mysql.connector.errors" in str(type(del_operation)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог получить удаляемую операцию из базы"]

                    if del_operation[0][0] is None:
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не найдена удаляемая операция"]

                    if del_operation[0][0] == 1:
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Операция оплачена"]

                    # Если пачка свободна от важной информации удалим ее
                    query = """DELETE FROM pack_operation WHERE Id = %s"""
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (del_operation_id, ))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог удалить операцию"]

        # Сохранение операций
        if self.__save_operation_sql:
            for save_operation_id in self.__save_operation_sql:
                save_operation = self.operation(save_operation_id)

                if not save_operation:
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог найти операцию для сохранения"]

                if save_operation_id < 0:

                    # сохранияем новую операцию
                    query = """INSERT INTO pack_operation (Pack_Id, Operation_id, Worker_Id, Position, Name, Date_make, Date_Input, Value, Price, Pay, Date_Pay)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    sql_values = (self.__id, save_operation["operation_id"], save_operation["worker_id"], save_operation["position"],
                                  save_operation["name"], save_operation["date_make"], save_operation["date_input"], save_operation["value"],
                                  save_operation["price"], save_operation["pay"], None)
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог сохранить новую операцию"]
                    save_operation["id"] = sql_info

                elif save_operation_id > 0:
                    # сохранияем изменение операции
                    query = """UPDATE pack_operation SET Pack_Id = %s, Operation_id = %s, Worker_Id = %s, Position = %s, Name = %s,
                                 Date_make = %s, Date_Input = %s, Value = %s, Price = %s, Pay = %s WHERE Id = %s"""
                    sql_values = (self.__id, save_operation["operation_id"], save_operation["worker_id"], save_operation["position"],
                                  save_operation["name"], save_operation["date_make"], save_operation["date_input"], save_operation["value"],
                                  save_operation["price"], save_operation["pay"], save_operation["id"])
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог изменить операцию"]

        # Дополнительный материал
        # Сохранение маетриала
        for material in self.__add_material:
            # Проверяем надо ли сохранять материал
            if material["id"] < 0:
                change_value = Decimal(str(material["weight"])) + Decimal(str(material["weight_rest"]))
                while change_value > 0:
                    # получим первый остаток на складе
                    # Проверяем первое кол-во на складе
                    query = """SELECT material_balance.Id, material_balance.BalanceWeight, MIN(material_supply.Data)
                                  FROM material_balance
                                    LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                    LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                  WHERE material_supplyposition.Material_NameId = %s AND material_balance.BalanceWeight > 0"""
                    sql_balance_material = my_sql.sql_select_transaction(sql_connect_transaction, query, (material["material_id"], ))
                    if "mysql.connector.errors" in str(type(sql_balance_material)):
                        return [False, "Не смог получить остаток ткани на балансе (Это плохо к админу)"]
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
                        return [False, "Не смог забрать ткань с баланса (Это плохо к админу)"]
                    # Делаем запись о заборе ткани с баланса склада
                    query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                VALUES (%s, %s, SYSDATE(), %s, %s, 126)"""
                    txt_note = "%s/%s - Добавление доп. ткани" % (self.__cut_id, self.__number_pack)
                    sql_values = (sql_balance_material[0][0], -take_material_value, txt_note, self.__cut_id)
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог добавить запись при увеличении веса ткани (Это плохо к админу)"]

                # Добавим запись о том что добавлена обрезь из доп ткани
                query = "UPDATE rest_warehouse SET Weight = Weight + %s"
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (material["weight_rest"], ))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог положить обрезь на склад (Это плохо к админу)"]

                txt_note = "%s/%s - Увеличение обрези в доп ткани пачки" % (self.__cut_id, self.__number_pack)
                query = "INSERT INTO transaction_records_rest (Cut_Id, Date, Balance, Note) VALUES (%s, NOW(), %s, %s)"
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__cut_id, material["weight_rest"], txt_note))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог записать добавление на склад обрези (Это плохо к админу)"]

                # Добавим запись о том что есть доп ткань
                query = "INSERT INTO pack_add_material (Pack_Id, Material_Name_Id, Weight, Weight_Rest, Price) VALUES (%s, %s, %s, %s, %s)"
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__id, material["material_id"], material["weight"],
                                                                                          material["weight_rest"], material["price"]))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог сделать запись о наличии доп ткани (Это плохо к админу)"]

        # Удаляем доп материал
        if self.__dell_add_material_sql:
            for del_material_id in self.__dell_add_material_sql:
                # получим записаные расходы и тип ткани
                query = """SELECT Material_Name_Id, Weight, Weight_Rest FROM pack_add_material WHERE Id = %s"""
                sum_material = my_sql.sql_select_transaction(sql_connect_transaction, query, (del_material_id, ))
                if "mysql.connector.errors" in str(type(sum_material)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог получить кол-во удаляемой фурнитуры из бызы"]

                change_value = sum_material[0][1] + sum_material[0][2]
                change_rest = -sum_material[0][2]

                query = """SELECT transaction_records_material.id, transaction_records_material.Supply_Balance_Id, SUM(transaction_records_material.Balance)
                              FROM transaction_records_material LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                                LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                              WHERE transaction_records_material.Cut_Material_Id = %s AND material_supplyposition.Material_NameId = %s
                              GROUP BY Supply_Balance_Id
                              ORDER BY Date"""
                sql_transaction = my_sql.sql_select_transaction(sql_connect_transaction, query, (self.__cut_id, sum_material[0][0]))
                if "mysql.connector.errors" in str(type(sql_transaction)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог получить записи расходов при уменьшении ткани (Это плохо к админу)"]
                if not sql_transaction:
                    # Если нету записей об удаляемой ткани
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Нету записей расходов об уменьшаемой ткани (Это плохо к админу)"]

                # проверяем сумму расходов и уменьшаемой ткани
                supply_value = 0
                for row_sql_info in sql_transaction:
                    supply_value += row_sql_info[2]

                if -supply_value < change_value:
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "записей об удалении со склада меньше чем возвращаемое (Это плохо к админу)"]

                # Если все сошлось то начинаем возвращать ткань на склад
                for supply_row in sql_transaction:
                    if change_value <= 0:
                        break

                    if supply_row[2] != 0:

                        if -supply_row[2] > change_value:
                            # Если в этом балансе больше чем нам надо
                            take_material_value = change_value
                            change_value = 0
                        else:
                            # Если в этом балансе меньше чем нам надо
                            take_material_value = -supply_row[2]
                            change_value -= -supply_row[2]

                        # возвращаем ткань на баланс склада
                        query = "UPDATE material_balance SET BalanceWeight = BalanceWeight + %s WHERE Id = %s"
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (take_material_value, supply_row[1]))
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог вернуть ткань на баланс склада при уменьшении ткани (Это плохо к админу)"]

                        # Делаем запись о возырате ткани на баланс склада
                        query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                    VALUES (%s, %s, SYSDATE(), %s, %s, 125)"""
                        txt_note = "%s/%s - Удаление доп. ткани" % (self.__cut_id, self.__number_pack)
                        sql_values = (supply_row[1], take_material_value, txt_note, self.__cut_id)
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            return [False, "Не смог добавить запись при уменьшении ткани (Это плохо к админу)"]

                query = "UPDATE rest_warehouse SET Weight = Weight + %s"
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (change_rest,))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог забрать обрезь со склада (Это плохо к админу)"]

                txt_note = "%s/%s - Уменьшение обрези в доп ткани пачки" % (self.__cut_id, self.__number_pack)
                query = "INSERT INTO transaction_records_rest (Cut_Id, Date, Balance, Note) VALUES (%s, NOW(), %s, %s)"
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__cut_id, change_rest, txt_note))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог забисать забор со склада обрези (Это плохо к админу)"]

                # Удалим запись о том что есть доп ткань
                query = "DELETE FROM pack_add_material WHERE Id = %s"
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (del_material_id, ))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог удалить запись о наличии доп ткани (Это плохо к админу)"]

        # закрываем транзакцию!
        my_sql.sql_commit_transaction(sql_connect_transaction)
        return [True, "Пачка созранена!"]

    def del_pack(self):
        # Проверим нет ли оплаченых операций
        query = """SELECT COUNT(*) FROM pack_operation WHERE Pack_Id = %s AND  Pay = 1"""
        sql_info = my_sql.sql_select(query, (self.__id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            return [False, "Не смог проверить оплаченые операции"]

        if sql_info[0][0] > 0:
            return [False, "Есть оплаченые операции! Пачку нельзя удалить."]

        # Проверим не принята ли пачка или не проверена
        if self.__date_make is not None or self.__date_complete is not None:
            return [False, "Пачка принята или проверана! Пачку нельзя удалить!"]

        # Начнем транзакцию
        sql_connect_transaction = my_sql.sql_start_transaction()

        # Удалим операции
        query = """DELETE FROM pack_operation WHERE Pack_Id = %s"""
        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "Не смог удалить операции"]

        # Удалим фурнитуру
        # Возьмем список ID для удаления
        query = """SELECT Id FROM pack_accessories WHERE Pack_Id = %s"""
        dell_accessories_sql_id = my_sql.sql_select_transaction(sql_connect_transaction, query, (self.__id, ))
        if "mysql.connector.errors" in str(type(dell_accessories_sql_id)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "Не смог получить ID фурнитуры для удаления"]

        for dell_accessories_id in dell_accessories_sql_id:
            dell_accessories_id = dell_accessories_id[0]
            if dell_accessories_id > 0:
                # Удаляемое ID больше 0 получим записаные расходы
                query = """SELECT Id, Supply_Balance_Id, SUM(Balance) as balance FROM transaction_records_accessories
                                  WHERE Pack_Accessories_Id = %s
                                  GROUP BY Supply_Balance_Id"""
                sql_transaction = my_sql.sql_select_transaction(sql_connect_transaction, query, (dell_accessories_id, ))
                if "mysql.connector.errors" in str(type(sql_transaction)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог получить записи расходов при удалении фурнитуры"]

            if not sql_transaction:
                # Если нету записей об удаляемой фурнитуре
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Нету записей расходов об удаляемой фурнитуре"]

            # проверяем сумму расходов и удаляемой фурнитуры
            supply_value = 0
            for row_sql_info in sql_transaction:
                supply_value += row_sql_info[2]

            query = """SELECT Value * Value_Thing FROM pack_accessories WHERE Id = %s"""
            sum_accessories = my_sql.sql_select_transaction(sql_connect_transaction, query, (dell_accessories_id, ))
            if "mysql.connector.errors" in str(type(sum_accessories)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Не смог получить кол-во удаляемой фурнитуры из бызы"]

            if sum_accessories[0][0] - -supply_value != 0:
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Не равны сумма удаляемой фурнитуры и сумма расходов этой фурнитуры"]

            # Если все сошлось то начинаем возвращать фурнитуру на склад
            supply_value = 0
            for supply_row in sql_transaction:
                if supply_row[2] < 0:
                    # возвращаем фурнитуру на баланс склада
                    query = "UPDATE accessories_balance SET BalanceValue = BalanceValue + %s WHERE Id = %s"
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (-supply_row[2], supply_row[1]))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог вернуть фурнитуру на баланс склада при удалении фурнитуры"]

                    # Делаем запись о возырате фурнитуры на баланс склада
                    query = """INSERT INTO transaction_records_accessories (Supply_Balance_Id, Balance, Date, Note, Pack_Accessories_Id, Code)
                                    VALUES (%s, %s, SYSDATE(), %s, %s, 221)"""
                    txt_note = "%s/%s - Удаление пачки" % (self.__cut_id, self.__number_pack)
                    sql_values = (supply_row[1], -supply_row[2], txt_note, dell_accessories_id)
                    sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                    if "mysql.connector.errors" in str(type(sql_info)):
                        my_sql.sql_rollback_transaction(sql_connect_transaction)
                        return [False, "Не смог добавить запись при удалении фурнитуры"]

                    supply_value += -supply_row[2]

            if supply_value != sum_accessories[0][0]:
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Кол-во фурнитуры в пачке не сошлось с возвращаемой при удалении"]

            # Если все успешно вернулось на склад то просто удаляем фурнитуру из пачки
            query = """DELETE FROM pack_accessories WHERE Id = %s"""
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (dell_accessories_id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Не смог удалить фурнитуру из пачки"]

        # Удалим ткань
        change_value = self.__weight_old_sql

        # получим записаные расходы
        query = """SELECT id, Supply_Balance_Id, SUM(Balance)
                                  FROM transaction_records_material
                                  WHERE Cut_Material_Id = %s
                                  GROUP BY Supply_Balance_Id
                                  ORDER BY Date"""
        sql_transaction = my_sql.sql_select_transaction(sql_connect_transaction, query, (self.__cut_id, ))
        if "mysql.connector.errors" in str(type(sql_transaction)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "Не смог получить записи расходов при удалении пачки (Это плохо к админу)"]
        if not sql_transaction:
            # Если нету записей об удаляемой ткани
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "Нету записей расходов об удаляемой пачке (Это плохо к админу)"]

        # проверяем сумму расходов и удаляемой ткани
        supply_value = 0
        for row_sql_info in sql_transaction:
            supply_value += row_sql_info[2]

        if -supply_value < change_value:
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "записей об удалении со склада меньше чем удаляемое (Это плохо к админу)"]

        # Если все сошлось то начинаем возвращать ткань на склад
        for supply_row in sql_transaction:
            if change_value <= 0:
                break

            if supply_row[2] != 0:

                if -supply_row[2] > change_value:
                    # Если в этом балансе больше чем нам надо
                    take_material_value = change_value
                    change_value = 0
                else:
                    # Если в этом балансе меньше чем нам надо
                    take_material_value = -supply_row[2]
                    change_value -= -supply_row[2]

                # возвращаем ткань на баланс склада
                query = "UPDATE material_balance SET BalanceWeight = BalanceWeight + %s WHERE Id = %s"
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (take_material_value, supply_row[1]))
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог вернуть ткань на баланс склада при улалении пачки (Это плохо к админу)"]

                # Делаем запись о возырате ткани на баланс склада
                query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                  VALUES (%s, %s, SYSDATE(), %s, %s, 121)"""
                txt_note = "%s/%s - Удаление пачки из кроя" % (self.__cut_id, self.__number_pack)
                sql_values = (supply_row[1], take_material_value, txt_note, self.__cut_id)
                sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                if "mysql.connector.errors" in str(type(sql_info)):
                    my_sql.sql_rollback_transaction(sql_connect_transaction)
                    return [False, "Не смог добавить запись при удалении пачки (Это плохо к админу)"]

        # Заберем со скдала изделия если пачка была принята
        if self.__date_make_sql is not None:
            query = "UPDATE product_article_warehouse SET Value_In_Warehouse = Value_In_Warehouse - %s WHERE Id = %s"
            sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__value_all_sql, self.__article_parametr))
            if "mysql.connector.errors" in str(type(sql_info)):
                my_sql.sql_rollback_transaction(sql_connect_transaction)
                return [False, "Не смог изменить баланс склада товара (Это плохо к админу)"]

        # Удалим саму пачку
        query = """DELETE FROM pack WHERE Id = %s"""
        dell_accessories_sql_id = my_sql.sql_change_transaction(sql_connect_transaction, query, (self.__id, ))
        if "mysql.connector.errors" in str(type(dell_accessories_sql_id)):
            my_sql.sql_rollback_transaction(sql_connect_transaction)
            return [False, "Не смог удалить саму пачку, проверьте доп ткань!"]

        my_sql.sql_commit_transaction(sql_connect_transaction)
        return [True, "Пачка удалена!"]

    def print_info(self):
        pass

    # Получекние значений
    def id(self):
        return self.__id

    def value(self):
        return self.__value_pieces

    def value_damage(self):
        return self.__value_damage

    def date_make(self):
        return self.__date_make

    def date_complete(self):
        return self.__date_complete

    def number_pack(self):
        return self.__number_pack

    def number_cut(self):
        return self.__number_cut

    def operations(self):
        return self.__operation

    def operation(self, id):
        for operation in self.__operation:
                if operation["id"] == id:
                    return operation
        else:
            return False

    def accessories(self):
        return self.__accessories

    def accessory(self, id):
        for accessory in self.__accessories:
                if accessory["id"] == id:
                    return accessory
        else:
            return False

    def value_all(self):
        return self.__value_all

    def material_id(self):
        return self.__material_id

    def article(self):
        return self.__article

    def article_id(self):
        return self.__article_id

    def article_name(self):
        return self.__article_parametr_name

    def article_size(self):
        return self.__article_size

    def article_product_name(self):
        return self.__article_name

    def article_barcode(self):
        return self.__article_barcode

    def size(self):
        return self.__size

    def parametr_name(self):
        return self.__article + " (" + self.__article_size + ") [" + self.__article_parametr_name + "]"

    def parametr(self):
        return self.__article_parametr_name

    def parametr_id(self):
        return self.__article_parametr_id

    def weight(self):
        return self.__weight

    def weight_piece(self):
        if self.__value_pieces:
            return round(self.__weight / self.__value_pieces, 4)
        else:
            return 0

    def client(self):
        return self.__client_id

    def client_name(self):
        return self.__client_name

    def order(self):
        return self.__order

    def note(self):
        return self.__note

    def note_article(self):
        return self.__note_article

    def material_price(self):
        if self.__material_price is None:
            query = """SELECT ROUND(SUM(-transaction_records_material.Balance * material_supplyposition.Price) / SUM(-transaction_records_material.Balance), 4)
                          FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
                            LEFT JOIN transaction_records_material ON transaction_records_material.Cut_Material_Id = cut.Id
                            LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                            LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                          WHERE pack.Id = %s AND material_supplyposition.Material_NameId = %s"""
            sql_info = my_sql.sql_select(query, (self.__id, self.__material_id))
            if "mysql.connector.errors" in str(type(sql_info)):
                print("Не смог получить цену ткани")
                return False
            if sql_info[0][0]:
                self.__material_price = round(sql_info[0][0], 4)
            else:
                self.__material_price = 0

        return self.__material_price

    def material_name(self):
        return self.__material_name

    def cut_date(self):
        return self.__cut_date

    def add_materials(self):
        return self.__add_material

    def percent_damage(self):
        if self.__value_pieces:
            return round((self.__value_damage * 100) / self.__value_pieces, 4)
        else:
            return 0

    def article_client_name(self):
        return self.__article_client_name

    def print_label(self):
        return self.__print_label

    def print_label_bool(self):
        if self.__print_label:
            return True
        else:
            return False

    # Вставка заначений
    def set_number_pack(self, number):
        if self.__number_pack != int(number):
            self.__number_pack = int(number)

        if not self.__save_sql_info:
                self.__save_sql_info = True

    def set_number_cut(self, number):
        if number is not None:
            if self.__number_cut != int(number):
                self.__number_cut = int(number)

    def set_date_make(self, date):
        if self.__date_make != date:
            if isinstance(date, QDate):
                self.__date_make = datetime.strptime(date.toString(1), "%Y-%m-%d")

                if not self.__save_sql_info:
                    self.__save_sql_info = True

            elif isinstance(date, datetime):
                self.__date_make = date

                if not self.__save_sql_info:
                    self.__save_sql_info = True

            elif date is None:
                self.__date_make = None
                if not self.__save_sql_info:
                    self.__save_sql_info = True

            else:
                raise RuntimeError("Не тот тип данных!")

    def set_date_complete(self, date):
        if self.__date_complete != date:
            if isinstance(date, QDate):
                self.__date_complete = datetime.strptime(date.toString(1), "%Y-%m-%d")

                if not self.__save_sql_info:
                    self.__save_sql_info = True

            elif isinstance(date, datetime):
                self.__date_complete = date

                if not self.__save_sql_info:
                    self.__save_sql_info = True

            elif date is None:
                self.__date_complete = None
                if not self.__save_sql_info:
                    self.__save_sql_info = True

            else:
                raise RuntimeError("Не тот тип данных!")

    def set_size(self, size):
        if size != "":
            try:
                if self.__size != int(size):
                    self.__size = int(size)

                    if not self.__save_sql_info:
                        self.__save_sql_info = True

                return True
            except ValueError:
                return False

    def set_article(self, id):
        if id != "":
            if self.__article_parametr != int(id):
                self.__article_parametr = int(id)

                if not self.__save_sql_info:
                        self.__save_sql_info = True

    def set_client(self, id):
        if id != "":
            if self.__client_id != int(id):
                self.__client_id = int(id)

                if not self.__save_sql_info:
                        self.__save_sql_info = True

    def set_value_pieces(self, value):
        if value != "":
            if self.__value_pieces != int(value):
                self.__value_pieces = int(value)

                if not self.__save_sql_info:
                        self.__save_sql_info = True

            self.calc_value()

    def set_value_damage(self, value):
        if value != "":
            if self.__value_damage != int(value):
                self.__value_damage = int(value)

                if not self.__save_sql_info:
                        self.__save_sql_info = True
            self.calc_value()

    def set_width(self, value):
        if value != "":
            try:
                width = float(value.replace(",", "."))
            except:
                return False
            if self.__weight != width:
                self.__weight = width

                if not self.__save_sql_info:
                        self.__save_sql_info = True

    def set_material_id(self, id):
        self.__material_id = id

    def set_operation(self, info, id=None):
        if id is not None:
            for operation in self.__operation:
                if operation["id"] == id:
                    edit_operation = operation
                    position = operation["position"]
                    if self.__save_operation_sql.count(operation["id"]) == 0:
                        self.__save_operation_sql.append(operation["id"])
                    break
            else:
                raise RuntimeError("Что то пошло не так со вставкой операции (id в for)")

        elif id is None:
            edit_operation = {"id": self.__new_operation_count,
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
            self.__save_operation_sql.append(self.__new_operation_count)
            self.__new_operation_count -= 1
            self.__operation.append(edit_operation)

            position = self.new_position_operation()
        else:
            raise RuntimeError("Что то пошло не так со вставкой операции (id)")

        edit_operation["position"] = position
        edit_operation["operation_id"] = info["operation_id"]
        edit_operation["name"] = info["name"]
        edit_operation["worker_id"] = info["worker_id"]
        edit_operation["worker_name"] = info["worker_name"]
        date = datetime.strptime(info["date_make"].toString(1), "%Y-%m-%d") if info["date_make"] is not None else None
        edit_operation["date_make"] = date
        date = datetime.strptime(info["date_input"].toString(1), "%Y-%m-%d") if info["date_input"] is not None else None
        edit_operation["date_input"] = date
        edit_operation["value"] = info["value"]
        edit_operation["price"] = info["price"]
        edit_operation["pay"] = info["pay"]

    def set_accessories(self, info, id=None):
        if id is not None:
            for accessories in self.__accessories:
                if accessories["id"] == id:
                    edit_accessories = accessories
                    if self.__save_accessories_sql.count(accessories["id"]) == 0:
                        self.__save_accessories_sql.append(accessories["id"])
                    break
            else:
                raise RuntimeError("Что то пошло не так со вставкой фурнитуры (id в for)")

        elif id is None:
            edit_accessories = {"id": self.__new_accessories_count,
                                "accessories_id": None,
                                "accessories_name": None,
                                "price": None,
                                "value": None,
                                "sql_value": None,
                                "value_thing": None}
            self.__save_accessories_sql.append(self.__new_accessories_count)
            self.__new_accessories_count -= 1
            self.__accessories.append(edit_accessories)

        else:
            raise RuntimeError("Что то пошло не так со вставкой фурнитуры (id)")

        query = """SELECT accessories_supplyposition.Price, MIN(Data)
                        FROM accessories_name
                          LEFT JOIN accessories_supplyposition ON accessories_name.Id = accessories_supplyposition.Accessories_NameId
                          LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.Accessories_SupplyPositionId
                          LEFT JOIN accessories_supply ON accessories_supplyposition.Accessories_SupplyId = accessories_supply.Id
                        WHERE accessories_name.Id = %s AND (accessories_balance.BalanceValue > 0 or accessories_balance.BalanceValue IS NULL)
                        GROUP BY accessories_name.Id"""
        sql_info = my_sql.sql_select(query, (info["accessories_id"],))
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог получить цену фурнитуры")

        price = sql_info[0][0]

        edit_accessories["accessories_id"] = info["accessories_id"]
        edit_accessories["accessories_name"] = info["accessories_name"]
        edit_accessories["price"] = price
        edit_accessories["value"] = info["value"]
        edit_accessories["sql_value"] = info["sql_value"]
        edit_accessories["value_thing"] = info["value_thing"]
        edit_accessories["sql_value_sum"] = info["value_thing"] * info["value"]

    def set_order(self, id):
        self.__order = int(id)

    def set_note(self, txt):
        self.__note = str(txt)
        if not self.__save_sql_info:
            self.__save_sql_info = True

    def set_add_material(self, info):
        price = self.take_material_price(info["material_id"])
        if not price:
            return [False, "Нету такой ткани!"]

        if self.take_amount_material(info["material_id"]) < float(info["weight"]):
            return [False, "На складе нет столько ткани!"]

        add_material = {"id": self.__new_add_material,
                        "material_id": info["material_id"],
                        "material_name": info["material_name"],
                        "weight": info["weight"],
                        "weight_rest": info["weight_rest"],
                        "price": price}

        self.__add_material.append(add_material)
        self.__new_add_material -= 1
        return [True, "Ok"]

    def set_print_label(self, info):
        if self.__print_label != int(info):
            self.__print_label = int(info)
            if not self.__save_sql_info:
                self.__save_sql_info = True

    # Удаление значений
    def del_operation(self, id):
        if id < 0:
            for e in enumerate(self.__operation):
                if e[1]["id"] == id:
                    self.__operation.pop(e[0])
                    try:
                        self.__save_operation_sql.remove(e[1]["id"])
                    except:
                        pass
                    return True
            else:
                return False
        else:
            for e in enumerate(self.__operation):
                if e[1]["id"] == id and e[1]["pay"] == 0:
                    self.__operation.pop(e[0])
                    try:
                        self.__save_operation_sql.remove(e[1]["id"])
                    except:
                        pass
                    self.__dell_operation_sql.append(e[1]["id"])
                    return True

        return False

    def del_accessories(self, id):
        if id < 0:
            for e in enumerate(self.__accessories):
                if e[1]["id"] == id:
                    self.__accessories.pop(e[0])
                    try:
                        self.__save_accessories_sql.remove(e[1]["id"])
                    except:
                        pass
                    print(self.__save_accessories_sql)
                    return True
            else:
                return False
        else:
            for e in enumerate(self.__accessories):
                if e[1]["id"] == id:
                    self.__accessories.pop(e[0])
                    try:
                        self.__save_accessories_sql.remove(e[1]["id"])
                    except:
                        pass
                    self.__dell_accessories_sql.append(e[1]["id"])
                    return True

        return False

    def del_client(self):
        self.__save_sql_info = True
        self.__client_id = None

    def del_order(self):
        self.__save_sql_info = True
        self.__order = None

    def del_add_material(self, id):
        if id < 0:
            for e in enumerate(self.__add_material):
                if e[1]["id"] == id:
                    self.__add_material.pop(e[0])
                    return True
            else:
                return False
        else:
            for e in enumerate(self.__add_material):
                if e[1]["id"] == id:
                    self.__add_material.pop(e[0])
                    self.__dell_add_material_sql.append(e[1]["id"])
                    return True

        return False

    # Разные функции
    def calc_value(self):
        if self.__value_pieces is not None:
            if self.__value_damage is None:
                damage = 0
            else:
                damage = self.__value_damage
            old_value = self.__value_all

            if self.__value_pieces - damage <= 0:
                return False

            self.__value_all = self.__value_pieces - damage

            # Вставим изменения в фурнитуру и операции если кол-ва равны
            for accessory in self.__accessories:
                if accessory["value"] == old_value:
                    accessory["value"] = self.__value_all
                    if not self.__save_accessories_sql.count(accessory["id"]):
                        self.__save_accessories_sql.append(accessory["id"])

            for operation in self.__operation:
                if operation["value"] == old_value and operation["pay"] == 0:
                    operation["value"] = self.__value_all
                    if not self.__save_operation_sql.count(operation["id"]):
                        self.__save_operation_sql.append(operation["id"])

    def clear_save_operation(self):
        self.__save_operation_sql = []

    def clear_save_accessories(self):
        self.__save_accessories_sql = []

    def check_balance_accessories(self, id):
        # Функция провыеряет хватает ли для сохранения или для изменения
        accessory = self.accessory(id)
        if not accessory:
            return [False, "Нет такого ID"]

        sum_accessories = round(accessory["value"] * accessory["value_thing"], 4)
        if sum_accessories >= 0 and accessory["sql_value_sum"] is None:
            # Новая фурнитура проверим склад
            query = """SELECT SUM(accessories_balance.BalanceValue) FROM accessories_balance
                                  LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                                  WHERE accessories_supplyposition.Accessories_NameId = %s"""
            sql_info = my_sql.sql_select(query, (accessory["accessories_id"],))
            if "mysql.connector.errors" in str(type(sql_info)):
                raise RuntimeError("Не смог получить сумму транзакций при проверке аксксуара")

            if sql_info[0][0] is None:
                self.__error_value_accessories_id.append(id)
                return [False, "На складе нет такой фурнитуры"]
            elif sql_info[0][0] > sum_accessories:
                try:
                    self.__error_value_accessories_id.remove(id)
                except:
                    pass
                return [True, "На складе хватит фурнитуры для добавления"]
            else:
                self.__error_value_accessories_id.append(id)
                return [False, "На складе не хватит фурнитуры для добавления"]

        elif sum_accessories > accessory["sql_value_sum"]:
            # Если стало больше фурнитуры то проверяем хватит ли нам на складе
            query = """SELECT SUM(accessories_balance.BalanceValue) FROM accessories_balance
                                  LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                                  WHERE accessories_supplyposition.Accessories_NameId = %s"""
            sql_info = my_sql.sql_select(query, (accessory["accessories_id"],))
            if "mysql.connector.errors" in str(type(sql_info)):
                raise RuntimeError("Не смог получить баланс склада при проверке аксксуара")

            if sql_info[0][0] is None:
                self.__error_value_accessories_id.append(id)
                return [False, "На складе нет такой фурнитуры"]
            elif sql_info[0][0] > (Decimal(str(sum_accessories)) - Decimal(accessory["sql_value_sum"])):
                try:
                    self.__error_value_accessories_id.remove(id)
                except:
                    pass
                return [True, "На складе хватит фурнитуры для увеличения"]
            else:
                self.__error_value_accessories_id.append(id)
                return [False, "На складе не хватит фурнитуры для увеличения"]

        elif sum_accessories < accessory["sql_value_sum"]:
            # Если стало меньше фурнитуры то проверяем хватит ли нам записей транзакций
            query = """SELECT SUM(Balance) as balance FROM transaction_records_accessories WHERE Pack_Accessories_Id = %s"""
            sql_info = my_sql.sql_select(query, (accessory["id"],))
            if "mysql.connector.errors" in str(type(sql_info)):
                raise RuntimeError("Не смог получить сумму транзакций при проверке аксксуара")

            if sql_info[0][0] is None:
                self.__error_value_accessories_id.append(id)
                return [False, "Нет записей об этой фурнитуре"]
            if -sql_info[0][0] > -(Decimal(str(sum_accessories)) - accessory["sql_value_sum"]):
                try:
                    self.__error_value_accessories_id.remove(id)
                except:
                    pass
                return [True, "Количество в транзакции хватит для уменьшения"]
            else:
                self.__error_value_accessories_id.append(id)
                return [False, "Количество в транзакции не хватит для уменьшения"]

        elif sum_accessories == accessory["sql_value_sum"]:
            # Изменений не произошло
            try:
                self.__error_value_accessories_id.remove(id)
            except:
                pass
            return [True, "Изменений не произошло"]

        else:
            # нештатная ситуация
            self.__error_value_accessories_id.append(id)
            return [False, "Нештатная ситуация"]

    def check_balance_material(self):
        if self.__material_id is not None:
            query = """SELECT SUM(material_balance.BalanceWeight) FROM material_balance
                              LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                              WHERE material_supplyposition.Material_NameId = %s"""
            sql_info = my_sql.sql_select(query, (self.__material_id,))
            if "mysql.connector.errors" in str(type(sql_info)):
                raise RuntimeError("Не смог получить баланс склада ткани")
            if sql_info[0][0] is None:
                self.__error_value_material = True
                return [False, "Нет на складе этой ткани"]
            elif sql_info[0][0] > Decimal(str(self.__weight)) - self.__weight_old_sql:
                self.__error_value_material = False
                return [True, "Ткани на складе хватит"]
            else:
                self.__error_value_material = True
                return [False, "Не хватит ткани на складе"]
        else:
            raise RuntimeError("Нету ID материала при проверки остатка баланса")

    def need_save_sql(self):
        if self.__save_sql_info or self.__save_operation_sql or self.__save_accessories_sql or self.__dell_operation_sql or self.__dell_accessories_sql:
            return True
        else:
            return False

    def new_position_operation(self):
        max_position = 0
        for operation in self.__operation:
            if operation["position"] is not None:
                max_position = max(max_position, operation["position"])

        return max_position + 1

    def clone_operation(self, id):
        for operation in self.__operation:
            if operation["id"] == id:

                clone_operation = {"id": self.__new_operation_count,
                                   "position": None,
                                   "operation_id": operation["operation_id"],
                                   "name": operation["name"],
                                   "worker_id": operation["worker_id"],
                                   "worker_name": operation["worker_name"],
                                   "date_make": operation["date_make"],
                                   "date_input": operation["date_input"],
                                   "value": operation["value"],
                                   "price": operation["price"],
                                   "pay": operation["pay"]}

                self.__save_operation_sql.append(self.__new_operation_count)
                self.__new_operation_count -= 1
                self.__operation.append(clone_operation)
                return [True, ""]
        else:
            return [False, "Не найден ID дублируемой операции"]

    def take_material_price(self, id_material):
        # Вернет цену материала по id матреиала!
        query = """SELECT Price
                        FROM material_name
                          LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                          LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                          LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                        WHERE material_name.Id = %s AND BalanceWeight > 0
                        ORDER BY Data
                        LIMIT 1"""
        sql_info = my_sql.sql_select(query, (id_material, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог получить цену материала")
        if sql_info:
            return sql_info[0][0]
        else:
            return None

    def take_amount_material(self, id_material):
        # Вернет остаток материала по id матреиала!
        query = """SELECT SUM(material_balance.BalanceWeight)
                      FROM  material_supplyposition LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                      WHERE material_supplyposition.Material_NameId = %s"""
        sql_info = my_sql.sql_select(query, (id_material, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог получить остаток ткани")
        if sql_info:
            return sql_info[0][0]
        else:
            return None

    def copy_pack(self, copy_id):
        query = """SELECT pack.Article_Parametr_Id, pack.Order_Id,
                                pack.Note, pack.Size, pack.Client_Id, clients.Name, product_article.Article,
                                product_article_size.Size, product_article_parametrs.Name, product_article.Name,
                                product_article_parametrs.Barcode, product_article.Id, product_article_parametrs.Id, product_article_parametrs.Product_Note,
                                product_article_parametrs.Client_Name
                              FROM pack
                              LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                              LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                              LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                              LEFT JOIN clients ON pack.Client_Id = clients.Id
                              WHERE pack.Id = %s"""
        sql_info = my_sql.sql_select(query, (copy_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить данные пачки")
            return False

        self.__article_parametr = sql_info[0][0]
        self.__order = sql_info[0][1]
        self.__note = sql_info[0][2]
        self.__size = sql_info[0][3]
        self.__client_id = sql_info[0][4]
        self.__client_name = sql_info[0][5]
        self.__article = sql_info[0][6]
        self.__article_size = sql_info[0][7]
        self.__article_parametr_name = sql_info[0][6] + " (" + sql_info[0][7] + ") [" + sql_info[0][8] + "]"
        self.__article_name = sql_info[0][9]
        self.__article_barcode = sql_info[0][10]
        self.__article_id = sql_info[0][11]
        self.__article_parametr_id = sql_info[0][12]
        self.__note_article = sql_info[0][13]
        self.__article_client_name = sql_info[0][14]

        query = """SELECT pack_operation.Position, pack_operation.Operation_id, pack_operation.Name, pack_operation.Price
                      FROM pack_operation
                        LEFT JOIN staff_worker_info ON pack_operation.Worker_Id = staff_worker_info.Id
                      WHERE pack_operation.Pack_Id = %s"""
        sql_info = my_sql.sql_select(query, (copy_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог получить операции пачки")

        self.__operation = []
        for item in sql_info:
            operation = {"id": self.__new_operation_count,
                         "position": item[0],
                         "operation_id": item[1],
                         "name": item[2],
                         "worker_id": None,
                         "worker_name": None,
                         "date_make": None,
                         "date_input": None,
                         "value": self.__value_all,
                         "price": item[3],
                         "pay": 0}
            self.__save_operation_sql.append(self.__new_operation_count)
            self.__new_operation_count -= 1
            self.__operation.append(operation)

        self.take_article_accessories()