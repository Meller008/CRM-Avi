from os import getcwd
from form import staff, supply_material
from datetime import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QListWidgetItem
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt, QDate
import re
import datetime
from decimal import Decimal
from function import my_sql
from form.templates import table, list
from classes.my_class import User


class PayList(table.TableList):
    def set_settings(self):

        self.setWindowTitle("Доплаты и вычеты")  # Имя окна
        self.resize(940, 270)
        self.pb_copy.deleteLater()
        self.pb_other.deleteLater()
        self.toolBar.setStyleSheet("background-color: rgb(191, 255, 42);")  # Цвет бара

        # Названия колонк (Имя, Длинна)
        self.table_header_name = (("№", 40), ("Кому", 100), ("Сумма", 75), ("Д. исполнения", 100), ("Причина", 200), ("Замтка", 180),
                                  ("Кто назначил", 100), ("Добавлено", 70), ("В ЗП", 35))

        self.filter = None
        self.query_table_all = """SELECT pay_worker.Id, pay_worker.Id, work.Last_Name, pay_worker.Balance, pay_worker.Date_In_Pay, pay_reason.Name,
                                                pay_worker.Note, admin.Last_Name, pay_worker.Date_Input,
                                                CASE
                                                  WHEN pay_worker.Pay = 0
                                                    THEN 'Нет'
                                                  WHEN pay_worker.Pay = 1
                                                    THEN 'Да'
                                                END
                                              FROM pay_worker
                                                LEFT JOIN staff_worker_info AS work ON pay_worker.Worker_Id = work.Id
                                                LEFT JOIN staff_worker_info AS admin ON pay_worker.Worker_Id_Insert = admin.Id
                                                LEFT JOIN pay_reason ON pay_worker.Reason_Id = pay_reason.Id
                                              ORDER BY pay_worker.Date_Input DESC , pay_worker.Date_In_Pay DESC """

        #  нулевой элемент должен быть ID
        self.query_table_select = """SELECT pay_worker.Id, pay_worker.Id, work.Last_Name, pay_worker.Balance, pay_worker.Date_In_Pay, pay_reason.Name,
                                        pay_worker.Note, admin.Last_Name, pay_worker.Date_Input,
                                        CASE
                                          WHEN pay_worker.Pay = 0
                                            THEN 'Нет'
                                          WHEN pay_worker.Pay = 1
                                            THEN 'Да'
                                        END
                                      FROM pay_worker
                                        LEFT JOIN staff_worker_info AS work ON pay_worker.Worker_Id = work.Id
                                        LEFT JOIN staff_worker_info AS admin ON pay_worker.Worker_Id_Insert = admin.Id
                                        LEFT JOIN pay_reason ON pay_worker.Reason_Id = pay_reason.Id
                                      ORDER BY pay_worker.Date_Input DESC , pay_worker.Date_In_Pay DESC """

        self.query_table_dell = "DELETE FROM pay_worker WHERE Id = %s AND Pay = 0"

    def set_table_info(self):
        self.table_items = my_sql.sql_select(self.query_table_select)
        if "mysql.connector.errors" in str(type(self.table_items)):
                QMessageBox.critical(self, "Ошибка sql получение таблицы", self.table_items.msg, QMessageBox.Ok)
                return False

        if not self.table_items:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            return False

        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        for table_typle in self.table_items:
            self.table_widget.insertRow(self.table_widget.rowCount())

            if table_typle[3] > 0:
                color = QBrush(QColor(150, 255, 161, 255))
            else:
                color = QBrush(QColor(252, 141, 141, 255))

            for column in range(1, len(table_typle)):
                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(table_typle[column]))
                elif isinstance(table_typle[column], datetime.date):
                    text = table_typle[column].strftime("%d.%m.%Y")
                else:
                    text = str(table_typle[column])

                item = QTableWidgetItem(text)
                item.setData(5, table_typle[0])
                item.setBackground(color)
                self.table_widget.setItem(self.table_widget.rowCount() - 1, column - 1, item)

    def ui_add_table_item(self):  # Добавить предмет
        self.new_pay = PayBrows(self)
        self.new_pay.setWindowModality(Qt.ApplicationModal)
        self.new_pay.show()

    def ui_change_table_item(self, id=False):  # изменить элемент
        if not self.pb_change.isEnabled():
            return False

        if id:
            item_id = id
        else:
            try:
                item_id = self.table_widget.selectedItems()[0].data(5)
            except:
                QMessageBox.critical(self, "Ошибка ", "Выделите операцию который хотите изменить", QMessageBox.Ok)
                return False

        self.new_pay = PayBrows(self, item_id)
        self.new_pay.setWindowModality(Qt.ApplicationModal)
        self.new_pay.show()

    def ui_filter(self):
        if self.filter is None:
            self.filter = PayFilter(self)
        self.filter.of_set_sql_query(self.query_table_all)
        self.filter.setWindowModality(Qt.ApplicationModal)
        self.filter.show()

    def of_set_filter(self, sql):
        self.query_table_select = sql

        self.ui_update()


class PayBrows(QDialog):
    def __init__(self, main=None, id=None):
        super(PayBrows, self).__init__()
        loadUi(getcwd() + '/ui/pay_plus_minus.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.menu_text = None
        self.main = main
        self.id = id

        self.button = None

        self.start_settings()
        self.set_size_table()
        self.access()

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
                    try:
                        val = int(item["value"])
                    except:
                        val = item["value"]
                a(val)
            else:
                a()

    def access_set_menu(self, text):
        self.menu_text = text

    def start_settings(self):
        if self.id is None:
            self.de_plus_date.setDate(QDate.currentDate())
            self.de_minus_date.setDate(QDate.currentDate())
            self.de_road_date.setDate(QDate.currentDate())
            self.de_p_m_date.setDate(QDate.currentDate())
            self.de_bye_date.setDate(QDate.currentDate())
        else:
            query = """SELECT work.Id, work.First_Name, work.Last_Name, pay_worker.Balance, pay_worker.Date_In_Pay, pay_reason.Id, pay_reason.Name, pay_worker.Note
                          FROM pay_worker
                            LEFT JOIN staff_worker_info AS work ON pay_worker.Worker_Id = work.Id
                            LEFT JOIN pay_reason ON pay_worker.Reason_Id = pay_reason.Id
                          WHERE pay_worker.Id = %s"""
            sql_info = my_sql.sql_select(query, (self.id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql получение операции", sql_info.msg, QMessageBox.Ok)
                    return False

            if sql_info[0][3] > 0:
                self.menu_text = "Доплата"
                self.sw_main.setCurrentIndex(1)

                self.le_work_plus.setWhatsThis(str(sql_info[0][0]))
                self.le_work_plus.setText(str(sql_info[0][1]) + " " + str(sql_info[0][2]))

                self.le_value_plus.setText(str(sql_info[0][3]))
                self.de_plus_date.setDate(sql_info[0][4])

                self.le_reason_plus.setWhatsThis(str(sql_info[0][5]))
                self.le_reason_plus.setText(str(sql_info[0][6]))

                self.le_note_plus.setText(str(sql_info[0][7]))

            else:
                self.menu_text = "Вычет"
                self.sw_main.setCurrentIndex(2)

                self.le_work_minus.setWhatsThis(str(sql_info[0][0]))
                self.le_work_minus.setText(str(sql_info[0][1]) + " " + str(sql_info[0][2]))

                self.le_value_minus.setText(str(-sql_info[0][3]))
                self.de_minus_date.setDate(sql_info[0][4])

                self.le_reason_minus.setWhatsThis(str(sql_info[0][5]))
                self.le_reason_minus.setText(str(sql_info[0][6]))

                self.le_note_minus.setText(str(sql_info[0][7]))

            self.lw_menu.setEnabled(False)

    def set_size_table(self):
        self.tw_road.horizontalHeader().resizeSection(0, 140)
        self.tw_road.horizontalHeader().resizeSection(1, 65)
        self.tw_road.horizontalHeader().resizeSection(2, 40)
        self.tw_road.horizontalHeader().resizeSection(3, 65)

    def ui_menu_select(self, item):
        self.menu_text = item.text()

        if self.menu_text == "Доплата":
            self.sw_main.setCurrentIndex(1)
        elif self.menu_text == "Вычет":
            self.sw_main.setCurrentIndex(2)
        elif self.menu_text == "Доплата за проезд":
            self.set_table_road()
            self.sw_main.setCurrentIndex(3)
        elif self.menu_text == "Обмен":
            self.sw_main.setCurrentIndex(4)
        elif self.menu_text == "Продажа материала":
            self.sw_main.setCurrentIndex(5)

    def ui_add_worker(self):
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_add_reason_plus(self):
        self.reason_list = PayReasonPlus(self, True)
        self.reason_list.setWindowModality(Qt.ApplicationModal)
        self.reason_list.show()

    def ui_add_reason_minus(self):
        self.reason_list = PayReasonMinus(self, True)
        self.reason_list.setWindowModality(Qt.ApplicationModal)
        self.reason_list.show()

    # Для дороги
    def ui_edit_date_road(self):
        self.set_table_road()

    def ui_add_reason_road(self):
        self.button = "Дорога - Плюс"
        self.reason_list = PayReasonPlus(self, True)
        self.reason_list.setWindowModality(Qt.ApplicationModal)
        self.reason_list.show()

    # Для обмена
    def ui_add_worker_m_p_minus(self):
        self.button = "Плюс минус - Минус"
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_add_worker_m_p_plus(self):
        self.button = "Плюс минус - Плюс"
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_add_reason_m_p_minus(self):
        self.button = "Плюс минус - Минус"
        self.reason_list = PayReasonMinus(self, True)
        self.reason_list.setWindowModality(Qt.ApplicationModal)
        self.reason_list.show()

    def ui_add_reason_m_p_plus(self):
        self.button = "Плюс минус - Плюс"
        self.reason_list = PayReasonPlus(self, True)
        self.reason_list.setWindowModality(Qt.ApplicationModal)
        self.reason_list.show()

    def ui_copy_to_note_1(self):
        self.le_p_m_note_minus.setText(self.le_p_m_note_plus.text())

    def ui_copy_to_note_2(self):
        self.le_p_m_note_plus.setText(self.le_p_m_note_minus.text())

    # Для продажи ткани
    def ui_add_worker_bye(self):
        self.button = "Продажа ткани"
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_add_reason_bye(self):
        self.button = "Продажа ткани"
        self.reason_list = PayReasonMinus(self, True)
        self.reason_list.setWindowModality(Qt.ApplicationModal)
        self.reason_list.show()

    def ui_add_material_name(self):
        self.material_name = supply_material.MaterialName(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_change_weight(self):
        try:
            weight = float(self.le_weight.text().replace(",", "."))
            self.need_weight = False

            query = """SELECT SUM(material_balance.BalanceWeight) FROM material_balance
                                  LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                  WHERE material_supplyposition.Material_NameId = %s"""
            sql_info = my_sql.sql_select(query, (self.le_material_name.whatsThis(),))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql баланс ткани", sql_info.msg, QMessageBox.Ok)
                return False

            if sql_info[0][0] is None:
                self.le_weight.setStyleSheet("border: 4px solid;\nborder-color: rgb(247, 84, 84);")
                self.le_weight.setToolTip("Нету такой ткани на складе")

            elif weight is not None and float(sql_info[0][0]) < weight:
                self.le_weight.setStyleSheet("border: 4px solid;\nborder-color: rgb(247, 84, 84);")
                self.le_weight.setToolTip("Этой ткани не хватит для изменения расходов")

            elif weight is None or float(sql_info[0][0]) >= weight:
                self.le_weight.setStyleSheet("border: 4px solid;\nborder-color: rgb(122, 247, 84);")
                self.le_weight.setToolTip("Новой ткани хватает")
                self.need_weight = True
                self.ui_material_sum_calc()
            else:
                self.le_weight.setStyleSheet("border: 4px solid;\nborder-color: rgb(247, 84, 84);")
                self.le_weight.setToolTip("Что то не так при проверке новой ткани (Обратитесь к админу)")
        except:
            self.le_weight.setStyleSheet("border: 4px solid;\nborder-color: rgb(247, 84, 84);")
            self.le_weight.setToolTip("Что то не так при проверке новой ткани (Обратитесь к админу)")

    def ui_material_sum_calc(self):
        try:
            weight = float(self.le_weight.text().replace(",", "."))
            minus = float(self.le_minus_sum.text().replace(",", "."))
            price = float(self.le_price.text())
        except:
            return False

        self.le_sum.setText(str(round(weight * price - minus, 4)))

    def ui_acc(self):
        if self.id is None:
            if self.menu_text == "Доплата":
                query = """INSERT INTO pay_worker (Worker_Id, Worker_Id_Insert, Reason_Id, Balance, Date_In_Pay, Date_Input, Note, Pay, Date_Pay)
                            VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s)"""
                sql_value = (self.le_work_plus.whatsThis(), User().id(), self.le_reason_plus.whatsThis(), self.le_value_plus.text().replace(",", "."),
                             self.de_plus_date.date().toString(Qt.ISODate), self.le_note_plus.text(), 0, None)
                sql_info = my_sql.sql_change(query, sql_value)
                if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql сохр. доплаты", sql_info.msg, QMessageBox.Ok)
                        return False

            elif self.menu_text == "Вычет":
                query = """INSERT INTO pay_worker (Worker_Id, Worker_Id_Insert, Reason_Id, Balance, Date_In_Pay, Date_Input, Note, Pay, Date_Pay)
                            VALUES (%s, %s, %s, -%s, %s, NOW(), %s, %s, %s)"""
                sql_value = (self.le_work_minus.whatsThis(), User().id(), self.le_reason_minus.whatsThis(), self.le_value_minus.text().replace(",", "."),
                             self.de_minus_date.date().toString(Qt.ISODate), self.le_note_minus.text(), 0, None)
                sql_info = my_sql.sql_change(query, sql_value)
                if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql сохр. вычета", sql_info.msg, QMessageBox.Ok)
                        return False

            elif self.menu_text == "Доплата за проезд":

                sql_values = []
                for row in range(self.tw_road.rowCount()):

                    work_id = self.tw_road.item(row, 0).data(-2)
                    balance = self.tw_road.item(row, 3).text().replace(',', ".")

                    if float(balance) > 0:
                        sql_values.append((work_id, User().id(), self.le_road_reason.whatsThis(), balance.replace(",", "."),
                                           self.de_road_date.date().toString(Qt.ISODate), self.le_note_road.text(), 0, None))

                if not sql_values:
                    return False

                query = """INSERT INTO pay_worker (Worker_Id, Worker_Id_Insert, Reason_Id, Balance, Date_In_Pay, Date_Input, Note, Pay, Date_Pay)
                            VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s)"""
                sql_info = my_sql.sql_many(query, sql_values)
                if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql сохр. дороги", sql_info.msg, QMessageBox.Ok)
                        return False

                self.close()
                self.destroy()

            elif self.menu_text == "Обмен":
                try:
                    float(self.le_p_m_balance.text().replace(",", "."))
                except:
                    QMessageBox.information(self, "Ошибка баланса", "Проверьте значения!", QMessageBox.Ok)
                    return False

                sql_values = []
                sql_values.append((self.le_p_m_worker_minus.whatsThis(), User().id(), self.le_p_m_reason_minus.whatsThis(), -float(self.le_p_m_balance.text().replace(",", ".")),
                                   self.de_p_m_date.date().toString(Qt.ISODate), self.le_p_m_note_minus.text(), 0, None))

                sql_values.append((self.le_p_m_worker_plus.whatsThis(), User().id(), self.le_p_m_reason_plus.whatsThis(), self.le_p_m_balance.text().replace(",", "."),
                                   self.de_p_m_date.date().toString(Qt.ISODate), self.le_p_m_note_plus.text(), 0, None))

                query = """INSERT INTO pay_worker (Worker_Id, Worker_Id_Insert, Reason_Id, Balance, Date_In_Pay, Date_Input, Note, Pay, Date_Pay)
                            VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s)"""
                sql_info = my_sql.sql_many(query, sql_values)
                if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql сохр. обмен", sql_info.msg, QMessageBox.Ok)
                        return False

                self.close()
                self.destroy()

            elif self.menu_text == "Продажа материала":
                if self.need_weight:
                    sql_connect_transaction = my_sql.sql_start_transaction()

                    query = """INSERT INTO pay_worker (Worker_Id, Worker_Id_Insert, Reason_Id, Balance, Date_In_Pay, Date_Input, Note, Pay, Date_Pay)
                            VALUES (%s, %s, %s, -%s, %s, NOW(), %s, %s, %s)"""
                    sql_value = (self.le_work_bye.whatsThis(), User().id(), self.le_reason_bye.whatsThis(), self.le_sum.text().replace(",", "."),
                                 self.de_bye_date.date().toString(Qt.ISODate), self.le_note_bye.text(), 0, None)
                    id_pay = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_value)
                    if "mysql.connector.errors" in str(type(id_pay)):
                            QMessageBox.critical(self, "Ошибка sql сохр. вычета продажи ткани", id_pay.msg, QMessageBox.Ok)
                            return False

                    change_value = float(self.le_weight.text().replace(",", "."))
                    material_id = self.le_material_name.whatsThis()

                    while change_value > 0:
                        # получим первый остаток на складе
                        # Проверяем первое кол-во на складе
                        query = """SELECT material_balance.Id, material_balance.BalanceWeight, MIN(material_supply.Data)
                                      FROM material_balance
                                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                        LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                      WHERE material_supplyposition.Material_NameId = %s AND material_balance.BalanceWeight > 0"""
                        sql_balance_material = my_sql.sql_select_transaction(sql_connect_transaction, query, (material_id, ))
                        if "mysql.connector.errors" in str(type(sql_balance_material)):
                            QMessageBox.critical(self, "Ошибка sql Не смог получить остаток ткани на балансе", sql_balance_material.msg, QMessageBox.Ok)
                        if sql_balance_material[0][1] > change_value:
                            # Если в этом балансе больше чем нам надо
                            take_material_value = change_value
                            change_value = 0
                        else:
                            # Если в этом балансе меньше чем нам надо
                            take_material_value = sql_balance_material[0][1]
                            change_value -= float(sql_balance_material[0][1])
                        # Забираем возможное кол-во
                        query = "UPDATE material_balance SET BalanceWeight = BalanceWeight - %s WHERE Id = %s"
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, (take_material_value, sql_balance_material[0][0]))
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql Не смог забрать ткань с баланса", sql_info.msg, QMessageBox.Ok)

                        # Делаем запись о заборе ткани с баланса склада
                        query = """INSERT INTO transaction_records_material (Supply_Balance_Id, Balance, Date, Note, Cut_Material_Id, Code)
                                    VALUES (%s, %s, SYSDATE(), %s, NULL, 150)"""
                        txt_note = "Продажа ткани работнику № %s, ID вычета %s" % (self.le_work_bye.whatsThis(), id_pay)
                        sql_values = (sql_balance_material[0][0], -take_material_value, txt_note)
                        sql_info = my_sql.sql_change_transaction(sql_connect_transaction, query, sql_values)
                        if "mysql.connector.errors" in str(type(sql_info)):
                            my_sql.sql_rollback_transaction(sql_connect_transaction)
                            QMessageBox.critical(self, "Ошибка sql Не смог добавить запись", sql_info.msg, QMessageBox.Ok)

                    my_sql.sql_commit_transaction(sql_connect_transaction)
                else:
                    QMessageBox.information(self, "Ошибка веса", "У вас что то не так с весом!", QMessageBox.Ok)

            else:
                QMessageBox.critical(self, "Ошибка", "Непонятный элемент меню", QMessageBox.Ok)
                return False

        else:
            if self.menu_text == "Доплата":
                query = """UPDATE pay_worker SET Worker_Id = %s, Reason_Id = %s, Balance = %s, Date_In_Pay = %s, Note = %s WHERE Id = %s"""
                sql_value = (self.le_work_plus.whatsThis(), self.le_reason_plus.whatsThis(), self.le_value_plus.text().replace(",", "."),
                             self.de_plus_date.date().toString(Qt.ISODate), self.le_note_plus.text(), self.id)
                sql_info = my_sql.sql_change(query, sql_value)
                if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql сохр. доплаты", sql_info.msg, QMessageBox.Ok)
                        return False

            elif self.menu_text == "Вычет":
                query = """UPDATE pay_worker SET Worker_Id = %s, Reason_Id = %s, Balance = -%s, Date_In_Pay = %s, Note = %s WHERE Id = %s"""
                sql_value = (self.le_work_minus.whatsThis(), self.le_reason_minus.whatsThis(), self.le_value_minus.text().replace(",", "."),
                             self.de_minus_date.date().toString(Qt.ISODate), self.le_note_minus.text(), self.id)
                sql_info = my_sql.sql_change(query, sql_value)
                if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql сохр. вычета", sql_info.msg, QMessageBox.Ok)
                        return False
            else:
                QMessageBox.critical(self, "Ошибка", "Непонятный элемент меню", QMessageBox.Ok)
                return False

        self.main.ui_update()
        self.close()
        self.destroy()

    def ui_can(self):
        self.close()
        self.destroy()

    def set_table_road(self):
        date_old = self.de_road_date.date()
        date_old = datetime.date(date_old.year(), date_old.month(), date_old.day())

        query = """SELECT One_year, Many_year FROM program_settings_road"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение цен оплаты проезда", sql_info.msg, QMessageBox.Ok)
                return False

        self.one_year_price = sql_info[0][0]
        self.many_year_price = sql_info[0][1]

        query = """SELECT Id, First_Name, Last_Name, Date_Recruitment
                    FROM staff_worker_info
                    WHERE Date_Recruitment < %s AND `Leave` = 0"""
        sql_info = my_sql.sql_select(query, (date_old.replace(date_old.year-1), ))
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение сотрудников со стажем", sql_info.msg, QMessageBox.Ok)
                return False

        self.tw_road.clearContents()
        self.tw_road.setRowCount(0)

        for row, worker in enumerate(sql_info):
            self.tw_road.insertRow(row)

            delta_date = date_old - worker[3]

            if delta_date.days < 730:
                color = QBrush(QColor(252, 252, 139, 255))
                price = self.one_year_price
            else:
                color = QBrush(QColor(252, 190, 139, 255))
                price = self.many_year_price

            new_table_item = QTableWidgetItem(str(worker[2]) + " " + str(worker[1]))
            new_table_item.setData(-2, worker[0])
            new_table_item.setBackground(color)
            new_table_item.setFlags(Qt.ItemIsEnabled)
            self.tw_road.setItem(row, 0, new_table_item)

            new_table_item = QTableWidgetItem(worker[3].strftime("%d.%m.%Y"))
            new_table_item.setData(-2, worker[0])
            new_table_item.setBackground(color)
            new_table_item.setFlags(Qt.ItemIsEnabled)
            self.tw_road.setItem(row, 1, new_table_item)

            new_table_item = QTableWidgetItem(str(delta_date.days))
            new_table_item.setData(-2, worker[0])
            new_table_item.setBackground(color)
            new_table_item.setFlags(Qt.ItemIsEnabled)
            self.tw_road.setItem(row, 2, new_table_item)

            new_table_item = QTableWidgetItem(str(price))
            new_table_item.setData(-2, worker[0])
            new_table_item.setBackground(color)
            self.tw_road.setItem(row, 3, new_table_item)

    def of_list_worker(self, item):
        if self.button == "Плюс минус - Минус":
            self.le_p_m_worker_minus.setWhatsThis(str(item[0]))
            self.le_p_m_worker_minus.setText(item[1])
        elif self.button == "Плюс минус - Плюс":
            self.le_p_m_worker_plus.setWhatsThis(str(item[0]))
            self.le_p_m_worker_plus.setText(item[1])
        elif self.button == "Продажа ткани":
            self.le_work_bye.setWhatsThis(str(item[0]))
            self.le_work_bye.setText(item[1])
        else:
            self.le_work_minus.setWhatsThis(str(item[0]))
            self.le_work_minus.setText(item[1])
            self.le_work_plus.setWhatsThis(str(item[0]))
            self.le_work_plus.setText(item[1])

        self.button = None

    def of_list_reason_plus(self, item):
        if self.button == "Плюс минус - Плюс":
            self.le_p_m_reason_plus.setWhatsThis(str(item[0]))
            self.le_p_m_reason_plus.setText(item[1])
        elif self.button == "Дорога - Плюс":
            self.le_road_reason.setWhatsThis(str(item[0]))
            self.le_road_reason.setText(item[1])
        else:
            self.le_reason_plus.setWhatsThis(str(item[0]))
            self.le_reason_plus.setText(item[1])
        self.button = None

    def of_list_reason_minus(self, item):
        if self.button == "Плюс минус - Минус":
            self.le_p_m_reason_minus.setWhatsThis(str(item[0]))
            self.le_p_m_reason_minus.setText(item[1])
        elif self.button == "Продажа ткани":
            self.le_reason_bye.setWhatsThis(str(item[0]))
            self.le_reason_bye.setText(item[1])
        else:
            self.le_reason_minus.setWhatsThis(str(item[0]))
            self.le_reason_minus.setText(item[1])
        self.button = None

    def of_list_material_name(self, item):
        self.le_material_name.setWhatsThis(str(item[0]))
        self.le_material_name.setText(item[1])

        # Проверим цену материала
        query = """SELECT Price
                        FROM material_name
                          LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                          LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                          LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                        WHERE material_name.Id = %s AND BalanceWeight > 0
                        ORDER BY Data
                        LIMIT 1"""
        sql_info = my_sql.sql_select(query, (item[0], ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql цена ткани", sql_info.msg, QMessageBox.Ok)
            return False
        if sql_info:
            self.le_price.setText(str(round(sql_info[0][0] * Decimal(1.3), 2)))
        else:
            self.le_price.setText("None")

        self.ui_change_weight()


class PayFilter(QDialog):
    def __init__(self, main):
        super(PayFilter, self).__init__()
        loadUi(getcwd() + '/ui/pay_plus_minus_filter.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.main = main

    def ui_view_work(self):
        self.button = "работник"
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_view_reason_plus(self):
        self.reason_list = PayReasonPlus(self, True)
        self.reason_list.setWindowModality(Qt.ApplicationModal)
        self.reason_list.show()

    def ui_view_reason_minus(self):
        self.reason_list = PayReasonMinus(self, True)
        self.reason_list.setWindowModality(Qt.ApplicationModal)
        self.reason_list.show()

    def ui_view_worker_insert(self):
        self.button = "начальник"
        self.worker_list = staff.Staff(self, True)
        self.worker_list.setWindowModality(Qt.ApplicationModal)
        self.worker_list.show()

    def ui_del_work(self):
        self.le_work.setWhatsThis("")
        self.le_work.setText("")

    def ui_del_reason_plus(self):
        self.le_reason_plus.setWhatsThis("")
        self.le_reason_plus.setText("")

    def ui_del_reason_minus(self):
        self.le_reason_minus.setWhatsThis("")
        self.le_reason_minus.setText("")

    def ui_del_worker_insert(self):
        self.le_worker_insert.setWhatsThis("")
        self.le_worker_insert.setText("")

    def ui_acc(self):
        where = ""

        # Блок  условий доплата или вычет
        where_item = ""
        if self.cb_plus.isChecked():
            where_item = self.add_filter(where_item, "pay_worker.Balance > 0", False)

        if self.cb_minus.isChecked():
            where_item = self.add_filter(where_item, "pay_worker.Balance < 0", False)

        if where_item:
            where_item = "(" + where_item + ")"
            where = self.add_filter(where, where_item)

        # Блок  условий выбора работника
        if self.le_work.whatsThis() != '':
            where = self.add_filter(where, "(pay_worker.Worker_Id = %s)" % self.le_work.whatsThis())

        # Блок  условий выбора причины плюса
        if self.le_reason_plus.whatsThis() != '':
            where = self.add_filter(where, "(pay_worker.Reason_Id = %s)" % self.le_reason_plus.whatsThis())

        # Блок  условий выбора причины минуса
        if self.le_reason_minus.whatsThis() != '':
            where = self.add_filter(where, "(pay_worker.Reason_Id = %s)" % self.le_reason_minus.whatsThis())

        # Блок  условий выбора работника который назначил
        if self.le_worker_insert.whatsThis() != '':
            where = self.add_filter(where, "(pay_worker.Worker_Id_Insert = %s)" % self.le_worker_insert.whatsThis())

        # Блок  условий даты внесения
        if self.gb_date_in.isChecked():
            sql_date = "(pay_worker.Date_Input >= '%s' AND pay_worker.Date_Input <= '%s')" % \
                       (self.de_date_in_from.date().toString(Qt.ISODate), self.de_date_in_to.date().toString(Qt.ISODate))
            where = self.add_filter(where, sql_date)

        # Блок  условий даты вступления в силу
        if self.gb_date_pay.isChecked():
            sql_date = "(pay_worker.Date_In_Pay >= '%s' AND pay_worker.Date_In_Pay <= '%s')" % \
                       (self.de_date_pay_from.date().toString(Qt.ISODate), self.de_date_pay_to.date().toString(Qt.ISODate))
            where = self.add_filter(where, sql_date)

        # Делаем замену так как Were должно быть перед ORDER BY
        if where:
            self.sql_query_all = self.sql_query_all.replace("ORDER BY", " WHERE " + where + " ORDER BY")

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

    def of_set_sql_query(self, sql):
        self.sql_query_all = sql

    def of_list_worker(self, item):
        if self.button == "работник":
            self.le_work.setWhatsThis(str(item[0]))
            self.le_work.setText(item[1])
        else:
            self.le_worker_insert.setWhatsThis(str(item[0]))
            self.le_worker_insert.setText(item[1])

    def of_list_reason_plus(self, item):
        self.le_reason_plus.setWhatsThis(str(item[0]))
        self.le_reason_plus.setText(item[1])
        self.ui_del_reason_minus()

    def of_list_reason_minus(self, item):
        self.le_reason_minus.setWhatsThis(str(item[0]))
        self.le_reason_minus.setText(item[1])
        self.ui_del_reason_plus()


class PayReasonPlus(list.ListItems):
    def set_settings(self):
        self.setWindowTitle("Причины +")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(191, 255, 42);")  # Цвет бара
        self.title_new_window = "Причина"  # Имя вызываемых окон

        self.sql_list = "SELECT Id, Name FROM pay_reason WHERE Plus_Or_Minus = 1"
        self.sql_add = "INSERT INTO pay_reason (Name, Note, Plus_Or_Minus) VALUES (%s, %s, 1)"
        self.sql_change_select = "SELECT Name, Note FROM pay_reason WHERE Id = %s"
        self.sql_update_select = 'UPDATE pay_reason SET Name = %s, Note = %s WHERE id = %s'
        self.sql_dell = "DELETE FROM pay_reason WHERE Id = %s"

        self.set_new_win = {"WinTitle": "Причина",
                            "WinColor": "(191, 255, 42)",
                            "lb_name": "Название",
                            "lb_note": "Заметка"}

    def ui_double_click_item(self, select_prov):
        if not self.dc_select:
            self.ui_change_item(select_prov.data(3))
        else:
            item = (select_prov.data(3), select_prov.text())
            self.m_class.of_list_reason_plus(item)
            self.close()
            self.destroy()


class PayReasonMinus(list.ListItems):
    def set_settings(self):
        self.setWindowTitle("Причины -")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(191, 255, 42);")  # Цвет бара
        self.title_new_window = "Причина"  # Имя вызываемых окон

        self.sql_list = "SELECT Id, Name FROM pay_reason WHERE Plus_Or_Minus = 0"
        self.sql_add = "INSERT INTO pay_reason (Name, Note, Plus_Or_Minus) VALUES (%s, %s, 0)"
        self.sql_change_select = "SELECT Name, Note FROM pay_reason WHERE Id = %s"
        self.sql_update_select = 'UPDATE pay_reason SET Name = %s, Note = %s WHERE id = %s'
        self.sql_dell = "DELETE FROM pay_reason WHERE Id = %s"

        self.set_new_win = {"WinTitle": "Причина",
                            "WinColor": "(191, 255, 42)",
                            "lb_name": "Название",
                            "lb_note": "Заметка"}

    def ui_double_click_item(self, select_prov):
        if not self.dc_select:
            self.ui_change_item(select_prov.data(3))
        else:
            item = (select_prov.data(3), select_prov.text())
            self.m_class.of_list_reason_minus(item)
            self.close()
            self.destroy()


class PayChangeReason(QDialog):
    def __init__(self):
        super(PayChangeReason, self).__init__()
        loadUi(getcwd() + '/ui/pay_change_reason.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.from_plus_id = None
        self.from_plus_name = None
        self.from_minus_id = None
        self.from_minus_name = None

        self.update_pluse_reasons()
        self.update_minus_reasons()

    def update_pluse_reasons(self):
        query = """SELECT Id, Name FROM pay_reason WHERE Plus_Or_Minus = 1"""
        sql_result = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_result)):
            QMessageBox.critical(self, "Ошибка sql получение причин", sql_result.msg, QMessageBox.Ok)
            return False

        self.lw_plus.clear()
        for item in sql_result:
            item_list = QListWidgetItem(item[1])
            item_list.setData(3, item[0])
            self.lw_plus.addItem(item_list)

    def update_minus_reasons(self):
        query = """SELECT Id, Name FROM pay_reason WHERE Plus_Or_Minus = 0"""
        sql_result = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_result)):
            QMessageBox.critical(self, "Ошибка sql получение причин", sql_result.msg, QMessageBox.Ok)
            return False

        self.lw_minus.clear()
        for item in sql_result:
            item_list = QListWidgetItem(item[1])
            item_list.setData(3, item[0])
            self.lw_minus.addItem(item_list)

    def select_plus_reason(self, item):
        self.from_plus_id = item.data(3)
        self.from_plus_name = item.text()
        self.reason_list = PayReasonPlus(self, True)
        self.reason_list.setWindowModality(Qt.ApplicationModal)
        self.reason_list.show()

    def select_minus_reason(self, item):
        self.from_minus_id = item.data(3)
        self.from_minus_name = item.text()
        self.reason_list = PayReasonMinus(self, True)
        self.reason_list.setWindowModality(Qt.ApplicationModal)
        self.reason_list.show()

    def of_list_reason_plus(self, item):
        text = "Меняем " + self.from_plus_name + "  -->  " + item[1]
        result = QMessageBox.question(self, "Изменение", text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            self.change_reason(self.from_plus_id, item[0])
            self.update_pluse_reasons()

    def of_list_reason_minus(self, item):
        text = "Меняем " + self.from_minus_name + "  -->  " + item[1]
        result = QMessageBox.question(self, "Изменение", text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:
            self.change_reason(self.from_minus_id, item[0])
            self.update_minus_reasons()

    def change_reason(self, from_id, to_id):
        print(from_id, to_id)
        query = "UPDATE pay_worker SET Reason_Id = %s WHERE Reason_Id = %s"
        sql_result = my_sql.sql_change(query, (to_id, from_id))
        if "mysql.connector.errors" in str(type(sql_result)):
            QMessageBox.critical(self, "Ошибка sql изменения причины", sql_result.msg, QMessageBox.Ok)
            return False

        query = "DELETE FROM pay_reason WHERE id = %s"
        sql_result = my_sql.sql_change(query, (from_id, ))
        if "mysql.connector.errors" in str(type(sql_result)):
            QMessageBox.critical(self, "Ошибка sql удаления причины", sql_result.msg, QMessageBox.Ok)
            return False
