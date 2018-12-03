""" Модуль содержит клас работника и все с ним связаное"""


class Worker:
    """"Класс работника"""

    def __init__(self, _id, first_name, last_name, middle_name, sex, date_birth, date_recruitment,
                 leave, date_leave, phone, address, inn, snils, note, birthplace, country, position,
                 insurance, migration_card, passport, patent, registration, account, card):

        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.sex = sex
        self.date_birth = date_birth
        self.date_recruitment = date_recruitment
        self.leave = leave
        self.date_leave = date_leave
        self.phone = phone
        self.address = address
        self.inn = inn
        self.snils = snils
        self.note = note
        self.birthplace = birthplace

        # другие классы
        self.country = country
        self.position = position
        self.insurance = insurance
        self.migration_card = migration_card
        self.passport = passport
        self.patent = patent
        self.registration = registration
        self.account = account
        self.card = card

    @classmethod
    def new(cls):
        return cls(None, None, None, None, None, None, None, None, None, None, None,
                   None, None, None, None, None, None, None, None, None, None, None)

