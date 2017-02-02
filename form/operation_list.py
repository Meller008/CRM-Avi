from os import getcwd
from form import staff
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from form.pack import PackBrows
from form.templates import table


operation_pack_filter = loadUiType(getcwd() + '/ui/operation_pack_filter.ui')[0]


class PayList(table.TableList):
    def set_settings(self):

        self.filter = None

        self.setWindowTitle("Доплаты и вычеты")  # Имя окна
        self.resize(900, 270)
        self.pb_copy.deleteLater()
        self.toolBar.setStyleSheet("background-color: rgb(255, 255, 255);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("Швея", 115), ("Операция", 200), ("Крой", 35), ("Пачка", 45), ("Цена", 55), ("Кол-во", 50), ("Итого", 65),
                                  ("Дата пошива", 85), ("Дата внесения", 110), ("Дата оплаты", 100))

        self.pb_add.deleteLater()
        self.pb_change.deleteLater()
        self.pb_dell.deleteLater()
        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()

        self.query_table_all = """SELECT pack.Id, CONCAT(work.Last_Name, ' ', work.First_Name), pack_operation.Name, cut.Id, pack.Number, pack_operation.Price, pack_operation.Value,
                                        pack_operation.Price* pack_operation.Value, DATE_FORMAT(pack_operation.Date_make, '%d.%m.%Y'),
                                        DATE_FORMAT(pack_operation.Date_Input, '%d.%m.%Y %H:%i:%S'), DATE_FORMAT(pack_operation.Date_Pay, '%d.%m.%Y')
                                      FROM pack_operation
                                        LEFT JOIN pack ON pack_operation.Pack_Id = pack.Id
                                        LEFT JOIN cut ON pack.Cut_Id = cut.Id
                                        LEFT JOIN staff_worker_info AS work ON pack_operation.Worker_Id = work.Id"""

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT pack.Id, CONCAT(work.Last_Name, ' ', work.First_Name), pack_operation.Name, cut.Id, pack.Number, pack_operation.Price, pack_operation.Value,
                                        pack_operation.Price* pack_operation.Value, DATE_FORMAT(pack_operation.Date_make, '%d.%m.%Y'),
                                        DATE_FORMAT(pack_operation.Date_Input, '%d.%m.%Y %H:%i:%S'), DATE_FORMAT(pack_operation.Date_Pay, '%d.%m.%Y')
                                      FROM pack_operation
                                        LEFT JOIN pack ON pack_operation.Pack_Id = pack.Id
                                        LEFT JOIN cut ON pack.Cut_Id = cut.Id
                                        LEFT JOIN staff_worker_info AS work ON pack_operation.Worker_Id = work.Id"""

        self.query_table_dell = ""

    def ui_add_table_item(self):  # Добавить предмет
        pass

    def ui_change_table_item(self, id=False):  # изменить элемент
        self.pack = PackBrows(pack_id=id)
        self.pack.setWindowModality(Qt.ApplicationModal)
        self.pack.show()

    def ui_filter(self):
        if self.filter is None:
            self.filter = PayListFilter(self)
        self.filter.of_set_sql_query(self.query_table_all)
        self.filter.setWindowModality(Qt.ApplicationModal)
        self.filter.show()

    def of_set_filter(self, sql):
        self.query_table_select = sql

        self.ui_update()


class PayListFilter(QDialog, operation_pack_filter):
    def __init__(self, main):
        super(PayListFilter, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main

    def ui_view_staff(self):
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_del_work(self):
        self.le_work.setWhatsThis("")
        self.le_work.setText("")

    def ui_acc(self):
        where = ""

        # Блок  условий состояния операции
        where_item = ""
        if self.cb_operation_nul.isChecked():
            where_item = self.add_filter(where_item, "pack_operation.Worker_Id IS NULL", False)

        if self.cb_operation_in.isChecked():
            where_item = self.add_filter(where_item, "pack_operation.Worker_Id IS NOT NULL", False)

        if self.cb_operation_pay.isChecked():
            where_item = self.add_filter(where_item, "pack_operation.Pay = 1", False)

        if where_item:
            where_item = "(" + where_item + ")"
            where = self.add_filter(where, where_item)

        # Блок  условий даты оплаты операции
        if self.gp_date_pay.isChecked():
            sql_date = "(pack_operation.Date_Pay >= '%s' AND pack_operation.Date_Pay <= '%s')" % (self.de_date_pay_from.date().toString(Qt.ISODate), self.de_date_pay_to.date().toString(Qt.ISODate))
            where = self.add_filter(where, sql_date)

        # Блок  условий состояния пачки
        where_item = ""
        if self.cb_pack_none.isChecked():
            where_item = self.add_filter(where_item, "(pack.Date_Make IS NULL AND pack.Date_Coplete IS NULL)", False)

        if self.cb_pack_make.isChecked():
            where_item = self.add_filter(where_item, "pack.Date_Make IS NOT NULL AND pack.Date_Coplete IS NULL", False)

        if self.cb_pack_complette.isChecked():
            where_item = self.add_filter(where_item, "pack.Date_Coplete IS NOT NULL AND pack.Date_Make IS NULL", False)

        if self.cb_pack_ok.isChecked():
            where_item = self.add_filter(where_item, "(pack.Date_Make IS NOT NULL AND pack.Date_Coplete IS NOT NULL)", False)

        if where_item:
            where_item = "(" + where_item + ")"
            where = self.add_filter(where, where_item)

        # Блок  условий даты проверки пачки
        if self.gb_date_complette.isChecked():
            sql_date = "(pack.Date_Coplete >= '%s' AND pack.Date_Coplete <= '%s')" % \
                       (self.de_pack_date_complette_from.date().toString(Qt.ISODate), self.de_pack_date_complette_to.date().toString(Qt.ISODate))
            where = self.add_filter(where, sql_date)

        # Блок  условий даты приемки пачки
        if self.gb_date_make.isChecked():
            sql_date = "(pack.Date_Make >= '%s' AND pack.Date_Make <= '%s')" % \
                       (self.de_pack_date_make_from.date().toString(Qt.ISODate), self.de_pack_date_make_to.date().toString(Qt.ISODate))
            where = self.add_filter(where, sql_date)

        # Блок  условий выбора швеи
        if self.le_work.whatsThis() != '':
            where = self.add_filter(where, "(pack_operation.Worker_Id = %s)" % self.le_work.whatsThis())

        self.sql_query_all = self.sql_query_all + " WHERE " + where

        self.main.of_set_filter(self.sql_query_all)

        self.close()

    def ui_can(self):
        self.close()
        self.destroy()

    def add_filter(self, where, add, and_add=True):
        if where:
            if and_add:
                where += " AND " + add
            else:
                where += " OR " + add
        else:
            where = add

        return where

    def of_list_worker(self, item):
        self.le_work.setWhatsThis(str(item[0]))
        self.le_work.setText(item[1])

    def of_set_sql_query(self, sql):
        self.sql_query_all = sql
