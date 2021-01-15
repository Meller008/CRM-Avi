import sys
from os import getcwd
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidgetItem, QDialog, QMainWindow, QListWidgetItem, QInputDialog
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QIcon, QBrush, QColor, QTextCharFormat
from PyQt5.QtCore import Qt, QDate, QTimer
from function import my_sql
from classes.my_class import User
import re

main_class = loadUiType(getcwd() + '/ui/operation/main.ui')[0]
operation_acc = loadUiType(getcwd() + '/ui/operation/operation_acc.ui')[0]
salary_date = loadUiType(getcwd() + '/ui/operation/salary_date.ui')[0]


class MainWindowOperation(QMainWindow, main_class):
    def __init__(self, *args):
        super(MainWindowOperation, self).__init__(*args)
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.show()

        self.showFullScreen()

        self.select_data = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.close_timer)
        self.timer.start(900000)

        self.start_var()
        self.start_settings()

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

    def start_var(self):
        self.user = {"id": None,
                     "f_name": None,
                     "l_name": None}

        self.cut = {"cut_id": None,
                    "pack_id": None,
                    "pack_number": None,
                    "pack_value": None,
                    "article_name": None,
                    "pack_size": None,
                    "pack_client": None,
                    "cut_date": None}

        self.operation_list = None

    def start_settings(self):
        self.tw_operation.horizontalHeader().resizeSection(0, 45)
        self.tw_operation.horizontalHeader().resizeSection(1, 340)
        self.tw_operation.horizontalHeader().resizeSection(2, 185)
        self.tw_operation.horizontalHeader().resizeSection(3, 230)
        self.tw_operation.horizontalHeader().resizeSection(4, 145)
        self.tw_operation.horizontalHeader().resizeSection(5, 140)

        self.tw_salary_operation.horizontalHeader().resizeSection(0, 55)
        self.tw_salary_operation.horizontalHeader().resizeSection(1, 50)
        self.tw_salary_operation.horizontalHeader().resizeSection(2, 80)
        self.tw_salary_operation.horizontalHeader().resizeSection(3, 58)
        self.tw_salary_operation.horizontalHeader().resizeSection(4, 260)
        self.tw_salary_operation.horizontalHeader().resizeSection(5, 70)
        self.tw_salary_operation.horizontalHeader().resizeSection(6, 60)
        self.tw_salary_operation.horizontalHeader().resizeSection(7, 70)
        self.tw_salary_operation.horizontalHeader().resizeSection(8, 100)
        self.tw_salary_operation.horizontalHeader().resizeSection(9, 155)

        self.tw_salary_p_m.horizontalHeader().resizeSection(0, 280)
        self.tw_salary_p_m.horizontalHeader().resizeSection(1, 65)
        self.tw_salary_p_m.horizontalHeader().resizeSection(2, 90)
        self.tw_salary_p_m.horizontalHeader().resizeSection(3, 400)

        self.tw_salary_history.horizontalHeader().resizeSection(0, 75)
        self.tw_salary_history.horizontalHeader().resizeSection(1, 280)
        self.tw_salary_history.horizontalHeader().resizeSection(2, 85)
        self.tw_salary_history.horizontalHeader().resizeSection(3, 90)
        self.tw_salary_history.horizontalHeader().resizeSection(4, 70)
        self.tw_salary_history.horizontalHeader().resizeSection(5, 60)
        self.tw_salary_history.horizontalHeader().resizeSection(6, 80)
        self.tw_salary_history.horizontalHeader().resizeSection(7, 100)
        self.tw_salary_history.horizontalHeader().resizeSection(8, 150)

        self.tw_staff_traffic.horizontalHeader().resizeSection(0, 300)
        self.tw_staff_traffic.horizontalHeader().resizeSection(1, 350)

    def ui_login(self):
        self.timer.start(900000)
        query = """SELECT staff_worker_info.Id, staff_worker_info.First_Name, staff_worker_info.Last_Name
                      FROM staff_worker_login
                        LEFT JOIN staff_worker_info ON staff_worker_login.Worker_Info_Id = staff_worker_info.Id
                      WHERE staff_worker_login.Login = %s AND BINARY staff_worker_login.Password = %s"""
        sql_info = my_sql.sql_select(query, (self.le_login.text(), self.le_pass.text()))
        if "mysql.connector.errors" in str(type(sql_info)):
            self.lb_login_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Не смог проверить логин(Err BD)</span></p></body></html>')
            return False

        if sql_info:
            # Если логин правильный
            self.user["id"] = sql_info[0][0]
            self.user["f_name"] = sql_info[0][1]
            self.user["l_name"] = sql_info[0][2]
            self.statusbar_label = QLabel(sql_info[0][2] + " " + sql_info[0][1])
            self.statusbar.addWidget(self.statusbar_label)

            # Отчищаем строки
            self.lb_login_error.setText('')
            self.le_login.setText("")
            self.le_pass.setText("")

            # Закрываем кнопку бейки
            self.pb_beika.setEnabled(False)

            # Заполняем 2 окно
            self.lb_l_name.setText("Имя: " + sql_info[0][1])
            self.lb_f_name.setText("Фамилия: " + sql_info[0][2])

            # запоминаем пользователя для доступа и настраиваем доступ
            User().set_id(sql_info[0][0])
            self.access()

            self.sw_main.setCurrentIndex(1)

        else:
            self.lb_login_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Не верный логин ил пароль</span></p></body></html>')

    def ui_log_out(self):
        self.start_var()
        self.start_settings()
        self.lb_f_name.setText("")
        self.lb_l_name.setText("")
        self.statusbar.removeWidget(self.statusbar_label)
        self.sw_main.setCurrentIndex(0)

    def ui_add_operation(self):
        self.timer.start(900000)
        self.le_cut_number.setFocus()
        self.sw_main.setCurrentIndex(2)

    def ui_cut_back(self):
        self.timer.start(900000)
        self.le_cut_number.setText("")
        self.sw_main.setCurrentIndex(1)

    def ui_cut_next(self):
        self.timer.start(900000)
        query = """SELECT COUNT(*) FROM cut WHERE Id = %s"""
        sql_info = my_sql.sql_select(query, (int(self.le_cut_number.text()), ))
        if "mysql.connector.errors" in str(type(sql_info)):
            self.lb_cut_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Не смог проверить крой (Err BD)</span></p></body></html>')
            return False

        if sql_info[0][0] == 1:
            self.cut["cut_id"] = int(self.le_cut_number.text())
            self.lb_cut_error.setText('')
            self.le_cut_number.setText("")
            self.le_pack_number.setFocus()
            self.sw_main.setCurrentIndex(3)
        else:
            self.lb_cut_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Нет кроя с таким номером</span></p></body></html>')
            self.le_cut_number.setText("")

    def ui_pack_back(self):
        self.timer.start(900000)
        self.le_pack_number.setText("")
        self.le_cut_number.setFocus()
        self.sw_main.setCurrentIndex(2)

    def ui_pack_next(self):
        self.timer.start(900000)
        query = """SELECT Id FROM pack WHERE Number = %s AND Cut_Id = %s"""
        sql_info = my_sql.sql_select(query, (int(self.le_pack_number.text()), self.cut["cut_id"]))
        if "mysql.connector.errors" in str(type(sql_info)):
            self.lb_pack_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Не смог проверить пачку (Err BD)</span></p></body></html>')
            return False

        if sql_info and sql_info[0][0] > 0:
            self.cut["pack_number"] = int(self.le_pack_number.text())
            self.cut["pack_id"] = int(sql_info[0][0])
            self.lb_pack_error.setText('')
            self.le_pack_number.setText("")
            self.set_pack_info()
            self.set_operation_table()
            self.sw_main.setCurrentIndex(4)
        else:
            self.lb_pack_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Нет пачки с таким номером</span></p></body></html>')
            self.le_pack_number.setText("")

    def ui_operation_back(self):
        self.timer.start(900000)
        self.le_operation_cut.setText("")
        self.le_operation_pack.setText("")
        self.le_operation_pack_value.setText("")
        self.le_operation_article.setText("")
        self.le_operation_size.setText("")
        self.le_operation_client.setText("")
        self.le_operation_cut_date.setText("")

        self.lb_pack_error.setText('')

        self.tw_operation.clearContents()
        self.tw_operation.setRowCount(0)

        self.le_pack_number.setFocus()
        self.sw_main.setCurrentIndex(3)

    def ui_operation_double_click(self, item):
        try:
            id = int(item.data(-2))
            open_operation = int(item.data(-1))
        except:
            return False

        if not open_operation:
            self.lb_operation_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Операция занята</span></p></body></html>')
            return False

        self.lb_operation_error.setText('')

        self.operation_acc = OperationAcc(self, self.cut, self.operation_list[self.tw_operation.currentRow()])
        self.operation_acc.setModal(True)
        self.operation_acc.show()

    def ui_operation_next(self):
        self.timer.start(900000)
        try:
            id = int(self.tw_operation.item(self.tw_operation.currentRow(), 0).data(-2))
            open_operation = int(self.tw_operation.item(self.tw_operation.currentRow(), 0).data(-1))
        except:
            self.lb_operation_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Выберите операцию</span></p></body></html>')
            return False

        if not open_operation:
            self.lb_operation_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Операция занята</span></p></body></html>')
            return False

        self.lb_operation_error.setText('')

        self.operation_acc = OperationAcc(self, self.cut, self.operation_list[self.tw_operation.currentRow()])
        self.operation_acc.setModal(True)
        self.operation_acc.show()

    def ui_operation_input_complete(self):
        self.le_operation_cut.setText("")
        self.le_operation_pack.setText("")
        self.le_operation_pack_value.setText("")
        self.le_operation_article.setText("")
        self.le_operation_size.setText("")
        self.le_operation_client.setText("")
        self.le_operation_cut_date.setText("")

        self.lb_pack_error.setText('')

        self.cut = {"cut_id": None,
                    "pack_id": None,
                    "pack_number": None,
                    "pack_value": None,
                    "article_name": None,
                    "pack_size": None,
                    "pack_client": None,
                    "cut_date": None}

        self.operation_list = None

        self.tw_operation.clearContents()
        self.tw_operation.setRowCount(0)

        self.sw_main.setCurrentIndex(1)

    def ui_salary_menu(self):
        self.timer.start(900000)
        self.sw_main.setCurrentIndex(5)

    def ui_salary_operation(self):
        self.timer.start(900000)
        query = """SELECT cut.Id, pack.Number, product_article.Article, product_article_size.Size, pack_operation.Name, pack_operation.Price,
                        pack.Value_Pieces - pack.Value_Damage, pack_operation.Price * (pack.Value_Pieces - pack.Value_Damage ),
                        pack_operation.Date_make, pack_operation.Date_Input,
                          CASE
                            WHEN pack.Date_Make IS NOT NULL AND pack.Date_Coplete IS NOT NULL THEN 1
                            ELSE 0
                          END
                      FROM pack_operation LEFT JOIN pack ON pack_operation.Pack_Id = pack.Id
                        LEFT JOIN cut ON pack.Cut_Id = cut.Id
                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE pack_operation.Worker_Id = %s AND pack_operation.Pay = 0"""
        sql_info = my_sql.sql_select(query, (self.user["id"], ))
        if "mysql.connector.errors" in str(type(sql_info)):
            return False

        self.tw_salary_operation.clearContents()
        self.tw_salary_operation.setRowCount(0)

        operation_all = 0
        operation_ok = 0
        operation_waiting = 0

        for row, operation in enumerate(sql_info):

            if operation[10] == 0:
                color = QBrush(QColor(246, 250, 127, 255))
                operation_waiting += operation[7]
            else:
                color = QBrush(QColor(120, 240, 138, 255))
                operation_ok += operation[7]

            self.tw_salary_operation.insertRow(row)

            new_table_item = QTableWidgetItem(str(operation[0]))
            new_table_item.setBackground(color)
            self.tw_salary_operation.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[1]))
            new_table_item.setBackground(color)
            self.tw_salary_operation.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[2]))
            new_table_item.setBackground(color)
            self.tw_salary_operation.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[3]))
            new_table_item.setBackground(color)
            self.tw_salary_operation.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[4]))
            new_table_item.setBackground(color)
            self.tw_salary_operation.setItem(row, 4, new_table_item)

            new_table_item = QTableWidgetItem(str(round(operation[5], 2)))
            new_table_item.setBackground(color)
            self.tw_salary_operation.setItem(row, 5, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[6]))
            new_table_item.setBackground(color)
            self.tw_salary_operation.setItem(row, 6, new_table_item)

            new_table_item = QTableWidgetItem(str(round(operation[7], 2)))
            new_table_item.setBackground(color)
            self.tw_salary_operation.setItem(row, 7, new_table_item)

            new_table_item = QTableWidgetItem(operation[8].strftime("%d.%m.%Y"))
            new_table_item.setBackground(color)
            self.tw_salary_operation.setItem(row, 8, new_table_item)

            new_table_item = QTableWidgetItem(operation[9].strftime("%d.%m.%Y %H:%M:%S"))
            new_table_item.setBackground(color)
            self.tw_salary_operation.setItem(row, 9, new_table_item)

        operation_all = operation_waiting + operation_ok

        self.le_salary_operation_all.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(operation_all, 2))))
        self.le_salary_operation_waiting.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(operation_waiting, 2))))
        self.le_salary_operation_ok.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(operation_ok, 2))))

        self.sw_main.setCurrentIndex(6)

    def ui_salary_p_m(self):
        self.timer.start(900000)
        query = """SELECT pay_reason.Name, pay_worker.Balance, pay_worker.Date_In_Pay, pay_worker.Note
                      FROM pay_worker LEFT JOIN pay_reason ON pay_worker.Reason_Id = pay_reason.Id
                      WHERE pay_worker.Worker_Id = %s AND pay_worker.Pay = 0"""
        sql_info = my_sql.sql_select(query, (self.user["id"],))
        if "mysql.connector.errors" in str(type(sql_info)):
            return False

        self.tw_salary_p_m.clearContents()
        self.tw_salary_p_m.setRowCount(0)

        p_m_plus = 0
        p_m_minus = 0
        p_m_all = 0

        for row, p_m in enumerate(sql_info):

            if p_m[1] >= 0:
                color = QBrush(QColor(246, 250, 127, 255))
                p_m_plus += p_m[1]
            else:
                color = QBrush(QColor(245, 113, 113, 255))
                p_m_minus += -p_m[1]

            self.tw_salary_p_m.insertRow(row)

            new_table_item = QTableWidgetItem(str(p_m[0]))
            new_table_item.setBackground(color)
            self.tw_salary_p_m.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(round(p_m[1], 2)))
            new_table_item.setBackground(color)
            self.tw_salary_p_m.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(p_m[2].strftime("%d.%m.%Y")))
            new_table_item.setBackground(color)
            self.tw_salary_p_m.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(p_m[3]))
            new_table_item.setBackground(color)
            self.tw_salary_p_m.setItem(row, 3, new_table_item)

        p_m_all = p_m_plus - p_m_minus
        self.tw_salary_p_m_all.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(p_m_all, 2))))
        self.tw_salary_p_m_minus.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(p_m_minus, 2))))
        self.tw_salary_p_m_plus.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(p_m_plus, 2))))

        self.sw_main.setCurrentIndex(7)

    def ui_salary_history(self):
        self.timer.start(900000)
        self.date = SalaryDate(self, self.user["id"])
        self.date.setModal(True)
        self.date.show()

    def ui_salary_menu_back(self):
        self.timer.start(900000)
        self.sw_main.setCurrentIndex(1)

    def ui_back_to_salary_menu(self):
        self.timer.start(900000)
        self.tw_salary_operation.clearContents()
        self.tw_salary_operation.setRowCount(0)

        self.tw_salary_p_m.clearContents()
        self.tw_salary_p_m.setRowCount(0)

        self.tw_salary_history.clearContents()
        self.tw_salary_history.setRowCount(0)

        self.sw_main.setCurrentIndex(5)

    def set_pack_info(self):
        query = """SELECT pack.Value_Pieces, product_article.Article, pack.Size, clients.Name, DATE_FORMAT(cut.Date_Cut, '%d.%m.%Y')
                      FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                        LEFT JOIN clients ON pack.Client_Id = clients.Id
                      WHERE pack.Id = %s"""
        sql_info = my_sql.sql_select(query, (self.cut["pack_id"], ))
        if "mysql.connector.errors" in str(type(sql_info)):
            self.lb_pack_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Не смог получить пачку (Err BD)</span></p></body></html>')
            return False

        if sql_info:
            self.cut["pack_value"] = sql_info[0][0]
            self.cut["article_name"] = sql_info[0][1]
            self.cut["pack_size"] = sql_info[0][2]
            self.cut["pack_client"] = sql_info[0][3]
            self.cut["cut_date"] = sql_info[0][4]

        else:
            self.lb_pack_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Пустой ответ пачки (Err BD)</span></p></body></html>')

        self.le_operation_cut.setText(str(self.cut["cut_id"]))
        self.le_operation_pack.setText(str(self.cut["pack_number"]))
        self.le_operation_pack_value.setText(str(self.cut["pack_value"]))
        self.le_operation_article.setText(str(self.cut["article_name"]))
        self.le_operation_size.setText(str(self.cut["pack_size"]))
        self.le_operation_client.setText(str(self.cut["pack_client"]))
        self.le_operation_cut_date.setText(str(self.cut["cut_date"]))

    def set_operation_table(self):
        query = """SELECT pack_operation.Id, pack_operation.Position, pack_operation.Name, sewing_machine.Name, staff_worker_info.Last_Name, staff_worker_info.First_Name,
                        DATE_FORMAT(pack_operation.Date_make, '%d.%m.%Y'), pack_operation.Price, staff_worker_info.Id
                      FROM pack LEFT JOIN pack_operation ON pack.Id = pack_operation.Pack_Id
                        LEFT JOIN operations ON pack_operation.Operation_id = operations.Id
                        LEFT JOIN sewing_machine ON operations.Sewing_Machine_Id = sewing_machine.Id
                        LEFT JOIN staff_worker_info ON pack_operation.Worker_Id = staff_worker_info.Id
                      WHERE pack.Id = %s
                      ORDER BY -pack_operation.Position DESC """
        sql_info = my_sql.sql_select(query, (self.cut["pack_id"], ))
        if "mysql.connector.errors" in str(type(sql_info)):
            self.lb_pack_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Не смог получить операции(Err BD)</span></p></body></html>')
            return False

        if sql_info:
            self.operation_list = sql_info
        else:
            self.lb_pack_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Пустой ответ операций (Err BD)</span></p></body></html>')

        self.tw_operation.clearContents()
        self.tw_operation.setRowCount(0)
        for row, operation in enumerate(self.operation_list):

            if operation[6] is None:
                color = QBrush(QColor(120, 240, 138, 255))
                open_operation = True
            elif operation[8] == self.user["id"]:
                color = QBrush(QColor(0, 221, 237, 255))
                open_operation = False
            else:
                color = QBrush(QColor(240, 120, 172, 255))
                open_operation = False

            self.tw_operation.insertRow(row)

            new_table_item = QTableWidgetItem(str(operation[1]))
            new_table_item.setData(-1, open_operation)
            new_table_item.setData(-2, operation[0])
            if color is not None:
                new_table_item.setBackground(color)
            self.tw_operation.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[2]))
            new_table_item.setData(-1, open_operation)
            new_table_item.setData(-2, operation[0])
            if color is not None:
                new_table_item.setBackground(color)
            self.tw_operation.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[3]))
            new_table_item.setData(-1, open_operation)
            new_table_item.setData(-2, operation[0])
            if color is not None:
                new_table_item.setBackground(color)
            self.tw_operation.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[4]) + " " + str(operation[5]))
            new_table_item.setData(-1, open_operation)
            new_table_item.setData(-2, operation[0])
            if color is not None:
                new_table_item.setBackground(color)
            self.tw_operation.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[6]))
            new_table_item.setData(-1, open_operation)
            new_table_item.setData(-2, operation[0])
            if color is not None:
                new_table_item.setBackground(color)
            self.tw_operation.setItem(row, 4, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[7]))
            new_table_item.setData(-1, open_operation)
            new_table_item.setData(-2, operation[0])
            if color is not None:
                new_table_item.setBackground(color)
            self.tw_operation.setItem(row, 5, new_table_item)

    def of_operation_input_complete(self, operation, date_make):
        query = """UPDATE pack_operation
                      SET Worker_Id = %s, Date_make = %s, Date_Input = SYSDATE()
                      WHERE Id = %s"""
        sql_value = (self.user["id"], date_make.toString(Qt.ISODate), operation[0])
        sql_info = my_sql.sql_change(query, sql_value)
        if "mysql.connector.errors" in str(type(sql_info)):
            self.lb_operation_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Операция не сохранена(Err BD)</span></p></body></html>')
            return False

        self.set_operation_table()
        self.lb_operation_error.setText('<html><head/><body><p align="center"><span style=" color:#00aa00;">Операция сохранена</span></p></body></html>')

    def of_salary_history_date(self, date):
        query = """SELECT 'Операция', pack_operation.Name, CONCAT(cut.Id, '/', pack.Number), CONCAT(product_article.Article, ' (', product_article_size.Size, ')'),
                        pack_operation.Price, pack.Value_Pieces - pack.Value_Damage, pack_operation.Price * (pack.Value_Pieces - pack.Value_Damage ),
                        pack_operation.Date_make, pack_operation.Date_Input
                      FROM pack_operation LEFT JOIN pack ON pack_operation.Pack_Id = pack.Id
                        LEFT JOIN cut ON pack.Cut_Id = cut.Id
                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE pack_operation.Worker_Id = %s AND pack_operation.Date_Pay = %s AND pack_operation.Pay = 1"""
        sql_info_1 = my_sql.sql_select(query, (self.user["id"], date))
        if "mysql.connector.errors" in str(type(sql_info_1)):
            return False

        query = """SELECT IF(pay_worker.Balance >= 0, 'Доплата', 'Вычет'), pay_reason.Name, '', '', pay_worker.Balance, '1', pay_worker.Balance, pay_worker.Date_In_Pay, ''
                      FROM pay_worker LEFT JOIN pay_reason ON pay_worker.Reason_Id = pay_reason.Id
                      WHERE pay_worker.Worker_Id = %s AND pay_worker.Date_Pay = %s AND pay_worker.Pay = 1"""
        sql_info_2 = my_sql.sql_select(query, (self.user["id"], date))
        if "mysql.connector.errors" in str(type(sql_info_2)):
            return False

        position_salary = sql_info_1 + sql_info_2

        self.tw_salary_history.clearContents()
        self.tw_salary_history.setRowCount(0)

        all_operation = 0
        all_p_m = 0

        for row, operation in enumerate(position_salary):
            self.tw_salary_history.insertRow(row)

            if operation[0] == "Операция":
                all_operation += operation[6]
            else:
                all_p_m += operation[6]

            new_table_item = QTableWidgetItem(str(operation[0]))
            self.tw_salary_history.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[1]))
            self.tw_salary_history.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[2]))
            self.tw_salary_history.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[3]))
            self.tw_salary_history.setItem(row, 3, new_table_item)

            new_table_item = QTableWidgetItem(str(round(operation[4], 2)))
            self.tw_salary_history.setItem(row, 4, new_table_item)

            new_table_item = QTableWidgetItem(str(operation[5]))
            self.tw_salary_history.setItem(row, 5, new_table_item)

            new_table_item = QTableWidgetItem(str(round(operation[6], 2)))
            self.tw_salary_history.setItem(row, 6, new_table_item)

            new_table_item = QTableWidgetItem(operation[7].strftime("%d.%m.%Y"))
            self.tw_salary_history.setItem(row, 7, new_table_item)

            if operation[8]:
                new_table_item = QTableWidgetItem(operation[8].strftime("%d.%m.%Y %H:%M:%S"))
                self.tw_salary_history.setItem(row, 8, new_table_item)

        all = all_operation + all_p_m
        self.tw_salary_history_p_m.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_p_m, 2))))
        self.tw_salary_history_operation.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_operation, 2))))
        self.tw_salary_history_all.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all, 2))))

        self.sw_main.setCurrentIndex(8)

    def ui_beika(self):
        self.timer.start(900000)
        query = "SELECT Id, Name FROM accessories_name WHERE For_Beika = 1"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            return False

        if len(sql_info) == 1:
            self.beika_accessories_id = sql_info[0][0]
        else:
            return False

        query = """SELECT Id, Name FROM material_name WHERE For_Beika = 1 ORDER BY Name"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            return False

        for material in sql_info:
            item = QListWidgetItem(material[1])
            item.setData(-1, (material[0]))
            item.setTextAlignment(Qt.AlignHCenter)
            self.lw_material.addItem(item)

        self.lw_material.setSpacing(5)

        self.sw_main.setCurrentIndex(9)

    def ui_beika_change_value(self, text):
        if text:
            if text[-1].isdigit() or text[-1] == "." or text[-1] == ",":
                try:
                    check_val = float(text.replace(",", "."))
                    if check_val > 30:
                        self.le_value.setText(text[:-1])
                    else:
                        self.le_value.setText(text.replace(",", "."))
                except ValueError:
                    self.le_value.setText(text[:-1])
            else:
                self.le_value.setText(text[:-1])

            # if text[-1].isdigit():
            #     return True
            # elif text[-1] == ".":
            #     return True
            # elif text[-1] == ",":
            #     self.le_value.setText(text.replace(",", "."))
            # else:
            #     self.le_value.setText(text[:-1])

    def ui_beika_acc(self):
        self.timer.start(900000)
        if self.le_value.text() == "":
            return False
        elif self.lw_material.currentRow() < 0:
            return False

        try:
            value = self.le_value.text().replace(",", ".")
        except:
            self.le_value.setStyleSheet("border: 4px solid;\nborder-color: rgb(247, 84, 84);")
            return False

        query = """INSERT INTO beika (Material_Id, Accessories_Id, Date, Value, Finished, Worker_Id, Supply_Id)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        sql_value = (self.lw_material.selectedItems()[0].data(-1), self.beika_accessories_id, self.cw_date.selectedDate().toString(Qt.ISODate),
                     value, 0, self.user["id"], None)
        sql_info = my_sql.sql_change(query, sql_value)
        if "mysql.connector.errors" in str(type(sql_info)):
            self.le_error.setText("Не получилось сохранить нарезку. Обратитесь к администрации.")
            self.pushButton_21.setEnabled(False)
            return False

        self.lw_material.clear()
        self.le_value.clear()

        self.sw_main.setCurrentIndex(1)

    def ui_beika_back(self):
        self.timer.start(900000)
        self.lw_material.clear()
        self.le_value.clear()

        self.sw_main.setCurrentIndex(1)

    def ui_go_traffic(self):
        self.timer.start(900000)
        self.sw_main.setCurrentIndex(10)
        self.set_work_traffic()

    def ui_select_date_work_traffic(self):
        self.set_work_traffic()

    def set_work_traffic(self):
        id = self.user["id"]

        if self.select_data is None or self.last_id != id \
                or self.cw_traffic.selectedDate().month() != self.select_data.month() or self.cw_traffic.selectedDate().year() != self.select_data.year():
            data = self.cw_traffic.selectedDate()
            query = """SELECT staff_worker_traffic.Id, staff_worker_traffic.Position, staff_worker_traffic.Data, staff_worker_traffic.Table_Data, staff_worker_traffic.Note
                          FROM staff_worker_traffic LEFT JOIN staff_worker_info ON staff_worker_traffic.Worker_Id = staff_worker_info.Id
                          WHERE staff_worker_traffic.Worker_Id = %s AND staff_worker_traffic.Data >= %s AND staff_worker_traffic.Data <= %s
                          ORDER BY staff_worker_traffic.Data"""
            sql_param = (id, data.toString("yyyy-MM-01-00-00-00"), data.toString("yyyy-MM-%s-23-59-59" % data.daysInMonth()))
            self.sql_traffic = my_sql.sql_select(query, sql_param)
            if "mysql.connector.errors" in str(type(self.sql_traffic)):
                return False

            # Очистим цветные метки
            if self.select_data:
                color = (255, 255, 255)
                color = QColor(color[0], color[1], color[2], 255)
                brush = QBrush()
                brush.setColor(color)
                fomat = QTextCharFormat()
                fomat.setBackground(brush)
                for day in range(1, self.select_data.daysInMonth() + 1):
                    d = QDate(self.select_data.year(), self.select_data.month(), day)
                    self.cw_traffic.setDateTextFormat(d, fomat)

            # Выставим цветные метки
            color_green = QColor(79, 255, 185, 200)
            color_yellow = QColor(230, 245, 95, 200)
            color_red = QColor(245, 110, 95, 200)

            for data in self.sql_traffic:
                if self.cw_traffic.dateTextFormat(data[2]).background().color() == color_yellow:
                    brush = QBrush()
                    brush.setColor(color_green)
                    fomat = QTextCharFormat()
                    fomat.setBackground(brush)
                elif self.cw_traffic.dateTextFormat(data[2]).background().color() == color_green:
                    brush = QBrush()
                    brush.setColor(color_red)
                    fomat = QTextCharFormat()
                    fomat.setBackground(brush)
                else:
                    brush = QBrush()
                    brush.setColor(color_yellow)
                    fomat = QTextCharFormat()
                    fomat.setBackground(brush)

                self.cw_traffic.setDateTextFormat(data[2], fomat)

        if self.cw_traffic.selectedDate() != self.select_data or self.last_id != id:

            self.last_id = id
            self.select_data = self.cw_traffic.selectedDate()
            self.tw_staff_traffic.clearContents()
            self.tw_staff_traffic.setRowCount(0)
            for data in self.sql_traffic:
                if data[2].strftime("%d.%m.%Y") == self.select_data.toString("dd.MM.yyyy"):
                    self.tw_staff_traffic.insertRow(self.tw_staff_traffic.rowCount())

                    new_table_item = QTableWidgetItem(data[2].strftime("%d.%m.%Y %H:%M"))
                    new_table_item.setData(-2, data[0])
                    self.tw_staff_traffic.setItem(self.tw_staff_traffic.rowCount()-1, 0, new_table_item)

                    new_table_item = QTableWidgetItem(data[4])
                    new_table_item.setData(-2, data[0])
                    self.tw_staff_traffic.setItem(self.tw_staff_traffic.rowCount()-1, 1, new_table_item)

    def ui_work_traffic_back(self):
        self.timer.start(900000)
        self.tw_staff_traffic.clearContents()
        self.tw_staff_traffic.setRowCount(0)

        self.sw_main.setCurrentIndex(1)

    def keyPressEvent(self, event):
        if event.key() == 16777221 or event.key() == 16777220:
            if self.sw_main.currentIndex() == 0:
                self.ui_login()
            elif self.sw_main.currentIndex() == 1:
                self.ui_add_operation()
            elif self.sw_main.currentIndex() == 2:
                self.ui_cut_next()
            elif self.sw_main.currentIndex() == 3:
                self.ui_pack_next()
            elif self.sw_main.currentIndex() == 4:
                self.ui_operation_next()
            elif self.sw_main.currentIndex() == 9:
                self.ui_beika_acc()

        event.accept()

    def close_timer(self):
        self.timer.stop()
        self.ui_log_out()

    def ui_services(self):
        res = QInputDialog.getText(self, "Код", "Введите сервис код")
        if res[1]:
            if res[0] == "088011":
                self.close()
                self.destroy()


class OperationAcc(QDialog, operation_acc):
    def __init__(self, main, cut, operation):
        super(OperationAcc, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.cw_date_make.setSelectedDate(QDate.currentDate())

        self.main = main
        self.select_cut = cut
        self.select_operation = operation

    def ui_date_acc(self):
        self.lb_cut.setText("Крой: " + str(self.select_cut["cut_id"]))
        self.lb_pack.setText("Пачка: " + str(self.select_cut["pack_number"]))
        self.lb_operation.setText("Операция: " + str(self.select_operation[1]) + " - " + str(self.select_operation[2]))
        self.ld_date_make.setText("Дата пошива: " + str(self.cw_date_make.selectedDate().toString("dd.MM.yyyy")))
        self.sw_main.setCurrentIndex(1)

    def ui_acc(self):
        self.main.of_operation_input_complete(self.select_operation, self.cw_date_make.selectedDate())
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()

    def keyPressEvent(self, event):
        if event.key() == 16777221 or event.key() == 16777220:
            if self.sw_main.currentIndex() == 0:
                self.ui_date_acc()
            elif self.sw_main.currentIndex() == 1:
                self.ui_acc()

        event.accept()


class SalaryDate(QDialog, salary_date):
    def __init__(self, main, work_id):
        super(SalaryDate, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main
        self.work = work_id

        self.set_sql_salary_date()

    def set_sql_salary_date(self):
        query = """(SELECT Date_Pay FROM pack_operation WHERE Pay = 1 AND Worker_Id = %s GROUP BY Date_Pay ORDER BY Date_Pay DESC)
                    UNION
                    (SELECT Date_Pay FROM pay_worker WHERE Pay = 1 AND Worker_Id = %s GROUP BY Date_Pay ORDER BY Date_Pay DESC)
                    ORDER BY Date_Pay DESC LIMIT 6"""
        sql_info = my_sql.sql_select(query, (self.work, self.work))
        if "mysql.connector.errors" in str(type(sql_info)):
            return False

        for date in sql_info:
            date_item = QListWidgetItem(date[0].strftime("%d.%m.%Y"))
            date_item.setData(-1, date[0])
            date_item.setTextAlignment(Qt.AlignHCenter)
            self.lw_date_salary.addItem(date_item)

    def ui_acc(self, item):
        try:
            date = self.lw_date_salary.selectedItems()[0].data(-1)
        except:
            return False

        self.main.of_salary_history_date(date)
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()


app = QApplication(sys.argv)
main = MainWindowOperation()
sys.exit(app.exec_())

