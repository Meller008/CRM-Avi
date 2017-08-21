from os import getcwd
from datetime import datetime
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QListWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt
from decimal import *
from function import my_sql, to_excel
from classes.my_class import User


salary_list = loadUiType(getcwd() + '/ui/salary_work.ui')[0]
salary_work = loadUiType(getcwd() + '/ui/salary_work_info.ui')[0]
salary_history = loadUiType(getcwd() + '/ui/salary_history.ui')[0]


class SalaryList(QDialog, salary_list):
    def __init__(self):
        super(SalaryList, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_size_table()

    def access(self):
        for item in User().access_list(self.__class__.__name__):
            a = getattr(self, item["atr1"])
            if item["atr2"]:
                a = getattr(a, item["atr2"])

            if item["value"]:
                if item["value"] == "True":
                    val = True
                elif item["value"] == "False":
                    val = False
                else:
                    val = item["value"]
                a(val)
            else:
                a()

    def start_sql_info(self):
        self.all_operation = 0
        self.all_plus = 0
        self.all_minus = 0
        self.salary = []
        query = """SELECT work.Id, CONCAT(work.Last_Name, ' ', work.First_Name) AS work_name, pack_operation.Id, pack_operation.Price * pack_operation.Value,
                        operations.Name ,pack_operation.Date_make, pack_operation.Date_Input, pack.Cut_Id, pack.Number
                      FROM pack_operation LEFT JOIN pack ON pack_operation.Pack_Id = pack.Id
                        LEFT JOIN operations ON pack_operation.Operation_id = operations.Id
                        LEFT JOIN staff_worker_info AS work ON pack_operation.Worker_Id = work.Id
                      WHERE pack_operation.Pay = 0 AND pack_operation.Worker_Id IS NOT NULL
                        AND pack.Date_Make IS NOT NULL AND pack.Date_Coplete IS NOT NULL
                      ORDER BY work_name, pack_operation.Date_Input"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить операции")
            return False

        previous_id = None
        id_in_salary = []
        for operation in sql_info:

            if previous_id != operation[0]:
                work = {
                        "worker_id": operation[0],
                        "worker_name": operation[1],
                        "operation_sum": 0,
                        "plus_sum": 0,
                        "plus_value": 0,
                        "minus_sum": 0,
                        "minus_value": 0,
                        "operation_list": [],
                        "p_m_list": []
                      }

                self.salary.append(work)
                previous_id = operation[0]
                id_in_salary.append(operation[0])

                work["operation_list"].append([operation[2], operation[3], operation[4], operation[5], operation[6], operation[7], operation[8]])
                work["operation_sum"] += operation[3]
                self.all_operation += operation[3]

            else:
                work["operation_list"].append([operation[2], operation[3], operation[4], operation[5], operation[6], operation[7], operation[8]])
                work["operation_sum"] += operation[3]
                self.all_operation += operation[3]

        query = """SELECT work.Id, CONCAT(work.Last_Name, ' ', work.First_Name) AS work_name, pay_worker.Id, pay_reason.Name, pay_worker.Balance,
                        pay_worker.Date_In_Pay, pay_worker.Note, admin.Last_Name
                      FROM pay_worker
                        LEFT JOIN staff_worker_info AS work ON pay_worker.Worker_Id = work.Id
                        LEFT JOIN pay_reason ON pay_worker.Reason_Id = pay_reason.Id
                        LEFT JOIN staff_worker_info AS admin ON pay_worker.Worker_Id_Insert = admin.Id
                      WHERE Pay = 0 AND Date_In_Pay <= %s
                      ORDER BY work_name, pay_worker.Date_In_Pay"""
        sql_info = my_sql.sql_select(query, (self.date_pay, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить доплаты вычеты")
            return False

        previous_id = None

        for p_m in sql_info:

            if p_m[0] != previous_id and p_m[0] not in id_in_salary:
                work = {
                        "worker_id": p_m[0],
                        "worker_name": p_m[1],
                        "operation_sum": 0,
                        "plus_sum": 0,
                        "plus_value": 0,
                        "minus_sum": 0,
                        "minus_value": 0,
                        "operation_list": [],
                        "p_m_list": []
                      }

                self.salary.append(work)
                previous_id = p_m[0]

                work["p_m_list"].append([p_m[2], p_m[3], p_m[4], p_m[5], p_m[6], p_m[7]])
                if p_m[4] > 0:
                    work["plus_sum"] += p_m[4]
                    work["plus_value"] += 1
                    self.all_plus += p_m[4]
                else:
                    work["minus_sum"] += -p_m[4]
                    work["minus_value"] += 1
                    self.all_minus += -p_m[4]

            elif p_m[0] != previous_id and p_m[0] in id_in_salary:

                # Если такой работник уже есть то ищем его
                for work_pay in self.salary:
                    if work_pay["worker_id"] == p_m[0]:
                        work = work_pay
                        break
                else:
                    QMessageBox.critical(self, "Ошибка", "Не найден работник при Д/В", QMessageBox.Ok)
                    return False

                previous_id = p_m[0]

                work["p_m_list"].append([p_m[2], p_m[3], p_m[4], p_m[5], p_m[6], p_m[7]])
                if p_m[4] > 0:
                    work["plus_sum"] += p_m[4]
                    work["plus_value"] += 1
                    self.all_plus += p_m[4]
                else:
                    work["minus_sum"] += -p_m[4]
                    work["minus_value"] += 1
                    self.all_minus += -p_m[4]

            else:
                previous_id = p_m[0]

                work["p_m_list"].append([p_m[2], p_m[3], p_m[4], p_m[5], p_m[6], p_m[7]])
                if p_m[4] > 0:
                    work["plus_sum"] += p_m[4]
                    work["plus_value"] += 1
                    self.all_plus += p_m[4]
                else:
                    work["minus_sum"] += -p_m[4]
                    work["minus_value"] += 1
                    self.all_minus += -p_m[4]

        self.set_table_info()

    def set_size_table(self):
        self.tw_main_salary.horizontalHeader().resizeSection(0, 155)
        self.tw_main_salary.horizontalHeader().resizeSection(1, 80)
        self.tw_main_salary.horizontalHeader().resizeSection(2, 80)
        self.tw_main_salary.horizontalHeader().resizeSection(3, 80)
        self.tw_main_salary.horizontalHeader().resizeSection(4, 80)
        self.tw_main_salary.horizontalHeader().resizeSection(5, 70)
        self.tw_main_salary.horizontalHeader().resizeSection(6, 60)
        self.tw_main_salary.horizontalHeader().resizeSection(7, 65)

        self.tw_main_salary_history.horizontalHeader().resizeSection(0, 155)
        self.tw_main_salary_history.horizontalHeader().resizeSection(1, 80)
        self.tw_main_salary_history.horizontalHeader().resizeSection(2, 80)
        self.tw_main_salary_history.horizontalHeader().resizeSection(3, 80)
        self.tw_main_salary_history.horizontalHeader().resizeSection(4, 80)
        self.tw_main_salary_history.horizontalHeader().resizeSection(5, 70)
        self.tw_main_salary_history.horizontalHeader().resizeSection(6, 60)
        self.tw_main_salary_history.horizontalHeader().resizeSection(7, 65)

        self.tw_many.horizontalHeader().resizeSection(0, 155)

    # окно расчета зп
    def ui_calc(self):
        date = self.de_pay_date.date()
        if date.toString(Qt.ISODate) == "2000-01-01":
            QMessageBox.critical(self, "Ошибка", "Выберите дату начисления зарплаты", QMessageBox.Ok)
            return False
        elif date.day() != date.daysInMonth():
            QMessageBox.critical(self, "Ошибка", "Вы выбрали не последний день. Пока это запрещено", QMessageBox.Ok)
            return False

        query = """SELECT COUNT(*)
                      FROM pack_operation
                      WHERE Date_Pay = %s"""
        sql_info = my_sql.sql_select(query, (date.toString(1), ))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог проверить дату")
            return False
        if sql_info[0][0] != 0:
            QMessageBox.critical(self, "Ошибка", "На эту дату уже был расчет", QMessageBox.Ok)
            return False

        self.date_pay = datetime(date.year(), date.month(), date.day()).date()

        self.start_sql_info()

    def ui_double_click(self, item):
        id = item.data(-2)

        for work_pay in self.salary:
            if work_pay["worker_id"] == id:
                self.work_info = SalaryInfo(work_pay)
                self.work_info.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.work_info.show()
                break

    def ui_save_salary(self):
        if not self.salary:
            return False

        sql_date = self.date_pay.strftime("%Y-%m-%d")
        result = QMessageBox.question(self, "Сохранить?", "Точно сохранить весь список в зарплату на %s?" % sql_date, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            operation_id_list = []
            p_m_id_list = []
            for work in self.salary:
                for operation in work["operation_list"]:
                    operation_id_list.append(operation[0])

                for p_m in work["p_m_list"]:
                    p_m_id_list.append(p_m[0])

            sql_date = self.date_pay.strftime("%Y-%m-%d")

            if operation_id_list:
                sql_date = self.date_pay.strftime("%Y-%m-%d")
                query = """UPDATE pack_operation SET Pay = 1, Date_Pay = '%s' WHERE Id IN %s""" % (sql_date, str(tuple(operation_id_list)).replace(",)", ")"))
                sql_info = my_sql.sql_change(query)
                if "mysql.connector.errors" in str(type(sql_info)):
                    print("Не смог поставить оплату операции")
                    return False

            if p_m_id_list:
                query = """UPDATE pay_worker SET Pay = 1, Date_Pay = '%s' WHERE Id IN %s""" % (sql_date, str(tuple(p_m_id_list)).replace(",)", ")"))
                sql_info = my_sql.sql_change(query)
                if "mysql.connector.errors" in str(type(sql_info)):
                    print("Не смог поставить оплату допдат и вычетов")
                    return False

        else:
            return False

    def ui_export_new_salary(self):
        path = QFileDialog.getSaveFileName(self, "Сохранение")
        if path[0]:
            to_excel.table_to_excel(self.tw_main_salary, path[0])

    # окно прошлой ЗП
    def ui_view_history_date(self):
        self.history = SalaryHistory()
        self.history.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.history.show()

        if self.history.exec() <= 0:
            return False

        self.all_operation_history = 0
        self.all_plus_history = 0
        self.all_minus_history = 0
        self.salary_history = []
        query = """SELECT work.Id, CONCAT(work.Last_Name, ' ', work.First_Name) AS work_name, pack_operation.Id, pack_operation.Price * pack_operation.Value,
                        operations.Name ,pack_operation.Date_make, pack_operation.Date_Input, pack.Cut_Id, pack.Number
                      FROM pack_operation LEFT JOIN pack ON pack_operation.Pack_Id = pack.Id
                        LEFT JOIN operations ON pack_operation.Operation_id = operations.Id
                        LEFT JOIN staff_worker_info AS work ON pack_operation.Worker_Id = work.Id
                      WHERE pack_operation.Date_Pay = %s
                      ORDER BY work_name, pack_operation.Date_Input"""
        sql_info = my_sql.sql_select(query, (self.history.date, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить операции")
            return False

        previous_id = None
        id_in_salary = []
        for operation in sql_info:

            if previous_id != operation[0]:
                work = {
                        "worker_id": operation[0],
                        "worker_name": operation[1],
                        "operation_sum": 0,
                        "plus_sum": 0,
                        "plus_value": 0,
                        "minus_sum": 0,
                        "minus_value": 0,
                        "operation_list": [],
                        "p_m_list": []
                      }

                self.salary_history.append(work)
                previous_id = operation[0]
                id_in_salary.append(operation[0])

                work["operation_list"].append([operation[2], operation[3], operation[4], operation[5], operation[6], operation[7], operation[8]])
                work["operation_sum"] += operation[3]
                self.all_operation_history += operation[3]

            else:
                work["operation_list"].append([operation[2], operation[3], operation[4], operation[5], operation[6], operation[7], operation[8]])
                work["operation_sum"] += operation[3]
                self.all_operation_history += operation[3]

        query = """SELECT work.Id, CONCAT(work.Last_Name, ' ', work.First_Name) AS work_name, pay_worker.Id, pay_reason.Name, pay_worker.Balance,
                        pay_worker.Date_In_Pay, pay_worker.Note, admin.Last_Name
                      FROM pay_worker
                        LEFT JOIN staff_worker_info AS work ON pay_worker.Worker_Id = work.Id
                        LEFT JOIN pay_reason ON pay_worker.Reason_Id = pay_reason.Id
                        LEFT JOIN staff_worker_info AS admin ON pay_worker.Worker_Id_Insert = admin.Id
                      WHERE Date_Pay = %s
                      ORDER BY work_name, pay_worker.Date_In_Pay"""
        sql_info = my_sql.sql_select(query, (self.history.date, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            print("Не смог получить доплаты вычеты")
            return False

        previous_id = None

        for p_m in sql_info:

            if p_m[0] != previous_id and p_m[0] not in id_in_salary:
                work = {
                        "worker_id": p_m[0],
                        "worker_name": p_m[1],
                        "operation_sum": 0,
                        "plus_sum": 0,
                        "plus_value": 0,
                        "minus_sum": 0,
                        "minus_value": 0,
                        "operation_list": [],
                        "p_m_list": []
                      }

                self.salary_history.append(work)
                previous_id = p_m[0]

                work["p_m_list"].append([p_m[2], p_m[3], p_m[4], p_m[5], p_m[6], p_m[7]])
                if p_m[4] > 0:
                    work["plus_sum"] += p_m[4]
                    work["plus_value"] += 1
                    self.all_plus_history += p_m[4]
                else:
                    work["minus_sum"] += -p_m[4]
                    work["minus_value"] += 1
                    self.all_minus_history += -p_m[4]

            elif p_m[0] != previous_id and p_m[0] in id_in_salary:

                # Если такой работник уже есть то ищем его
                for work_pay in self.salary_history:
                    if work_pay["worker_id"] == p_m[0]:
                        work = work_pay
                        break
                else:
                    QMessageBox.critical(self, "Ошибка", "Не найден работник при Д/В", QMessageBox.Ok)
                    return False

                previous_id = p_m[0]

                work["p_m_list"].append([p_m[2], p_m[3], p_m[4], p_m[5], p_m[6], p_m[7]])
                if p_m[4] > 0:
                    work["plus_sum"] += p_m[4]
                    work["plus_value"] += 1
                    self.all_plus_history += p_m[4]
                else:
                    work["minus_sum"] += -p_m[4]
                    work["minus_value"] += 1
                    self.all_minus_history += -p_m[4]

            else:
                previous_id = p_m[0]

                work["p_m_list"].append([p_m[2], p_m[3], p_m[4], p_m[5], p_m[6], p_m[7]])
                if p_m[4] > 0:
                    work["plus_sum"] += p_m[4]
                    work["plus_value"] += 1
                    self.all_plus_history += p_m[4]
                else:
                    work["minus_sum"] += -p_m[4]
                    work["minus_value"] += 1
                    self.all_minus_history += -p_m[4]

        self.tw_main_salary_history.clearContents()
        self.tw_main_salary_history.setRowCount(0)

        for row, salary in enumerate(self.salary_history):
            self.tw_main_salary_history.insertRow(row)

            new_table_item = QTableWidgetItem(str(salary["worker_name"]))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary_history.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(round(salary["operation_sum"] + salary["plus_sum"] - salary["minus_sum"], 2)))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary_history.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(round(salary["operation_sum"], 2)))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary_history.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(round(salary["plus_sum"], 2)))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary_history.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(round(salary["minus_sum"], 2)))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary_history.setItem(row, 4, new_table_item)

            new_table_item = QTableWidgetItem(str(len(salary["operation_list"])))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary_history.setItem(row, 5, new_table_item)

            new_table_item = QTableWidgetItem(str(salary["plus_value"]))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary_history.setItem(row, 6, new_table_item)

            new_table_item = QTableWidgetItem(str(salary["minus_value"]))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary_history.setItem(row, 7, new_table_item)

        self.le_all_operation_history.setText(str(round(self.all_operation_history, 2)))
        self.le_all_plus_history.setText(str(round(self.all_plus_history, 2)))
        self.le_all_minus_history.setText(str(round(self.all_minus_history, 2)))
        self.le_all_sum_history.setText(str(round((self.all_operation_history + self.all_plus_history) - self.all_minus_history, 2)))

    def ui_double_click_history(self, item):
        id = item.data(-2)

        for work_pay in self.salary_history:
            if work_pay["worker_id"] == id:
                self.work_info = SalaryInfo(work_pay)
                self.work_info.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.work_info.show()
                break

    def set_table_info(self):

        self.tw_main_salary.clearContents()
        self.tw_main_salary.setRowCount(0)

        for row, salary in enumerate(self.salary):
            self.tw_main_salary.insertRow(row)

            new_table_item = QTableWidgetItem(str(salary["worker_name"]))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(round(salary["operation_sum"] + salary["plus_sum"] - salary["minus_sum"], 2)))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(round(salary["operation_sum"], 2)))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(round(salary["plus_sum"], 2)))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(round(salary["minus_sum"], 2)))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary.setItem(row, 4, new_table_item)

            new_table_item = QTableWidgetItem(str(len(salary["operation_list"])))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary.setItem(row, 5, new_table_item)

            new_table_item = QTableWidgetItem(str(salary["plus_value"]))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary.setItem(row, 6, new_table_item)

            new_table_item = QTableWidgetItem(str(salary["minus_value"]))
            new_table_item.setData(-2, salary["worker_id"])
            self.tw_main_salary.setItem(row, 7, new_table_item)

        self.le_all_operation.setText(str(round(self.all_operation, 2)))
        self.le_all_plus.setText(str(round(self.all_plus, 2)))
        self.le_all_minus.setText(str(round(self.all_minus, 2)))
        self.le_all_sum.setText(str(round((self.all_operation + self.all_plus) - self.all_minus, 2)))

    def ui_export_salary(self):
        path = QFileDialog.getSaveFileName(self, "Сохранение")
        if path[0]:
            to_excel.table_to_excel(self.tw_main_salary_history, path[0])

    # сводное окно
    def ui_calc_many(self):
        table_column = {}
        table_row = {}
        date_from = self.de_date_many_from.date().toString(Qt.ISODate)
        date_to = self.de_date_many_to.date().toString(Qt.ISODate)

        self.tw_many.clearContents()
        self.tw_many.setRowCount(0)
        self.tw_many.setColumnCount(1)

        query = """SELECT CONCAT(work.Last_Name, ' ', work.First_Name) as w, pack_operation.Date_Pay,
                        SUM(pack_operation.Price * pack_operation.Value)
                      FROM staff_worker_info AS work LEFT JOIN pack_operation ON work.Id = pack_operation.Worker_Id
                      WHERE pack_operation.Pay = 1 AND pack_operation.Date_Pay >= %s AND pack_operation.Date_Pay <= %s
                      GROUP BY pack_operation.Date_Pay, w"""
        sql_info_operation = my_sql.sql_select(query, (date_from, date_to))
        if "mysql.connector.errors" in str(type(sql_info_operation)):
            print("Не смог получить операции")
            return False

        query = """SELECT CONCAT(work.Last_Name, ' ', work.First_Name) as w, pay_worker.Date_Pay, SUM(pay_worker.Balance)
                      FROM staff_worker_info AS work LEFT JOIN pay_worker ON work.Id = pay_worker.Worker_Id
                      WHERE pay_worker.Pay = 1 AND pay_worker.Date_Pay >= %s AND pay_worker.Date_Pay <= %s
                      GROUP BY pay_worker.Date_Pay, w"""
        sql_info_p_m = my_sql.sql_select(query, (date_from, date_to))
        if "mysql.connector.errors" in str(type(sql_info_operation)):
            print("Не смог получить доплаты вычеты")
            return False

        row = 0
        col = 1
        for operation in sql_info_operation:
            if table_row.get(operation[0]) is None:
                table_row[operation[0]] = row
                item = QTableWidgetItem(str(operation[0]))
                self.tw_many.insertRow(row)
                self.tw_many.setItem(row, 0, item)
                row += 1

            if table_column.get(operation[1]) is None:
                table_column[operation[1]] = col
                self.tw_many.insertColumn(col)
                self.tw_many.setHorizontalHeaderItem(col, QTableWidgetItem(operation[1].strftime("%d.%m.%Y")))
                self.tw_many.horizontalHeader().resizeSection(col, 75)
                col += 1

            item = QTableWidgetItem(str(round(operation[2], 2)))
            self.tw_many.setItem(table_row[operation[0]], table_column[operation[1]], item)

        for p_m in sql_info_p_m:
            if table_row.get(p_m[0]) is None:
                table_row[p_m[0]] = row
                item = QTableWidgetItem(str(p_m[0]))
                self.tw_many.insertRow(row)
                self.tw_many.setItem(row, 0, item)
                row += 1

            if table_column.get(p_m[1]) is None:
                table_column[p_m[1]] = col
                self.tw_many.insertColumn(col)
                self.tw_many.setHorizontalHeaderItem(col, QTableWidgetItem(p_m[1].strftime("%d.%m.%Y")))
                self.tw_many.horizontalHeader().resizeSection(col, 75)
                col += 1

            operation_item = self.tw_many.item(table_row[p_m[0]], table_column[p_m[1]])
            if operation_item is None:
                item = QTableWidgetItem(str(round(p_m[2], 2)))
                self.tw_many.setItem(table_row[p_m[0]], table_column[p_m[1]], item)
            else:
                new_salary = round(Decimal(operation_item.text()) + p_m[2], 2)
                item = QTableWidgetItem(str(new_salary))
                self.tw_many.setItem(table_row[p_m[0]], table_column[p_m[1]], item)

    def ui_many_export(self):
        path = QFileDialog.getSaveFileName(self, "Сохранение")
        if path[0]:
            to_excel.table_to_excel(self.tw_many, path[0])


class SalaryInfo(QDialog, salary_work):
    def __init__(self, work):
        super(SalaryInfo, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.work = work

        self.set_size_table()
        self.set_table()

    def set_size_table(self):
        self.tw_operation.horizontalHeader().resizeSection(0, 235)
        self.tw_operation.horizontalHeader().resizeSection(1, 45)
        self.tw_operation.horizontalHeader().resizeSection(2, 45)
        self.tw_operation.horizontalHeader().resizeSection(3, 60)
        self.tw_operation.horizontalHeader().resizeSection(4, 90)
        self.tw_operation.horizontalHeader().resizeSection(5, 120)

        self.tw_p_m.horizontalHeader().resizeSection(0, 235)
        self.tw_p_m.horizontalHeader().resizeSection(1, 55)
        self.tw_p_m.horizontalHeader().resizeSection(2, 80)
        self.tw_p_m.horizontalHeader().resizeSection(3, 160)
        self.tw_p_m.horizontalHeader().resizeSection(4, 60)

    def set_table(self):
        for row, operation in enumerate(self.work["operation_list"]):
            self.tw_operation.insertRow(row)

            new_table_item = QTableWidgetItem(str(operation[2]))
            self.tw_operation.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[5]))
            self.tw_operation.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[6]))
            self.tw_operation.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(round(operation[1], 2)))
            self.tw_operation.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[3].strftime("%d.%m.%Y")))
            self.tw_operation.setItem(row, 4, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[4].strftime("%d.%m.%Y %H:%M:%S")))
            self.tw_operation.setItem(row, 5, new_table_item)

        for row, p_m in enumerate(self.work["p_m_list"]):
            self.tw_p_m.insertRow(row)

            if p_m[2] > 0:
                color = QBrush(QColor(152, 251, 152, 255))
            else:
                color = QBrush(QColor(240, 128, 128, 255))

            new_table_item = QTableWidgetItem(str(p_m[1]))
            new_table_item.setBackground(color)
            self.tw_p_m.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(round(p_m[2], 2)))
            new_table_item.setBackground(color)
            self.tw_p_m.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(p_m[3].strftime("%d.%m.%Y")))
            new_table_item.setBackground(color)
            self.tw_p_m.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(p_m[4]))
            new_table_item.setBackground(color)
            self.tw_p_m.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(p_m[5]))
            new_table_item.setBackground(color)
            self.tw_p_m.setItem(row, 4, new_table_item)

    def ui_acc(self):
        self.close()
        self.destroy()


class SalaryHistory(QDialog, salary_history):
    def __init__(self):
        super(SalaryHistory, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.set_sql_salary_date()

    def set_sql_salary_date(self):
        query = """(SELECT Date_Pay FROM pack_operation WHERE Pay = 1 GROUP BY Date_Pay ORDER BY Date_Pay DESC)
                    UNION
                    (SELECT Date_Pay FROM pay_worker WHERE Pay = 1 GROUP BY Date_Pay ORDER BY Date_Pay DESC)
                    ORDER BY Date_Pay DESC"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог получыить даты закрытых месяцов")

        for date in sql_info:
            date_item = QListWidgetItem(date[0].strftime("%d.%m.%Y"))
            date_item.setData(-1, date[0])
            self.lw_date_salary.addItem(date_item)

    def ui_double_click(self, item):
        self.date = item.data(-1)
        self.done(1)
        self.close()
        self.destroy()