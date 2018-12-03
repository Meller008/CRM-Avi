"""Все окна связанные с работниками"""

from os import getcwd

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from classes.repository import WorkerPositionRepository, WorkerRepository
from function.widget import set_list_to, table_column


class WorkerListWindow(QDialog):
    """Окно скписка оабочих"""
    def __init__(self):
        super(WorkerListWindow, self).__init__()
        loadUi(getcwd() + '/ui/new/worker_list.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()
        self.set_position_list()
        self.set_worker_list()

    def set_start_settings(self):
        """Установка стандартных настроек при запуске окна"""
        self.set_icon_to_buttons()

        column = (("Фамилия", 130), ("Имя", 130), ("Дата приема", 90), ("Логин", 50), ("Гражданство", 160), ("Дата увольн.", 90))
        table_column.set_table_columns(self.tw_worker, column)

    def set_icon_to_buttons(self):
        """Вставляет икони в кнопки"""
        self.pb_add_list.setIcon(QIcon(getcwd() + "/images/add_list.png"))
        self.pb_add_list.setIconSize(QSize(30, 30))

        self.pb_edit_list.setIcon(QIcon(getcwd() + "/images/edit_list.png"))
        self.pb_edit_list.setIconSize(QSize(30, 30))

        self.pb_del_list.setIcon(QIcon(getcwd() + "/images/del_list.png"))
        self.pb_del_list.setIconSize(QSize(30, 30))

        self.pb_add_doc.setIcon(QIcon(getcwd() + "/images/new_doc.png"))
        self.pb_add_doc.setIconSize(QSize(30, 30))

        self.pb_change_doc.setIcon(QIcon(getcwd() + "/images/edit_doc.png"))
        self.pb_change_doc.setIconSize(QSize(30, 30))

        self.pb_del_doc.setIcon(QIcon(getcwd() + "/images/del_doc.png"))
        self.pb_del_doc.setIconSize(QSize(30, 30))

        self.pb_copy_doc.setIcon(QIcon(getcwd() + "/images/copy_doc.png"))
        self.pb_copy_doc.setIconSize(QSize(30, 30))

        self.pb_filter.setIcon(QIcon(getcwd() + "/images/filter.png"))
        self.pb_filter.setIconSize(QSize(30, 30))

        self.pb_menu.setIcon(QIcon(getcwd() + "/images/menu.png"))
        self.pb_menu.setIconSize(QSize(30, 30))

    def set_position_list(self):
        """Вставляет список вакансий"""
        worker_position_list = WorkerPositionRepository().list()
        set_position_list = [[position.id, position.name] for position in worker_position_list]  # Генерируем список для вставки
        set_list_to.list_widget(self.lw_position, set_position_list)

    def set_worker_list(self):
        """Вставка списка работников"""
        worker_list = WorkerRepository().list()
        set_worker_list = [[worker.id, worker.last_name, worker.first_name, worker.date_recruitment,  # Генерируем список для вставки
                            worker.login, worker.country, worker.date_leave]
                           for worker in worker_list]
        set_list_to.table_widget(self.tw_worker, set_worker_list)
