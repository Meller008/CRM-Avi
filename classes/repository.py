""" Модуль содержит мапперы. Превращает данные из моделей в обекты и наоборот."""

from classes.pony_models import Staff_worker_info, Staff_position
from classes.worker import Worker
from pony.orm import db_session, left_join
from collections import namedtuple


class WorkerRepository:
    """Репозиторий работников"""

    @db_session
    def find(self, _id):
        """Поиск работника по ID"""
        model_worker = Staff_worker_info[_id]

        new_worker = Worker(model_worker.id, model_worker.first_name, model_worker.last_name, model_worker.middle_name,
                            model_worker.sex, model_worker.date_birth, model_worker.date_recruitment, model_worker.leave,
                            model_worker.date_leave, model_worker.phone, model_worker.address, model_worker.inn,
                            model_worker.snils, model_worker.note, model_worker.birthplace, model_worker.country,
                            model_worker.position, model_worker.insurance, model_worker.migration_card, model_worker.passport,
                            model_worker.patent, model_worker.registration, model_worker.account, model_worker.card)

        return new_worker

    @db_session
    def list(self):
        """Возвращает именуемый список всех работников

        id first_name last_name middle_name date_recruitment leave date_leave login country"""

        WorkerTuple = namedtuple("Worker", "id first_name last_name middle_name date_recruitment leave date_leave login country")
        list_workers = []
        for model_worker in left_join((w.id, w.first_name, w.last_name, w.middle_name, w.date_recruitment,
                                       w.leave, w.date_leave, w.account.login, w.country.name)
                                      for w in Staff_worker_info):
            list_workers.append(WorkerTuple(*model_worker))

        return list_workers


class WorkerPositionRepository:
    """Репозиторий вакансий"""
    @db_session
    def list(self):
        """Возвращает список вакансий"""
        return Staff_position.select()[:]
