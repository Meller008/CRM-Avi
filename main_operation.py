import sys
from os import getcwd
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidgetItem, QDialog, QMainWindow
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt, QDate
from function import my_sql

main_class = loadUiType(getcwd() + '/ui/operation/main.ui')[0]
operation_acc = loadUiType(getcwd() + '/ui/operation/operation_acc.ui')[0]


class MainWindowOperation(QMainWindow, main_class):
    def __init__(self, *args):
        super(MainWindowOperation, self).__init__(*args)
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.show()

        self.start_var()
        self.start_settings()

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

    def ui_login(self):
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

            # Заполняем 2 окно
            self.lb_l_name.setText("Имя: " + sql_info[0][1])
            self.lb_f_name.setText("Фамилия: " + sql_info[0][2])
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
        self.sw_main.setCurrentIndex(2)

    def ui_cut_back(self):
        self.le_cut_number.setText("")
        self.sw_main.setCurrentIndex(1)

    def ui_cut_next(self):
        query = """SELECT COUNT(*) FROM cut WHERE Id = %s"""
        sql_info = my_sql.sql_select(query, (int(self.le_cut_number.text()), ))
        if "mysql.connector.errors" in str(type(sql_info)):
            self.lb_cut_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Не смог проверить крой (Err BD)</span></p></body></html>')
            return False

        if sql_info[0][0] == 1:
            self.cut["cut_id"] = int(self.le_cut_number.text())
            self.lb_cut_error.setText('')
            self.le_cut_number.setText("")
            self.sw_main.setCurrentIndex(3)
        else:
            self.lb_cut_error.setText('<html><head/><body><p align="center"><span style=" color:#ff0000;">Нет кроя с таким номером</span></p></body></html>')
            self.le_cut_number.setText("")

    def ui_pack_back(self):
        self.le_pack_number.setText("")
        self.sw_main.setCurrentIndex(2)

    def ui_pack_next(self):
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

        self.sw_main.setCurrentIndex(3)

    def ui_operation_next(self):
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
                      ORDER BY pack_operation.Position"""
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


try:
    app = QApplication(sys.argv)
    main = MainWindowOperation()
    sys.exit(app.exec_())
except:
    print(123)
