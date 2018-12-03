""""Этот модуль содержит функцию создания колонок в таблице"""

from PyQt5.QtWidgets import QTableWidgetItem


def set_table_columns(widget, column_list, clear_widget=True):
    """Функция генерирует колоки в QTableWidget

        table_widget - виджет таблиццы QTableWidget
        column_list - список колон вида [ [имя, размер], [имя, размер], ... ]
        clear_widget - Очистить виджет перед вставкой данных"""

    if clear_widget:
        widget.clearContents()
        widget.setRowCount(0)

    for column, data in enumerate(column_list):
        widget.insertColumn(column)
        widget.setHorizontalHeaderItem(column, QTableWidgetItem(data[0]))
        widget.horizontalHeader().resizeSection(column, int(data[1]))
