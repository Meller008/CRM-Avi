from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QMainWindow,  QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate
from function import my_sql
from decimal import Decimal
import re

report_all_class = loadUiType(getcwd() + '/ui/report_all.ui')[0]


class ReportAll(QMainWindow, report_all_class):
    def __init__(self):
        super(ReportAll, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_settings()

    def start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

        self.tw_material_1.horizontalHeader().resizeSection(0, 190)
        self.tw_material_1.horizontalHeader().resizeSection(1, 90)
        self.tw_material_1.horizontalHeader().resizeSection(2, 90)
        self.tw_material_1.horizontalHeader().resizeSection(3, 40)
        self.tw_material_1.horizontalHeader().resizeSection(4, 90)
        self.tw_material_1.horizontalHeader().resizeSection(5, 90)

        self.tw_material_2.horizontalHeader().resizeSection(0, 195)
        self.tw_material_2.horizontalHeader().resizeSection(1, 90)
        self.tw_material_2.horizontalHeader().resizeSection(2, 90)

        self.tw_material_3.horizontalHeader().resizeSection(0, 190)
        self.tw_material_3.horizontalHeader().resizeSection(1, 90)
        self.tw_material_3.horizontalHeader().resizeSection(2, 90)
        self.tw_material_3.horizontalHeader().resizeSection(3, 90)
        self.tw_material_3.horizontalHeader().resizeSection(4, 90)

    def ui_calc(self):
        index_tab = self.tabWidget.currentIndex()

        if index_tab == 1:
            self.calc_material()

    def calc_material(self):

        try:
            old_balance_value = Decimal(self.le_last_balance_value.text().replace(",", "."))
            old_balance_sum = Decimal(self.le_last_balance_sum.text().replace(",", "."))
        except:
            QMessageBox.critical(self, "Ошибка баланса", "Что то не так с балансом! Не могу его получить!", QMessageBox.Ok)
            return False

        # Таблица 1
        #
        filter_date = (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate())
        self.tw_material_1.clearContents()
        self.tw_material_1.setRowCount(0)
        material = {}

        # Получим приходы
        query = """SELECT material_name.Id, material_name.Name, SUM(material_supplyposition.Weight), COUNT(material_supply.Id),
                        SUM(material_supplyposition.Weight * material_supplyposition.Price)
                      FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                        LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                      WHERE material_supply.Data BETWEEN %s AND %s
                      GROUP BY material_name.Id"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение приходов", sql_info.msg, QMessageBox.Ok)
                return False

        for material_in in sql_info:
            new_tup = {'name': material_in[1], 'value_in': material_in[2], "sum_in": material_in[4], "pcs": material_in[3], 'value_out': 0, "sum_out": 0}
            material.update({material_in[0]: new_tup})

        # Получим расход
        query = """SELECT material_name.Id, material_name.Name, SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                        LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                        LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                      WHERE transaction_records_material.Cut_Material_Id IN (SELECT cut.Id FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)
                          OR transaction_records_material.Beika_Id IN (SELECT beika.Id FROM beika WHERE Date >= %s AND Date <= %s)
                          OR (transaction_records_material.Code IN (150, 151) AND transaction_records_material.Date >= %s 
                                AND transaction_records_material.Date <= DATE_FORMAT(%s,'%Y-%m-%d 23:59:59'))
                      GROUP BY material_name.Id"""
        sql_info = my_sql.sql_select(query, filter_date*3)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расходов", sql_info.msg, QMessageBox.Ok)
            return False

        # Соединим расход с приходом
        for material_out in sql_info:
            if material.get(material_out[0]) is None:
                new_tup = {'name': material_out[1], 'value_in': 0, "sum_in": 0, "pcs": 0, 'value_out': 0, "sum_out": 0}
                material.update({material_out[0]: new_tup})

            material[material_out[0]]["value_out"] += material_out[2]
            material[material_out[0]]["sum_out"] += material_out[3]

        # Вставим все в таблицу
        all_value_in, all_sum_in, all_value_out, all_sum_out = 0, 0, 0, 0

        for key, value in material.items():
            self.tw_material_1.insertRow(self.tw_material_1.rowCount())

            item = QTableWidgetItem(str(value["name"]))
            self.tw_material_1.setItem(self.tw_material_1.rowCount() - 1, 0, item)

            all_value_in += value["value_in"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["value_in"], 2)))
            item = QTableWidgetItem(text)
            self.tw_material_1.setItem(self.tw_material_1.rowCount() - 1, 1, item)

            all_sum_in += value["sum_in"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["sum_in"], 2)))
            item = QTableWidgetItem(text)
            self.tw_material_1.setItem(self.tw_material_1.rowCount() - 1, 2, item)

            item = QTableWidgetItem(str(value["pcs"]))
            self.tw_material_1.setItem(self.tw_material_1.rowCount() - 1, 3, item)

            all_value_out += value["value_out"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["value_out"], 2)))
            item = QTableWidgetItem(text)
            self.tw_material_1.setItem(self.tw_material_1.rowCount() - 1, 4, item)

            all_sum_out += value["sum_out"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["sum_out"], 2)))
            item = QTableWidgetItem(text)
            self.tw_material_1.setItem(self.tw_material_1.rowCount() - 1, 5, item)

        else:
            self.tw_material_1.insertRow(self.tw_material_1.rowCount())

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_value_in, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_1.setItem(self.tw_material_1.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_in, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_1.setItem(self.tw_material_1.rowCount() - 1, 2, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_value_out, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_1.setItem(self.tw_material_1.rowCount() - 1, 4, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_out, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_1.setItem(self.tw_material_1.rowCount() - 1, 5, item)

            self.le_supply_value.setText(str(round(all_value_in, 2)))
            self.le_supply_sum.setText(str(round(all_sum_in, 2)))
            self.le_consumption_value.setText(str(round(all_value_out, 2)))
            self.le_consumption_sum.setText(str(round(all_sum_out, 2)))

        # Таблица 2
        # Заполним подробный расход
        self.tw_material_2.clearContents()
        self.tw_material_2.setRowCount(0)

        query = """SELECT Note, SUM(transaction_records_material.Balance), SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Code IN (120, 121, 123, 124, 133, 134)
                        AND transaction_records_material.Cut_Material_Id IN (SELECT cut.Id FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)
                        GROUP BY Code"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на пачки", sql_info.msg, QMessageBox.Ok)
            return False

        all_info_value, all_info_sum = 0, 0

        sum_value, sum_sum = 0, 0
        self.tw_material_2.insertRow(self.tw_material_2.rowCount())
        self.tw_material_2.setSpan(self.tw_material_2.rowCount()-1, 0, 1, 3)
        item = QTableWidgetItem("Пачки")
        item.setTextAlignment(Qt.AlignHCenter)
        self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

        for i in sql_info:
            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            item = QTableWidgetItem(i[0])
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

            sum_value += i[1] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[1] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            sum_sum += i[2] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        else:
            all_info_value += sum_value
            all_info_sum += sum_sum

            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        query = """SELECT Note, SUM(transaction_records_material.Balance), SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Code IN (130, 131, 132)
                        AND transaction_records_material.Cut_Material_Id IN (SELECT cut.Id FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)
                        GROUP BY Code"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на обрезь", sql_info.msg, QMessageBox.Ok)
            return False

        sum_value, sum_sum = 0, 0
        self.tw_material_2.insertRow(self.tw_material_2.rowCount())
        self.tw_material_2.setSpan(self.tw_material_2.rowCount()-1, 0, 1, 3)
        item = QTableWidgetItem("Обрезь")
        item.setTextAlignment(Qt.AlignHCenter)
        self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

        for i in sql_info:
            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            item = QTableWidgetItem(i[0])
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

            sum_value += i[1] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[1] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            sum_sum += i[2] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        else:
            all_info_value += sum_value
            all_info_sum += sum_sum

            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        query = """SELECT Note, SUM(transaction_records_material.Balance), SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Code IN (125, 126)
                        AND transaction_records_material.Cut_Material_Id IN (SELECT cut.Id FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)
                        GROUP BY Code"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на доп ткань", sql_info.msg, QMessageBox.Ok)
            return False

        sum_value, sum_sum = 0, 0
        self.tw_material_2.insertRow(self.tw_material_2.rowCount())
        self.tw_material_2.setSpan(self.tw_material_2.rowCount()-1, 0, 1, 3)
        item = QTableWidgetItem("Доп. ткань")
        item.setTextAlignment(Qt.AlignHCenter)
        self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

        for i in sql_info:
            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            item = QTableWidgetItem(i[0])
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

            sum_value += i[1] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[1] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            sum_sum += i[2] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        else:
            all_info_value += sum_value
            all_info_sum += sum_sum

            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        query = """SELECT Note, SUM(transaction_records_material.Balance), SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Code IN (140, 141)
                        AND transaction_records_material.Beika_Id IN (SELECT beika.Id FROM beika WHERE Date >= %s AND Date <= %s)
                        GROUP BY Code"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на бйеку", sql_info.msg, QMessageBox.Ok)
            return False

        sum_value, sum_sum = 0, 0
        self.tw_material_2.insertRow(self.tw_material_2.rowCount())
        self.tw_material_2.setSpan(self.tw_material_2.rowCount()-1, 0, 1, 3)
        item = QTableWidgetItem("Бейка")
        item.setTextAlignment(Qt.AlignHCenter)
        self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

        for i in sql_info:
            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            item = QTableWidgetItem(i[0])
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

            sum_value += i[1] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[1] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            sum_sum += i[2] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        else:
            all_info_value += sum_value
            all_info_sum += sum_sum

            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        query = """SELECT Note, SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Code = 150
                        AND transaction_records_material.Date >= %s AND transaction_records_material.Date <= DATE_FORMAT(%s,'%Y-%m-%d 23:59:59')"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на продажу ткани", sql_info.msg, QMessageBox.Ok)
            return False

        sum_value, sum_sum = 0, 0
        self.tw_material_2.insertRow(self.tw_material_2.rowCount())
        self.tw_material_2.setSpan(self.tw_material_2.rowCount()-1, 0, 1, 3)
        item = QTableWidgetItem("Продажа ткани")
        item.setTextAlignment(Qt.AlignHCenter)
        self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

        for i in sql_info:
            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            item = QTableWidgetItem(i[0])
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

            sum_value += i[1] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[1] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            sum_sum += i[2] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        else:
            all_info_value += sum_value
            all_info_sum += sum_sum

            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        query = """SELECT Note, SUM(transaction_records_material.Balance), SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Code NOT IN (120, 121, 123, 124, 130, 131, 132, 140, 141, 150, 110, 111, 126, 125, 133, 134)
                        AND transaction_records_material.Date >= %s AND transaction_records_material.Date <= DATE_FORMAT(%s,'%Y-%m-%d 23:59:59')
                        GROUP BY Code"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода прочего", sql_info.msg, QMessageBox.Ok)
            return False

        sum_value, sum_sum = 0, 0
        self.tw_material_2.insertRow(self.tw_material_2.rowCount())
        self.tw_material_2.setSpan(self.tw_material_2.rowCount()-1, 0, 1, 3)
        item = QTableWidgetItem("Прочее")
        item.setTextAlignment(Qt.AlignHCenter)
        self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

        for i in sql_info:
            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            item = QTableWidgetItem(i[0])
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 0, item)

            sum_value += i[1] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[1] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            sum_sum += i[2] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        else:
            all_info_value += sum_value
            all_info_sum += sum_sum

            self.tw_material_2.insertRow(self.tw_material_2.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        # Отобразим сумму
        self.tw_material_2.insertRow(self.tw_material_2.rowCount())
        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_info_value, 2)))
        item = QTableWidgetItem(text)
        self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_info_sum, 2)))
        item = QTableWidgetItem(text)
        self.tw_material_2.setItem(self.tw_material_2.rowCount() - 1, 2, item)

        # Таблица 3
        # Заполним таблицу расхода по транзакциям
        self.tw_material_3.clearContents()
        self.tw_material_3.setRowCount(0)

        query = """SELECT trm.Note, SUM(IF(trm.Date >= %s, trm.Balance, 0)), SUM(IF(trm.Date >= %s, trm.Balance * material_supplyposition.Price, 0)),
                        SUM(trm.Balance), SUM(trm.Balance * material_supplyposition.Price) AS sum_m
                      FROM transaction_records_material AS trm LEFT JOIN material_balance ON trm.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                        LEFT JOIN cut ON trm.Cut_Material_Id = cut.Id
                        LEFT JOIN beika ON trm.Beika_Id = beika.Id
                      WHERE cut.Date_Cut <= %s OR trm.Date <= DATE_FORMAT(%s,'%Y-%m-%d 23:59:59') OR (beika.Date <= %s AND beika.Finished = 1)
                        or trm.Supply_Balance_Id IN (SELECT material_balance.Id FROM material_supply
                                                          LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                                                          LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                                                        WHERE material_supply.Data <= %s AND (trm.Note LIKE 'Заказ % - %'))
                      GROUP BY Code"""
        date = (self.de_date_from.date().toPyDate(),self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate(),
                self.de_date_to.date().toPyDate(), self.de_date_to.date().toPyDate(), self.de_date_to.date().toPyDate())
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения транзакций", sql_info.msg, QMessageBox.Ok)
            return False

        all_transaction_value, all_transaction_sum, all_transaction_value_month, all_transaction_sum_month = 0, 0, 0, 0
        for transaction in sql_info:
            self.tw_material_3.insertRow(self.tw_material_3.rowCount())
            item = QTableWidgetItem(transaction[0])
            self.tw_material_3.setItem(self.tw_material_3.rowCount() - 1, 0, item)

            all_transaction_value_month += transaction[1] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(transaction[1] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_3.setItem(self.tw_material_3.rowCount() - 1, 1, item)

            all_transaction_sum_month += transaction[2] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(transaction[2] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_3.setItem(self.tw_material_3.rowCount() - 1, 2, item)

            all_transaction_value += transaction[3] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(transaction[3] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_3.setItem(self.tw_material_3.rowCount() - 1, 3, item)

            all_transaction_sum += transaction[4] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(transaction[4] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_3.setItem(self.tw_material_3.rowCount() - 1, 4, item)

        else:
            self.tw_material_3.insertRow(self.tw_material_3.rowCount())

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_transaction_value_month, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_3.setItem(self.tw_material_3.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_transaction_sum_month, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_3.setItem(self.tw_material_3.rowCount() - 1, 2, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_transaction_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_3.setItem(self.tw_material_3.rowCount() - 1, 3, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_transaction_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_material_3.setItem(self.tw_material_3.rowCount() - 1, 4, item)

            self.le_transaction_balance_value.setText(str(round(all_transaction_value, 2)))
            self.le_transaction_balance_sum.setText(str(round(all_transaction_sum, 2)))

        balance_value = all_value_in + old_balance_value - -all_value_out
        balance_sum = all_sum_in + old_balance_sum - -all_sum_out

        self.le_new_balance_value.setText(str(round(balance_value, 2)))
        self.le_new_balance_sum.setText(str(round(balance_sum, 2)))

        difference_value = all_transaction_value - balance_value
        difference_sum = all_transaction_sum - balance_sum

        self.le_difference_value.setText(str(round(difference_value, 2)))
        self.le_difference_sum.setText(str(round(difference_sum, 2)))

