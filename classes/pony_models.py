""" Модуль содержит модели таблиц для БД Пони ОРМ"""

from datetime import date
from decimal import Decimal
from pony.orm import *


db = Database(provider='mysql', host='192.168.1.24', user='crm', passwd='Aa088011', db='avi_crm')


class Staff_position(db.Entity):
    """"Модель позиции вакансии для работника"""
    id = PrimaryKey(int, auto=True)
    name = Required(str, 45)
    number = Optional(str, 6)
    worker = Set("Staff_worker_info")


class Staff_country(db.Entity):
    """"Модель страны для работника"""
    id = PrimaryKey(int, auto=True)
    name = Required(str, 45, column="country_name")
    patent = Required(bool)
    act = Optional(str)
    worker = Set("Staff_worker_info")


class Staff_worker_info(db.Entity):
    """"Модель работника"""
    id = PrimaryKey(int, auto=True)
    first_name = Required(str, 40)
    last_name = Required(str, 40)
    middle_name = Optional(str, 40)
    sex = Required(str, 1)
    date_birth = Required(date)
    date_recruitment = Required(date)
    leave = Required(bool)
    date_leave = Optional(date)
    phone = Optional(str, 17)
    address = Optional(str, 80)
    inn = Optional(str, 13)
    snils = Optional(str, 15)
    note = Optional(str)
    birthplace = Optional(str, 78)
    country = Required(Staff_country, column="Country_Id")
    position = Required(Staff_position, column="Position_Id")
    insurance = Optional("Staff_worker_insurance")
    migration_card = Optional("Staff_worker_migration")
    passport = Optional("Staff_worker_passport")
    patent = Optional("Staff_worker_patent")
    registration = Optional("Staff_worker_registraton")
    account = Optional("Staff_worker_login")
    card = Optional("Staff_worker_kard")


class Staff_worker_insurance(db.Entity):
    """Модель страховки для работника"""
    id = PrimaryKey(int, auto=True)
    number = Required(str, 25)
    company = Required(str, 30)
    date = Required(date)
    worker_info_id = Required(Staff_worker_info)


class Staff_worker_migration(db.Entity):
    """Модель миграционной карты для работника"""
    id = PrimaryKey(int, auto=True)
    serial = Required(str, 5)
    number = Required(str, 8)
    kpp = Required(str, 15)
    date_validity_from = Required(date)  # Срок действия С
    date_validity_to = Required(date)  # Срок действия ДО
    date_migration = Required(date)  # Дата выдачи
    worker_info_id = Required(Staff_worker_info)


class Staff_worker_passport(db.Entity):
    """Модель паспорта для работника"""
    id = PrimaryKey(int, auto=True)
    series = Optional(str, 6)
    number = Required(str, 12)
    issued = Required(str, 40)
    data_issued = Required(date)  # Дата выдачи
    date_ending = Required(date)  # Дата окончания
    worker_info_id = Required(Staff_worker_info)


class Staff_worker_patent(db.Entity):
    """Модель патента для работника"""
    id = PrimaryKey(int, auto=True)
    serial = Required(str, 6)
    number = Required(str, 12)
    additional_Number = Required(str, 12)  # Дополнительный номер
    issued = Required(str, 38)
    data_Issued = Required(date)  # Дата выдачи
    date_Ending = (date)  # Дата окончания
    worker_info_id = Required(Staff_worker_info)


class Staff_worker_registraton(db.Entity):
    """Модель регистрации для работника"""
    id = PrimaryKey(int, auto=True)
    address = Required(str, 90)
    date_Registration = Optional(date)  # Дата постановки
    date_Validity_From = Optional(date)  # Срок пребывания С
    date_Validity_To = Optional(date)  # Срок пребывания ДО
    worker_info_id = Required(Staff_worker_info)


class Staff_worker_login(db.Entity):
    """Модель логина для работника"""
    worker_id = PrimaryKey(Staff_worker_info, column="Worker_Info_Id")
    login = Required(str, 20, unique=True)
    password = Optional(str, 20)


class Staff_worker_kard(db.Entity):
    """Модель карты посещения для работника"""
    worker_id = PrimaryKey(Staff_worker_info)
    card_id = Required(str, 20, unique=True)





db.generate_mapping()
set_sql_debug(True)


@db_session
def print_pos():
    print("Тест вакансий:: ", Staff_position[10].name)
    print("Тест стран для работников:: ", Staff_country[7].name)
    print("Тест работников:: ", Staff_worker_info[1].first_name + " " + Staff_worker_info[1].last_name)
    print("Тест страховки через работников:: ", Staff_worker_info[105].insurance.number)
    print("Тест миграционной карты через работников:: ", Staff_worker_info[105].migration_card.number)
    print("Тест паспорта через работников:: ", Staff_worker_info[105].passport.number)
    print("Тест патента через работников:: ", Staff_worker_info[105].patent.number)
    print("Тест регистрации через работников:: ", Staff_worker_info[105].registration.address)
    print("Тест логина через работников:: ", Staff_worker_info[105].account.login)
    print(Staff_worker_registraton.select(lambda r: r.worker_info_id.id == 138)[:])


#print_pos()