"""Этот модуль отвечает за вставку списков в таблицы, листы, деревья"""

from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem
from PyQt5.QtCore import Qt, QDate
from decimal import Decimal
import datetime
import re


def list_widget(widget, data_list, first_id=True, clear_widget=True):
    """Вставка списка в QListWidget

        widget - Виджет в который будут вставляться данные
        data_list - Данные в виде списка [ [id, значение], [id, значение], ... ]
        first_id - Первое значение ID и оно будет вставленно в data(-1)
        clear_widget - Очистить виджет перед вставкой данных
    """
    if clear_widget:
        widget.clear()

    for data in data_list:
        new_row = QListWidgetItem(str(data[1]))

        if first_id:
            new_row.setData(-1, data[0])

        widget.addItem(new_row)

    return True


def table_widget(widget, data_list, first_id=True, clear_widget=True):
    """Вставка списка в QTableWidget

        widget - Виджет в который будут вставляться данные
        data_list - Данные в виде списка [ [id, значение], [id, значение], ... ]
        first_id - Первое значение ID и оно будет вставленно в data(-1)
        clear_widget - Очистить виджет перед вставкой данных
    """

    class QTableWidgetItemDecimal(QTableWidgetItem):
        """Класс QTableWidgetItem для сортировки чисел c точкой и пробелом
            Этот класс наследуется от QTableWidgetItem. Но в нем изменена функция сортировки
            что бы таблица сортировала ячейки как пологоается по числу"""
        def __lt__(self, other):
            return Decimal(self.text().replace(" ", "")) < Decimal(other.text().replace(" ", ""))

    if clear_widget:
        widget.clearContents()
        widget.setRowCount(0)

    if first_id:  # Если у нас в данных первое знаечение ID, то вставлять надо со следующегго знвчения
        start_column = -1
    else:
        start_column = 0

    widget.setSortingEnabled(False)  # отключаем сортировку для избежания ошибок
    for row_data in data_list:
        widget.insertRow(widget.rowCount())

        data_1 = None  # Переменная для хранения значения Id и вставки в -1
        for column, data in enumerate(row_data, start_column):
            if first_id and column == -1:  # Если задано что первое значение это ID, то пропустим это первое значение
                data_1 = data
                continue

            if isinstance(data, Decimal):  # Если вставляемое значение Decimal
                text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(data))
                item = QTableWidgetItemDecimal(text)

            elif isinstance(data, datetime.date):  # Если вставляемое значение дата
                q_date = QDate(data.year, data.month, data.day)
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, q_date)

            else:
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, data)

            if first_id and data_1:
                item.setData(-1, data_1)

            widget.setItem(widget.rowCount() - 1, column, item)

    widget.setSortingEnabled(True)

    return True
