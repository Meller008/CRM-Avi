from function import my_sql
from PyQt5.QtCore import QDate
from datetime import datetime


class Material:

    def __init__(self, id=None):
        self.__id = None
        self.__Name = None
        self.__information = None
        self.__balance = None

        if id is not None:
            self.set_sql_info(id)

    def set_sql_info(self, sql_id=None):
        if sql_id is None and self.__id is None:
            print("Неверный id ткани")
            return False

        query = """SELECT material_name.Id, material_name.Name, material_name.Information, SUM(material_balance.BalanceWeight)
                    FROM material_name
                      LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                      LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                    WHERE Material_NameId = %s"""
        sql_info = my_sql.sql_select(query, (sql_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить данные ткани")
            return False

        self.__id = sql_info[0][0]
        self.__Name = sql_info[0][1]
        self.__information = sql_info[0][2]
        self.__balance = sql_info[0][3]
        return True

    def name(self):
        return self.__Name


class Client:
    def __init__(self, id=None):
        self.__id = None
        self.__mame = None
        self.__legal_address = None
        self.__actual_address = None
        self.__inn = None
        self.__kpp = None
        self.__ogrn = None
        self.__account = None
        self.__bank = None
        self.__corres_account = None
        self.__bik = None
        self.__contact_person = None
        self.__phone = None
        self.__mail = None
        self.__note = None
        self.__no_nds = None

        self.__adress_array = None
        self.__vendor_numbers_array = None

        if id is not None:
            self.set_sql_info(id)

    def set_sql_info(self, sql_id=None):
        if sql_id is None and self.__id is None:
            print("Неверный id клиента")
            return False

        query = """SELECT Id, Name, Legal_Address, Actual_Address, INN, KPP, OGRN, Account, Bank, corres_Account, BIK, Contact_Person, Phone, Mail, Note, No_Nds
                    FROM clients
                    WHERE Id = %s"""
        sql_info = my_sql.sql_select(query, (sql_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить данные клиента")
            return False

        self.__id = sql_info[0][0]
        self.__mame = sql_info[0][1]
        self.__legal_address = sql_info[0][2]
        self.__actual_address = sql_info[0][3]
        self.__inn = sql_info[0][4]
        self.__kpp = sql_info[0][5]
        self.__ogrn = sql_info[0][6]
        self.__account = sql_info[0][7]
        self.__bank = sql_info[0][8]
        self.__corres_account = sql_info[0][9]
        self.__bik = sql_info[0][10]
        self.__contact_person = sql_info[0][11]
        self.__phone = sql_info[0][12]
        self.__mail = sql_info[0][13]
        self.__note = sql_info[0][14]
        if sql_info[0][15] == 1:
            self.__no_nds = True
        else:
            self.__no_nds = False
        return True

        query = """SELECT adress.Id, adress.Name, adress.Adres, adress.KPP
                    FROM clients_actual_address AS adress
                    WHERE adress.Client_Id = %s"""
        sql_info = my_sql.sql_select(query, (sql_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить адреса клиента")
            return False
        self.__adress_array = []
        for adres in sql_info:
            self.__adress_array.append({"id": adres[0], "name adres": adres[1], "adres": adres[2], "kpp": adres[3]})

        query = """SELECT number.Id, number.Number, number.Contract, number.Data_From
                    FROM clients_vendor_number AS number
                    WHERE number.Client_Id = %s"""
        sql_info = my_sql.sql_select(query, (sql_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить намер поставщика у клиента")
            return False
        self.__vendor_numbers_array = []
        for number in sql_info:
            self.__vendor_numbers_array.append({"id": number[0], "number": number[1], "contract": number[2], "date": number[3]})


class Cut:
    def __init__(self, id=None):
        self.__id = None
        self.__date_cut = None
        self.__worker_id = None
        self.__weight = None
        self.__weight_rest = None
        self.__note = None
        self.__complete = None
        self.__pack_id_dict = None
        self.__material_id = None
        self.__material_name = None
        self.__material_price = None
        self.__number = None

        self.__save_sql_info = False

        if id is not None:
            self.take_sql_info(int(id))

    # sql функции
    def take_sql_info(self, sql_id=None):
        if sql_id is None and self.__id is None:
            print("Не верный ID")
            return False
        query = """SELECT cut.Id, cut.Date_Cut, cut.Worker_Id, SUM(pack.Weight), cut.Weight_Rest, cut.Note,
                      CASE
                        WHEN SUM(IF(pack.Date_Coplete IS NULL, 1, 0)) > 0 THEN '0'
                        ELSE '1'
                      END,
                      Material_Id, material_name.Name, Material_Price
                    FROM cut
                      LEFT JOIN pack ON cut.Id = pack.Cut_Id
                      LEFT JOIN material_name ON cut.Material_Id = material_name.Id
                    WHERE cut.Id = %s"""
        sql_info = my_sql.sql_select(query, (sql_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить данные кроя")
            return False

        self.__id = sql_info[0][0]
        self.__number = sql_info[0][0]
        self.__date_cut = sql_info[0][1]
        self.__worker_class = sql_info[0][2]
        self.__weight = sql_info[0][3]
        self.__weight_rest = sql_info[0][4]
        self.__note = sql_info[0][5]
        if sql_info[0][6] == '1':
            self.__complete = True
        else:
            self.__complete = False
        self.__material_id = sql_info[0][7]
        self.__material_name = sql_info[0][8]
        self.__material_name = sql_info[0][9]


        return True

    def take_pack_sql(self):
        if self.__id is None:
            print("Не верный ID")
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

    # Получекние значений
    def id(self):
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

    def take_new_number_pack(self):
        if self.__pack_id_dict is None:
            return 1
        else:
            pass

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

    def set_worker_id(self, id):
        if self.__worker_id != int(id):
            self.__worker_id = int(id)

            if not self.__save_sql_info:
                    self.__save_sql_info = True

    def set_note(self, note):
        if self.__note != str(note):
            self.__note = str(note)

            if not self.__save_sql_info:
                    self.__save_sql_info = True

    def set_weight_rest(self, weight):
        if self.__weight_rest != float(weight.replace(",", ".")):
            self.__weight_rest = float(weight.replace(",", "."))

            if not self.__save_sql_info:
                    self.__save_sql_info = True


class Pack:
    def __init__(self, id=None):
        self.__id = None
        self.__cut_id = None
        self.__material_id = None
        self.__client_id = None
        self.__article_parametr = None
        self.__number_pack = None
        self.__number_cut = None
        self.__value_pieces = None
        self.__value_damage = None
        self.__value_all = None
        self.__weight = None
        self.__note = None
        self.__size = None
        self.__date_make = None
        self.__date_complete = None
        self.__order = None

        self.__save_sql_info = False

        self.__operation = []
        self.__accessories = []

        if id is not None:
            self.set_sql_info(id)

        self.__new_operation_count = -1
        self.__new_accessories_count = -1

        # Учесть при сохранении
        self.__save_operation_sql = []
        self.__dell_operation_sql = []
        self.__save_accessories_sql = []
        self.__dell_accessories_sql = []
        self.__dell_client = False
        self.__dell_order = False

    # sql функции
    def set_sql_info(self, sql_id=None):
        if sql_id is None and self.__id is None:
            print("Неверный id пачки")
            return False

        query = """SELECT pack.Id, pack.Cut_Id, pack.Material_Id, pack.Client_Id, pack.Number, pack.Value_Pieces, pack.Value_Damage,
                      pack.Weight, pack.Note, pack.Size, pack.Date_Make, pack.Date_Coplete
                    FROM pack
                    WHERE pack.Id = %s"""
        sql_info = my_sql.sql_select(query, (sql_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить данные пачки")
            return False

        self.__id = sql_info[0][0]
        self.__cut_id = sql_info[0][1]
        self.__material_id = sql_info[0][2]
        self.__client_id = sql_info[0][3]
        self.__number = sql_info[0][4]
        self.__value_pieces = sql_info[0][5]
        self.__value_damage = sql_info[0][6]
        self.__weight = sql_info[0][7]
        self.__note = sql_info[0][8]
        self.__size = sql_info[0][9]
        self.__date_make = sql_info[0][10]
        self.__date_complete = sql_info[0][11]
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
                             "value": None,
                             "price": item[3]}
                self.__save_operation_sql.append(self.__new_operation_count)
                self.__new_operation_count -= 1
                self.__operation.append(operation)
            return self.__operation
        else:
            print("Нету артикула")
            return False

    def take_article_accessories(self):
        if self.__article_parametr:
            query = """SELECT material.Id, accessories_name.Name, accessories_supplyposition.Price, material.Value, MIN(Data)
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
                               "value": item[3],
                               "fifo_id": None}
                self.__save_accessories_sql.append(self.__new_accessories_count)
                self.__new_accessories_count -= 1
                self.__accessories.append(accessories)
            return self.__accessories
        else:
            print("Нету артикула")
            return False

    # Получекние значений

    def id(self):
        return self.__id

    def value(self):
        return self.__value_pieces

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

    def accessories(self):
        return self.__accessories

    def accessory(self, id):
        for accessory in self.__accessories:
                if accessory["id"] == id:
                    return accessory

    def value_all(self):
        return self.__value_all


    # Вставка заначений
    def set_number_pack(self, number):
        if number == "":
            if self.__number_pack != int(number):
                self.__number_pack = int(number)

            if not self.__save_sql_info:
                    self.__save_sql_info = True

    def set_number_cut(self, number):
        if number == "":
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
            else:
                raise RuntimeError("Не тот тип данных!")

    def set_size(self, size):
        if size != "":
            if self.__size != int(size):
                self.__size = int(size)

                if not self.__save_sql_info:
                        self.__save_sql_info = True

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
            if self.__weight != float(value.replace(",", ".")):
                self.__weight = float(value.replace(",", "."))

                if not self.__save_sql_info:
                        self.__save_sql_info = True

    def set_operation(self, info, id=None):
        if id is not None:
            for operation in self.__operation:
                if operation["id"] == id:
                    edit_operation = operation
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
                              "price": None}
            self.__save_operation_sql.append(self.__new_operation_count)
            self.__new_operation_count -= 1
            self.__operation.append(edit_operation)
        else:
            raise RuntimeError("Что то пошло не так со вставкой операции (id)")

        edit_operation["position"] = info["position"]
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

    def set_accessories(self, info, id=None):
        if id is not None:
            for accessories in self.__accessories:
                if accessories["id"] == id:
                    edit_accessories = accessories
                    self.__save_accessories_sql.append(accessories["id"])
                    break
            else:
                raise RuntimeError("Что то пошло не так со вставкой фурнитуры (id в for)")


        elif id is None:
            edit_accessories = {"id": self.__new_operation_count,
                                "accessories_id": None,
                                "accessories_name": None,
                                "price": None,
                                "value": None,
                                "fifo_id": None}
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

    def set_order(self, id):
        self.__order = int(id)


    #Удаление значений
    def del_operation(self, id):
        if id < 0:
            for e in enumerate(self.__operation):
                if e[1]["id"] == id:
                    self.__operation.pop(e[0])
                    return True
            else:
                return False
        else:
            for e in enumerate(self.__operation):
                if e[1]["id"] == id:
                    self.__operation.pop(e[0])
                    self.__dell_operation_sql.append(e[0])
                    return True

        return False

    def del_client(self):
        self.__dell_client = True
        self.__client_id = None

    def del_order(self):
        self.__dell_order = True
        self.__order = None


    #Разные функции
    def calc_value(self):
        if self.__value_pieces is not None:
            if self.__value_damage is None:
                damage = 0
            else:
                damage = self.__value_damage
            self.__value_all = self.__value_pieces - damage





class Worker:
    def __init__(self, id=None):
        self.__id = None
        self.__first_Name = None
        self.__last_Name = None
        self.__middle_Name = None
        self.__sex = None
        self.__date_birth = None
        self.__date_recruitment = None
        self.__leave = None
        self.__date_leave = None
        self.__country_name = None
        self.__phone = None
        self.__address = None
        self.__position_name = None
        self.__birthplace = None
        self.__note = None

        if id is not None:
            self.set_sql_info(id)

    def set_sql_info(self, sql_id=None):
        if sql_id is None and self.__id is None:
            print("Неверный id работника")
            return False

        query = """SELECT info.Id, info.First_Name, info.Last_Name, info.Middle_Name, info.Sex, info.Date_Birth, info.Date_Recruitment, info.`Leave`,
                      info.Date_Leave, staff_country.Country_name, info.Phone, info.Address, staff_position.Name, info.Birthplace, info.Note
                    FROM staff_worker_info AS info
                        LEFT JOIN staff_position ON info.Position_Id = staff_position.Id
                        LEFT JOIN staff_country ON info.Country_Id = staff_country.Id
                    WHERE info.Id = $s"""
        sql_info = my_sql.sql_select(query, (sql_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить данные работника")
            return False

        self.__id = sql_info[0][0]
        self.__first_Name = sql_info[0][1]
        self.__last_Name = sql_info[0][2]
        self.__middle_Name = sql_info[0][3]
        self.__sex = sql_info[0][4]
        self.__date_birth = sql_info[0][5]
        self.__date_recruitment = sql_info[0][6]
        if int(sql_info[0][7]):
            self.__leave = True
            self.__date_leave = sql_info[0][8]
        else:
            self.__leave = False
            self.__date_leave = None
        self.__country_name = sql_info[0][9]
        self.__phone = sql_info[0][10]
        self.__address = sql_info[0][11]
        self.__position_name = sql_info[0][12]
        self.__birthplace = sql_info[0][13]
        self.__note = sql_info[0][14]
        return True
