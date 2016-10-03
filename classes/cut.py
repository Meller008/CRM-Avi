from function import my_sql


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
    def __init__(self):
        self.__id = None
        self.__date_cut = None
        self.__worker_id = None
        self.__weight = None
        self.__weight_rest = None
        self.__note = None
        self.__complete = None
        self.__pack_id_dict = None

    def set_sql_info(self, sql_id=None):
        if sql_id is None and self.__id is None:
            print("Не верный ID")
            return False
        query = """SELECT cut.Id, cut.Date_Cut, cut.Worker_Id, SUM(pack.Weight), cut.Weight_Rest, cut.Note,
                      CASE
                        WHEN SUM(IF(pack.Date_Coplete IS NULL, 1, 0)) > 0 THEN '0'
                        ELSE '1'
                      END
                    FROM cut
                      LEFT JOIN pack ON cut.Id = pack.Cut_Id
                    WHERE cut.Id = %s"""
        sql_info = my_sql.sql_select(query, (sql_id,))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить данные кроя")
            return False

        self.__id = sql_info[0][0]
        self.__date_cut = sql_info[0][1]
        self.__worker_class = sql_info[0][2]
        self.__weight = sql_info[0][3]
        self.__weight_rest = sql_info[0][4]
        self.__note = sql_info[0][5]
        if sql_info[0][6] == '1':
            self.__complete = True
        else:
            self.__complete = False

        return True

    def set_pack_sql(self):
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

    def id(self):
        return self.__id

    def pack(self, id_pack):
            pack = self.__pack_id_dict.get(id_pack)
            if pack is not None:
                return pack
            else:
                print("Нет пачки с таким ID в крое")
                return False


class Pack:
    def __init__(self, id=None):
        self.__id = None
        self.__cut_id = None
        self.__material_id = None
        self.__client_id = None
        self.__number = None
        self.__value_piecec = None
        self.__value_damage = None
        self.__weight = None
        self.__note = None
        self.__size = None
        self.__date_make = None
        self.__date_complete = None

        if id is not None:
            self.set_sql_info(id)

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
        self.__value_piecec = sql_info[0][5]
        self.__value_damage = sql_info[0][6]
        self.__weight = sql_info[0][7]
        self.__note = sql_info[0][8]
        self.__size = sql_info[0][9]
        self.__date_make = sql_info[0][10]
        self.__date_complete = sql_info[0][11]
        return True

    def value(self):
        return self.__value_piecec


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
