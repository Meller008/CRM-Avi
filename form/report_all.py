from os import getcwd
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QTableWidgetItem, QDialog, QListWidgetItem
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt, QDate
from function import my_sql, table_to_html
from decimal import Decimal
from classes import print_qt
import datetime
import re


class ReportAll(QMainWindow):
    def __init__(self):
        super(ReportAll, self).__init__()
        loadUi(getcwd() + '/ui/report_all.ui', self)
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
        
        self.tw_accessories_1.horizontalHeader().resizeSection(0, 190)
        self.tw_accessories_1.horizontalHeader().resizeSection(1, 90)
        self.tw_accessories_1.horizontalHeader().resizeSection(2, 90)
        self.tw_accessories_1.horizontalHeader().resizeSection(3, 40)
        self.tw_accessories_1.horizontalHeader().resizeSection(4, 90)
        self.tw_accessories_1.horizontalHeader().resizeSection(5, 90)

        self.tw_accessories_2.horizontalHeader().resizeSection(0, 195)
        self.tw_accessories_2.horizontalHeader().resizeSection(1, 90)
        self.tw_accessories_2.horizontalHeader().resizeSection(2, 90)

        self.tw_accessories_3.horizontalHeader().resizeSection(0, 190)
        self.tw_accessories_3.horizontalHeader().resizeSection(1, 90)
        self.tw_accessories_3.horizontalHeader().resizeSection(2, 90)
        self.tw_accessories_3.horizontalHeader().resizeSection(3, 90)
        self.tw_accessories_3.horizontalHeader().resizeSection(4, 90)

        self.tw_comparing_1.horizontalHeader().resizeSection(0, 150)
        self.tw_comparing_1.horizontalHeader().resizeSection(1, 80)
        self.tw_comparing_1.horizontalHeader().resizeSection(2, 80)

        self.tw_comparing_2.horizontalHeader().resizeSection(0, 150)
        self.tw_comparing_2.horizontalHeader().resizeSection(1, 80)
        self.tw_comparing_2.horizontalHeader().resizeSection(2, 80)

        self.tw_product_1.horizontalHeader().resizeSection(0, 120)
        self.tw_product_1.horizontalHeader().resizeSection(1, 50)
        self.tw_product_1.horizontalHeader().resizeSection(2, 50)
        self.tw_product_1.horizontalHeader().resizeSection(3, 75)
        self.tw_product_1.horizontalHeader().resizeSection(4, 50)
        self.tw_product_1.horizontalHeader().resizeSection(5, 75)
        self.tw_product_1.horizontalHeader().resizeSection(6, 75)
        self.tw_product_1.horizontalHeader().resizeSection(7, 75)

        self.tw_product_2.horizontalHeader().resizeSection(0, 100)
        self.tw_product_2.horizontalHeader().resizeSection(1, 60)
        self.tw_product_2.horizontalHeader().resizeSection(2, 70)
        self.tw_product_2.horizontalHeader().resizeSection(3, 70)
        self.tw_product_2.horizontalHeader().resizeSection(4, 80)
        self.tw_product_2.horizontalHeader().resizeSection(5, 80)
        self.tw_product_2.horizontalHeader().resizeSection(6, 50)

        self.tw_product_3.horizontalHeader().resizeSection(0, 150)
        self.tw_product_3.horizontalHeader().resizeSection(1, 65)
        self.tw_product_3.horizontalHeader().resizeSection(2, 70)
        self.tw_product_3.horizontalHeader().resizeSection(3, 70)
        self.tw_product_3.horizontalHeader().resizeSection(4, 95)
        self.tw_product_3.horizontalHeader().resizeSection(5, 95)
        self.tw_product_3.horizontalHeader().resizeSection(6, 70)
        self.tw_product_3.horizontalHeader().resizeSection(7, 95)
        self.tw_product_3.horizontalHeader().resizeSection(8, 95)

        self.tw_product_4.horizontalHeader().resizeSection(0, 200)
        self.tw_product_4.horizontalHeader().resizeSection(1, 80)

        self.tw_save_material.horizontalHeader().resizeSection(0, 70)
        self.tw_save_material.horizontalHeader().resizeSection(1, 70)
        self.tw_save_material.horizontalHeader().resizeSection(2, 70)
        self.tw_save_material.horizontalHeader().resizeSection(3, 85)
        self.tw_save_material.horizontalHeader().resizeSection(4, 85)
        self.tw_save_material.horizontalHeader().resizeSection(5, 85)
        self.tw_save_material.horizontalHeader().resizeSection(6, 85)
        self.tw_save_material.horizontalHeader().resizeSection(7, 85)
        self.tw_save_material.horizontalHeader().resizeSection(8, 85)
        self.tw_save_material.horizontalHeader().resizeSection(9, 85)
        self.tw_save_material.horizontalHeader().resizeSection(10, 85)
        self.tw_save_material.horizontalHeader().resizeSection(11, 85)
        self.tw_save_material.horizontalHeader().resizeSection(12, 85)
        self.tw_save_material.horizontalHeader().resizeSection(13, 85)
        self.tw_save_material.horizontalHeader().resizeSection(14, 85)
        self.tw_save_material.horizontalHeader().resizeSection(15, 85)

        self.tw_save_accessories.horizontalHeader().resizeSection(0, 70)
        self.tw_save_accessories.horizontalHeader().resizeSection(1, 70)
        self.tw_save_accessories.horizontalHeader().resizeSection(2, 70)
        self.tw_save_accessories.horizontalHeader().resizeSection(3, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(4, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(5, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(6, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(7, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(8, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(9, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(10, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(11, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(12, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(13, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(14, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(15, 85)

        self.tw_save_accessories.horizontalHeader().resizeSection(0, 70)
        self.tw_save_accessories.horizontalHeader().resizeSection(1, 70)
        self.tw_save_accessories.horizontalHeader().resizeSection(2, 70)
        self.tw_save_accessories.horizontalHeader().resizeSection(3, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(4, 85)
        self.tw_save_accessories.horizontalHeader().resizeSection(5, 85)

        self.tw_save_product.horizontalHeader().resizeSection(0, 70)
        self.tw_save_product.horizontalHeader().resizeSection(1, 70)
        self.tw_save_product.horizontalHeader().resizeSection(2, 70)
        self.tw_save_product.horizontalHeader().resizeSection(3, 85)
        self.tw_save_product.horizontalHeader().resizeSection(4, 85)
        self.tw_save_product.horizontalHeader().resizeSection(5, 85)
        self.tw_save_product.horizontalHeader().resizeSection(6, 85)
        self.tw_save_product.horizontalHeader().resizeSection(7, 85)
        self.tw_save_product.horizontalHeader().resizeSection(8, 85)
        self.tw_save_product.horizontalHeader().resizeSection(9, 85)
        self.tw_save_product.horizontalHeader().resizeSection(10, 85)
        self.tw_save_product.horizontalHeader().resizeSection(11, 85)
        self.tw_save_product.horizontalHeader().resizeSection(12, 85)
        self.tw_save_product.horizontalHeader().resizeSection(13, 85)
        self.tw_save_product.horizontalHeader().resizeSection(14, 85)
        self.tw_save_product.horizontalHeader().resizeSection(15, 85)
        self.tw_save_product.horizontalHeader().resizeSection(16, 85)
        self.tw_save_product.horizontalHeader().resizeSection(17, 85)
        self.tw_save_product.horizontalHeader().resizeSection(18, 85)

    def ui_calc(self):
        index_tab = self.tabWidget.currentIndex()

        if index_tab == 1:
            self.calc_material()
        elif index_tab == 2:
            self.calc_accessories()
        elif index_tab == 3:
            self.calc_comparing()
        elif index_tab == 4 or index_tab == 5:
            self.calc_production()
        elif index_tab == 6:
            self.calc_total()
        elif index_tab == 7:
            self.view_save()

    def ui_print(self):
        index_tab = self.tabWidget.currentIndex()

        if index_tab == 1:
            self.print_material()
        elif index_tab == 2:
            self.print_accessories()
        elif index_tab == 3:
            self.print_comparing()
        elif index_tab == 4 or index_tab == 5:
            self.print_production()
        elif index_tab == 7:
            self.print_save()

    # Расчет ткани

    def calc_material(self):

        try:
            old_balance_value = Decimal(self.le_last_balance_value.text().replace(",", "."))
            old_balance_sum = Decimal(self.le_last_balance_sum.text().replace(",", "."))
        except:
            QMessageBox.critical(self, "Ошибка баланса", "Что то не так с балансом! Не могу его получить!", QMessageBox.Ok)
            return False

        self.le_last_balance_material_total.setText(str(round(old_balance_sum, 2)))

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
        sql_info = my_sql.sql_select(query, filter_date * 3)
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

            self.le_supply_sum_material_total.setText(str(round(all_sum_in, 2)))
            self.le_consumption_sum_material_total.setText(str(round(all_sum_out, 2)))

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
        self.tw_material_2.setSpan(self.tw_material_2.rowCount() - 1, 0, 1, 3)
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
        self.tw_material_2.setSpan(self.tw_material_2.rowCount() - 1, 0, 1, 3)
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
        self.tw_material_2.setSpan(self.tw_material_2.rowCount() - 1, 0, 1, 3)
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
        self.tw_material_2.setSpan(self.tw_material_2.rowCount() - 1, 0, 1, 3)
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
        self.tw_material_2.setSpan(self.tw_material_2.rowCount() - 1, 0, 1, 3)
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
        self.tw_material_2.setSpan(self.tw_material_2.rowCount() - 1, 0, 1, 3)
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
                        OR trm.Supply_Balance_Id IN (SELECT material_balance.Id FROM material_supply
                                                          LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                                                          LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                                                        WHERE material_supply.Data <= %s AND trm.Code IN (110, 111))
                      GROUP BY Code"""
        date = (self.de_date_from.date().toPyDate(), self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate(),
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

        self.le_transaction_balance_material.setText(str(round(all_transaction_sum, 2)))
        if difference_sum > 0:
            self.le_adjustments_plus_material.setText(str(round(difference_sum, 2)))
        elif difference_sum < 0:
            self.le_adjustments_minus_material.setText(str(round(difference_sum, 2)))

    def print_material(self):
        up_html = """
          <table>
          <caption>#head#</caption>
          <tr> <th>Остаток прошлый кол-во</th><th>Приход кол-во</th><th>Расход кол-во</th><th>Остаток кол-во</th><th>Остаток транз. кол-во</th><th>Разница кол-во</th> </tr>
          <tr> <td>#le_last_balance_value#</td><td>#le_supply_value#</td><td>#le_consumption_value#</td><td>#le_new_balance_value#</td><td>#le_transaction_balance_value#</td><td>#le_difference_value#</td> </tr>
          
          <tr> <th>Остаток прошлый рублей</th><th>Приход рублей</th><th>Расход рублей</th><th>Остаток рублей</th><th>Остаток транз. рублей</th><th>Разница рублей</th> </tr>
          <tr> <td>#le_last_balance_sum#</td><td>#le_supply_sum#</td><td>#le_consumption_sum#</td><td>#le_new_balance_sum#</td><td>#le_transaction_balance_sum#</td><td>#le_difference_sum#</td> </tr>
          </table>"""

        head = "Отчет по ткани %s - %s" % (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate))
        up_html = up_html.replace("#head#", head)
        up_html = up_html.replace("#le_last_balance_value#", self.le_last_balance_value.text())
        up_html = up_html.replace("#le_supply_value#", self.le_supply_value.text())
        up_html = up_html.replace("#le_consumption_value#", self.le_consumption_value.text())
        up_html = up_html.replace("#le_new_balance_value#", self.le_new_balance_value.text())
        up_html = up_html.replace("#le_transaction_balance_value#", self.le_transaction_balance_value.text())
        up_html = up_html.replace("#le_difference_value#", self.le_difference_value.text())

        up_html = up_html.replace("#le_last_balance_sum#", self.le_last_balance_sum.text())
        up_html = up_html.replace("#le_supply_sum#", self.le_supply_sum.text())
        up_html = up_html.replace("#le_consumption_sum#", self.le_consumption_sum.text())
        up_html = up_html.replace("#le_new_balance_sum#", self.le_new_balance_sum.text())
        up_html = up_html.replace("#le_transaction_balance_sum#", self.le_transaction_balance_sum.text())
        up_html = up_html.replace("#le_difference_sum#", self.le_difference_sum.text())

        html = table_to_html.tab_html(self.tw_material_1, table_head="Приход + расход (Живой)", up_template=up_html)
        html += '<div style="display: inline-block; width: 100%">'
        html += table_to_html.tab_html(self.tw_material_2, table_head="Подробный расход (Живой)")
        html += '</div> <div style="display: inline-block; width: 100%">'
        html += table_to_html.tab_html(self.tw_material_3, table_head="Суммы транзакций  (Живой + Неживой) за месяц / всего ДО этой даты")
        html += '</div>'
        self.print_class = print_qt.PrintHtml(self, html)

    def ui_material_save(self):
        query = """INSERT INTO report_all_material_save (Date_Save, Date_From, Date_To, Last_Balance_Value, Last_Balance_Sum, Supply_Value,
                                      Supply_Sum, Consumption_Value, Consumption_Sum, New_Balance_Value, New_Balance_Sum,
                                      Transaction_Balance_Value, Transaction_Balance_Sum, Difference_Value, Difference_Sum)
                      VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        parametrs = (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate(), self.le_last_balance_value.text(),
                     self.le_last_balance_sum.text(), self.le_supply_value.text(), self.le_supply_sum.text(), self.le_consumption_value.text(),
                     self.le_consumption_sum.text(), self.le_new_balance_value.text(), self.le_new_balance_sum.text(), self.le_transaction_balance_value.text(),
                     self.le_transaction_balance_sum.text(), self.le_difference_value.text(), self.le_difference_sum.text())

        sql_info = my_sql.sql_change(query, parametrs)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql сохранения отчета!", sql_info.msg, QMessageBox.Ok)
            return False
        else:
            QMessageBox.information(self, "Сохранено", "Отчет успешно сохранен!", QMessageBox.Ok)

    def ui_view_save_report_material(self):
        self.save_date_window = SaveReportMaterial("ткань")
        self.save_date_window.setModal(True)
        self.save_date_window.show()

        if self.save_date_window.exec_() != 1:
            return False

        self.le_last_balance_value.setText(str(self.save_date_window.balance_value))
        self.le_last_balance_sum.setText(str(self.save_date_window.balance_sum))

    # Расчет фурнитуры

    def calc_accessories(self):

        try:
            old_balance_value = Decimal(self.le_last_balance_value_accessories.text().replace(",", "."))
            old_balance_sum = Decimal(self.le_last_balance_sum_accessories.text().replace(",", "."))
        except:
            QMessageBox.critical(self, "Ошибка баланса", "Что то не так с балансом! Не могу его получить!", QMessageBox.Ok)
            return False

        self.le_last_balance_accessories_total.setText(str(round(old_balance_sum, 2)))

        # Таблица 1
        #
        filter_date = (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate())
        self.tw_accessories_1.clearContents()
        self.tw_accessories_1.setRowCount(0)
        material = {}

        # Получим приходы
        query = """SELECT accessories_name.Id, accessories_name.Name, SUM(accessories_supplyposition.Value), COUNT(accessories_supply.Id), 
                          SUM(accessories_supplyposition.Value * accessories_supplyposition.Price)
                      FROM accessories_supply LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.Accessories_SupplyId
                        LEFT JOIN accessories_name ON accessories_supplyposition.Accessories_NameId = accessories_name.Id
                      WHERE accessories_supply.Data BETWEEN %s AND %s
                      GROUP BY accessories_name.Id"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение приходов", sql_info.msg, QMessageBox.Ok)
            return False

        for material_in in sql_info:
            new_tup = {'name': material_in[1], 'value_in': material_in[2], "sum_in": material_in[4], "pcs": material_in[3], 'value_out': 0, "sum_out": 0}
            material.update({material_in[0]: new_tup})

        # Получим расход
        query = """SELECT accessories_name.Id, accessories_name.Name, SUM(transaction_records_accessories.Balance),
                        SUM(transaction_records_accessories.Balance * accessories_supplyposition.Price)
                      FROM transaction_records_accessories LEFT JOIN accessories_balance ON transaction_records_accessories.Supply_Balance_Id = accessories_balance.Id
                      LEFT JOIN accessories_supplyposition ON accessories_balance.accessories_SupplyPositionId = accessories_supplyposition.Id
                        LEFT JOIN accessories_supply ON accessories_supplyposition.accessories_SupplyId = accessories_supply.Id
                        LEFT JOIN accessories_name ON accessories_supplyposition.accessories_NameId = accessories_name.Id
                      WHERE transaction_records_accessories.Pack_Accessories_Id IN (SELECT pack_accessories.Id
                                                                                      FROM pack_accessories LEFT JOIN pack ON pack_accessories.Pack_Id = pack.Id
                                                                                        LEFT JOIN cut ON pack.Cut_Id = cut.Id
                                                                                      WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)
                      GROUP BY accessories_name.Id"""
        sql_info = my_sql.sql_select(query, filter_date)
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
            self.tw_accessories_1.insertRow(self.tw_accessories_1.rowCount())

            item = QTableWidgetItem(str(value["name"]))
            self.tw_accessories_1.setItem(self.tw_accessories_1.rowCount() - 1, 0, item)

            all_value_in += value["value_in"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["value_in"], 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_1.setItem(self.tw_accessories_1.rowCount() - 1, 1, item)

            all_sum_in += value["sum_in"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["sum_in"], 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_1.setItem(self.tw_accessories_1.rowCount() - 1, 2, item)

            item = QTableWidgetItem(str(value["pcs"]))
            self.tw_accessories_1.setItem(self.tw_accessories_1.rowCount() - 1, 3, item)

            all_value_out += value["value_out"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["value_out"], 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_1.setItem(self.tw_accessories_1.rowCount() - 1, 4, item)

            all_sum_out += value["sum_out"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["sum_out"], 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_1.setItem(self.tw_accessories_1.rowCount() - 1, 5, item)

        else:
            self.tw_accessories_1.insertRow(self.tw_accessories_1.rowCount())

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_value_in, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_1.setItem(self.tw_accessories_1.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_in, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_1.setItem(self.tw_accessories_1.rowCount() - 1, 2, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_value_out, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_1.setItem(self.tw_accessories_1.rowCount() - 1, 4, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_out, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_1.setItem(self.tw_accessories_1.rowCount() - 1, 5, item)

            self.le_supply_value_accessories.setText(str(round(all_value_in, 2)))
            self.le_supply_sum_accessories.setText(str(round(all_sum_in, 2)))
            self.le_consumption_value_accessories.setText(str(round(all_value_out, 2)))
            self.le_consumption_sum_accessories.setText(str(round(all_sum_out, 2)))

            self.le_supply_sum_accessories_total.setText(str(round(all_sum_in, 2)))
            self.le_consumption_sum_accessories_total.setText(str(round(all_sum_out, 2)))

        # Таблица 2
        # Заполним подробный расход
        self.tw_accessories_2.clearContents()
        self.tw_accessories_2.setRowCount(0)

        query = """SELECT Note, SUM(transaction_records_accessories.Balance), SUM(transaction_records_accessories.Balance * accessories_supplyposition.Price)
                      FROM transaction_records_accessories
                        LEFT JOIN accessories_balance ON transaction_records_accessories.Supply_Balance_Id = accessories_balance.Id
                        LEFT JOIN accessories_supplyposition ON accessories_balance.accessories_SupplyPositionId = accessories_supplyposition.Id
                      WHERE Code IN (220, 221, 222, 223, 224)
                        AND transaction_records_accessories.Pack_Accessories_Id IN (SELECT pack_accessories.Id
                                                                                      FROM pack_accessories LEFT JOIN pack ON pack_accessories.Pack_Id = pack.Id
                                                                                        LEFT JOIN cut ON pack.Cut_Id = cut.Id
                                                                                      WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)
                        GROUP BY Code"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на пачки", sql_info.msg, QMessageBox.Ok)
            return False

        all_info_value, all_info_sum = 0, 0

        sum_value, sum_sum = 0, 0
        self.tw_accessories_2.insertRow(self.tw_accessories_2.rowCount())
        self.tw_accessories_2.setSpan(self.tw_accessories_2.rowCount() - 1, 0, 1, 3)
        item = QTableWidgetItem("Пачки")
        item.setTextAlignment(Qt.AlignHCenter)
        self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 0, item)

        for i in sql_info:
            self.tw_accessories_2.insertRow(self.tw_accessories_2.rowCount())
            item = QTableWidgetItem(i[0])
            self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 0, item)

            sum_value += i[1] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[1] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 1, item)

            sum_sum += i[2] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 2, item)

        else:
            all_info_value += sum_value
            all_info_sum += sum_sum

            self.tw_accessories_2.insertRow(self.tw_accessories_2.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 2, item)
            
        query = """SELECT Note, SUM(transaction_records_accessories.Balance), SUM(transaction_records_accessories.Balance * accessories_supplyposition.Price)
               FROM transaction_records_accessories
                 LEFT JOIN accessories_balance ON transaction_records_accessories.Supply_Balance_Id = accessories_balance.Id
                 LEFT JOIN accessories_supplyposition ON accessories_balance.accessories_SupplyPositionId = accessories_supplyposition.Id
               WHERE Code NOT IN (240, 220, 221, 222, 223, 224, 210, 211)
                 AND transaction_records_accessories.Date >= %s AND transaction_records_accessories.Date <= DATE_FORMAT(%s,'%Y-%m-%d 23:59:59')
                 GROUP BY Code"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода прочего", sql_info.msg, QMessageBox.Ok)
            return False

        sum_value, sum_sum = 0, 0
        self.tw_accessories_2.insertRow(self.tw_accessories_2.rowCount())
        self.tw_accessories_2.setSpan(self.tw_accessories_2.rowCount() - 1, 0, 1, 3)
        item = QTableWidgetItem("Прочее")
        item.setTextAlignment(Qt.AlignHCenter)
        self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 0, item)

        for i in sql_info:
            self.tw_accessories_2.insertRow(self.tw_accessories_2.rowCount())
            item = QTableWidgetItem(i[0])
            self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 0, item)

            sum_value += i[1] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[1] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 1, item)

            sum_sum += i[2] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 2, item)

        else:
            all_info_value += sum_value
            all_info_sum += sum_sum

            self.tw_accessories_2.insertRow(self.tw_accessories_2.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 2, item)

        # Отобразим сумму
        self.tw_accessories_2.insertRow(self.tw_accessories_2.rowCount())
        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_info_value, 2)))
        item = QTableWidgetItem(text)
        self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_info_sum, 2)))
        item = QTableWidgetItem(text)
        self.tw_accessories_2.setItem(self.tw_accessories_2.rowCount() - 1, 2, item)

        # Таблица 3
        # Заполним таблицу расхода по транзакциям
        self.tw_accessories_3.clearContents()
        self.tw_accessories_3.setRowCount(0)

        query = """SELECT tra.Note, SUM(IF(tra.Date >= %s, tra.Balance, 0)), SUM(IF(tra.Date >= %s, tra.Balance * accessories_supplyposition.Price, 0)),
                         SUM(tra.Balance), SUM(tra.Balance * accessories_supplyposition.Price) AS sum_m
                      FROM transaction_records_accessories AS tra LEFT JOIN accessories_balance ON tra.Supply_Balance_Id = accessories_balance.Id
                        LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                        LEFT JOIN pack_accessories ON tra.Pack_Accessories_Id = pack_accessories.Id
                        LEFT JOIN pack ON pack_accessories.Pack_Id = pack.Id
                        LEFT JOIN cut ON pack.Cut_Id = cut.Id
                      WHERE cut.Date_Cut <= %s OR tra.Date <= DATE_FORMAT(%s,'%Y-%m-%d 23:59:59') 
                        or (tra.Supply_Balance_Id IN (SELECT accessories_balance.Id FROM accessories_supply 
                                                        LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.Accessories_SupplyId
                                                        LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.Accessories_SupplyPositionId
                                                      WHERE accessories_supply.Data <= %s) and tra.Code IN (210, 211, 240))
                      GROUP BY Code"""
        date = (self.de_date_from.date().toPyDate(), self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate(),
                self.de_date_to.date().toPyDate(), self.de_date_to.date().toPyDate())
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения транзакций", sql_info.msg, QMessageBox.Ok)
            return False

        all_transaction_value, all_transaction_sum, all_transaction_value_month, all_transaction_sum_month = 0, 0, 0, 0
        for transaction in sql_info:
            self.tw_accessories_3.insertRow(self.tw_accessories_3.rowCount())
            item = QTableWidgetItem(transaction[0])
            self.tw_accessories_3.setItem(self.tw_accessories_3.rowCount() - 1, 0, item)

            all_transaction_value_month += transaction[1] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(transaction[1] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_3.setItem(self.tw_accessories_3.rowCount() - 1, 1, item)

            all_transaction_sum_month += transaction[2] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(transaction[2] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_3.setItem(self.tw_accessories_3.rowCount() - 1, 2, item)

            all_transaction_value += transaction[3] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(transaction[3] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_3.setItem(self.tw_accessories_3.rowCount() - 1, 3, item)

            all_transaction_sum += transaction[4] or 0
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(transaction[4] or 0, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_3.setItem(self.tw_accessories_3.rowCount() - 1, 4, item)

        else:
            self.tw_accessories_3.insertRow(self.tw_accessories_3.rowCount())

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_transaction_value_month, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_3.setItem(self.tw_accessories_3.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_transaction_sum_month, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_3.setItem(self.tw_accessories_3.rowCount() - 1, 2, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_transaction_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_3.setItem(self.tw_accessories_3.rowCount() - 1, 3, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_transaction_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories_3.setItem(self.tw_accessories_3.rowCount() - 1, 4, item)

            self.le_transaction_balance_value_accessories.setText(str(round(all_transaction_value, 2)))
            self.le_transaction_balance_sum_accessories.setText(str(round(all_transaction_sum, 2)))

        balance_value = all_value_in + old_balance_value - -all_value_out
        balance_sum = all_sum_in + old_balance_sum - -all_sum_out

        self.le_new_balance_value_accessories.setText(str(round(balance_value, 2)))
        self.le_new_balance_sum_accessories.setText(str(round(balance_sum, 2)))

        difference_value = all_transaction_value - balance_value
        difference_sum = all_transaction_sum - balance_sum

        self.le_difference_value_accessories.setText(str(round(difference_value, 2)))
        self.le_difference_sum_accessories.setText(str(round(difference_sum, 2)))

        self.le_transaction_balance_accessories.setText(str(round(all_transaction_sum, 2)))

        if difference_sum > 0:
            self.le_adjustments_plus_accessories.setText(str(round(difference_sum, 2)))
        elif difference_sum < 0:
            self.le_adjustments_minus_accessories.setText(str(round(difference_sum, 2)))

    def print_accessories(self):
        up_html = """
          <table>
          <caption>#head#</caption>
          <tr> <th>Остаток прошлый кол-во</th><th>Приход кол-во</th><th>Расход кол-во</th><th>Остаток кол-во</th><th>Остаток транз. кол-во</th><th>Разница кол-во</th> </tr>
          <tr> <td>#le_last_balance_value#</td><td>#le_supply_value#</td><td>#le_consumption_value#</td><td>#le_new_balance_value#</td><td>#le_transaction_balance_value#</td><td>#le_difference_value#</td> </tr>
          
          <tr> <th>Остаток прошлый рублей</th><th>Приход рублей</th><th>Расход рублей</th><th>Остаток рублей</th><th>Остаток транз. рублей</th><th>Разница рублей</th> </tr>
          <tr> <td>#le_last_balance_sum#</td><td>#le_supply_sum#</td><td>#le_consumption_sum#</td><td>#le_new_balance_sum#</td><td>#le_transaction_balance_sum#</td><td>#le_difference_sum#</td> </tr>
          </table>"""

        head = "Отчет по фурнитуре %s - %s" % (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate))
        up_html = up_html.replace("#head#", head)
        up_html = up_html.replace("#le_last_balance_value#", self.le_last_balance_value_accessories.text())
        up_html = up_html.replace("#le_supply_value#", self.le_supply_value_accessories.text())
        up_html = up_html.replace("#le_consumption_value#", self.le_consumption_value_accessories.text())
        up_html = up_html.replace("#le_new_balance_value#", self.le_new_balance_value_accessories.text())
        up_html = up_html.replace("#le_transaction_balance_value#", self.le_transaction_balance_value_accessories.text())
        up_html = up_html.replace("#le_difference_value#", self.le_difference_value_accessories.text())

        up_html = up_html.replace("#le_last_balance_sum#", self.le_last_balance_sum_accessories.text())
        up_html = up_html.replace("#le_supply_sum#", self.le_supply_sum_accessories.text())
        up_html = up_html.replace("#le_consumption_sum#", self.le_consumption_sum_accessories.text())
        up_html = up_html.replace("#le_new_balance_sum#", self.le_new_balance_sum_accessories.text())
        up_html = up_html.replace("#le_transaction_balance_sum#", self.le_transaction_balance_sum_accessories.text())
        up_html = up_html.replace("#le_difference_sum#", self.le_difference_sum_accessories.text())

        html = table_to_html.tab_html(self.tw_accessories_1, table_head="Приход + расход (Живой)", up_template=up_html)
        html += '<div style="display: inline-block; width: 100%">'
        html += table_to_html.tab_html(self.tw_accessories_2, table_head="Подробный расход (Живой)")
        html += '</div> <div style="display: inline-block; width: 100%">'
        html += table_to_html.tab_html(self.tw_accessories_3, table_head="Суммы транзакций  (Живой + Неживой) за месяц / всего ДО этой даты")
        html += '</div>'
        self.print_class = print_qt.PrintHtml(self, html)

    def ui_accessories_save(self):
        query = """INSERT INTO report_all_accessories_save (Date_Save, Date_From, Date_To, Last_Balance_Value, Last_Balance_Sum, Supply_Value,
                                      Supply_Sum, Consumption_Value, Consumption_Sum, New_Balance_Value, New_Balance_Sum,
                                      Transaction_Balance_Value, Transaction_Balance_Sum, Difference_Value, Difference_Sum)
                      VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        parametrs = (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate(), self.le_last_balance_value_accessories.text(),
                     self.le_last_balance_sum_accessories.text(), self.le_supply_value_accessories.text(), self.le_supply_sum_accessories.text(),
                     self.le_consumption_value_accessories.text(), self.le_consumption_sum_accessories.text(), self.le_new_balance_value_accessories.text(),
                     self.le_new_balance_sum_accessories.text(), self.le_transaction_balance_value_accessories.text(),
                     self.le_transaction_balance_sum_accessories.text(), self.le_difference_value_accessories.text(), self.le_difference_sum_accessories.text())

        sql_info = my_sql.sql_change(query, parametrs)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql сохранения отчета!", sql_info.msg, QMessageBox.Ok)
            return False
        else:
            QMessageBox.information(self, "Сохранено", "Отчет успешно сохранен!", QMessageBox.Ok)

    def ui_view_save_report_accessories(self):
        self.save_date_window = SaveReportMaterial("фурнитура")
        self.save_date_window.setModal(True)
        self.save_date_window.show()

        if self.save_date_window.exec_() != 1:
            return False

        self.le_last_balance_value_accessories.setText(str(self.save_date_window.balance_value))
        self.le_last_balance_sum_accessories.setText(str(self.save_date_window.balance_sum))

    # Расчет прочих расходов

    def calc_comparing(self):
        filter_date = (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate())

        self.tw_comparing_1.clearContents()
        self.tw_comparing_1.setRowCount(0)

        # Получим расход на ткань
        query = """SELECT comparing_name.Name, SUM(comparing_supplyposition.Value), SUM(comparing_supplyposition.Value * comparing_supplyposition.Price)
                      FROM comparing_supplyposition
                        LEFT JOIN comparing_name ON comparing_supplyposition.Comparing_NameId = comparing_name.Id
                        LEFT JOIN material_supply ON comparing_supplyposition.Material_SupplyId = material_supply.Id
                      WHERE comparing_supplyposition.Accessories_SupplyId IS NULL
                            AND material_supply.Data BETWEEN %s AND %s
                      GROUP BY comparing_name.Id"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение расходов на ткань", sql_info.msg, QMessageBox.Ok)
            return False

        all_sum_material, all_value_material = 0, 0

        for com in sql_info:
            self.tw_comparing_1.insertRow(self.tw_comparing_1.rowCount())

            item = QTableWidgetItem(str(com[0]))
            self.tw_comparing_1.setItem(self.tw_comparing_1.rowCount() - 1, 0, item)

            all_value_material += com[1]
            item = QTableWidgetItem(str(com[1]))
            self.tw_comparing_1.setItem(self.tw_comparing_1.rowCount() - 1, 1, item)

            all_sum_material += com[2]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(com[2], 2)))
            item = QTableWidgetItem(text)
            self.tw_comparing_1.setItem(self.tw_comparing_1.rowCount() - 1, 2, item)

        else:

            self.tw_comparing_1.insertRow(self.tw_comparing_1.rowCount())

            item = QTableWidgetItem(str(all_value_material))
            self.tw_comparing_1.setItem(self.tw_comparing_1.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_material, 2)))
            item = QTableWidgetItem(text)
            self.tw_comparing_1.setItem(self.tw_comparing_1.rowCount() - 1, 2, item)

            self.le_comparing_material.setText(str(round(all_sum_material, 2)))

        # Получим расходы на фурнитуру
        self.tw_comparing_2.clearContents()
        self.tw_comparing_2.setRowCount(0)

        # Получим расход на ткань
        query = """SELECT comparing_name.Name, SUM(comparing_supplyposition.Value), SUM(comparing_supplyposition.Value * comparing_supplyposition.Price)
                      FROM comparing_supplyposition
                        LEFT JOIN comparing_name ON comparing_supplyposition.Comparing_NameId = comparing_name.Id
                        LEFT JOIN accessories_supply ON comparing_supplyposition.accessories_SupplyId = accessories_supply.Id
                      WHERE comparing_supplyposition.Accessories_SupplyId IS NULL
                            AND accessories_supply.Data BETWEEN %s AND %s
                      GROUP BY comparing_name.Id"""
        sql_info = my_sql.sql_select(query, filter_date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получение расходов на фурнитуру", sql_info.msg, QMessageBox.Ok)
            return False

        all_sum_accessories, all_value_accessories = 0, 0

        for com in sql_info:
            self.tw_comparing_2.insertRow(self.tw_comparing_2.rowCount())

            item = QTableWidgetItem(str(com[0]))
            self.tw_comparing_2.setItem(self.tw_comparing_2.rowCount() - 1, 0, item)

            all_value_accessories += com[1]
            item = QTableWidgetItem(str(com[1]))
            self.tw_comparing_2.setItem(self.tw_comparing_2.rowCount() - 1, 1, item)

            all_sum_accessories += com[2]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(com[2], 2)))
            item = QTableWidgetItem(text)
            self.tw_comparing_2.setItem(self.tw_comparing_2.rowCount() - 1, 2, item)

        else:

            self.tw_comparing_2.insertRow(self.tw_comparing_2.rowCount())

            item = QTableWidgetItem(str(all_value_accessories))
            self.tw_comparing_2.setItem(self.tw_comparing_2.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_accessories, 2)))
            item = QTableWidgetItem(text)
            self.tw_comparing_2.setItem(self.tw_comparing_2.rowCount() - 1, 2, item)

            self.le_comparing_accessories.setText(str(round(all_sum_accessories, 2)))

        self.le_comparing_sum.setText(str(all_sum_accessories + all_sum_material))

    def print_comparing(self):
        up_html = """
          <table>
          <caption>#head#</caption>
          <tr> <th>Сусса расходаов</th> </tr>
          <tr> <td>#le_comparing_sum#</td> </tr>
          </table>"""

        head = "Отчет по прочим расходам %s - %s" % (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate))
        up_html = up_html.replace("#head#", head)
        up_html = up_html.replace("#le_comparing_sum#", self.le_comparing_sum.text())

        html = table_to_html.tab_html(self.tw_comparing_1, table_head="Расход на ткань",  up_template=up_html)
        html += table_to_html.tab_html(self.tw_comparing_2, table_head="Расход на фурнитуру")

        self.print_class = print_qt.PrintHtml(self, html)

    def ui_comparing_save(self):
        query = """INSERT INTO report_all_comparing_save (Date_Save, Date_From, Date_To, Comparing_Material, Comparing_Accessories, Comparing_Sum)
                    VALUES (NOW(), %s, %s, %s, %s, %s)"""

        parametrs = (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate(),
                     self.le_comparing_material.text(), self.le_comparing_accessories.text(), self.le_comparing_sum.text())

        sql_info = my_sql.sql_change(query, parametrs)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql сохранения отчета!", sql_info.msg, QMessageBox.Ok)
            return False
        else:
            QMessageBox.information(self, "Сохранено", "Отчет успешно сохранен!", QMessageBox.Ok)

    # Расчет продукции
    def calc_production(self):
        try:
            old_balance_value = Decimal(self.le_last_balance_value_article.text().replace(",", "."))
            old_balance_sum = Decimal(self.le_last_balance_sum_article.text().replace(",", "."))
        except:
            QMessageBox.critical(self, "Ошибка баланса", "Что то не так с балансом! Не могу его получить!\nПроверьте следующую вкладку", QMessageBox.Ok)
            return False

        self.le_old_balance_article_total.setText(str(old_balance_sum))

        self.tw_product_1.clearContents()
        self.tw_product_1.setRowCount(0)

        article_list = {}

        # Получим произведеные артикула
        query = """SELECT product_article_parametrs.Id, CONCAT(product_article.Article, '(', product_article_size.Size, ')[', product_article_parametrs.Name, ']'),
                        SUM(pack.Value_Pieces - pack.Value_Damage), product_article_parametrs.Price
                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s AND product_article_parametrs.Id IS NOT NULL 
                      GROUP BY product_article_parametrs.Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения покроеных пачек", sql_info.msg, QMessageBox.Ok)
            return False

        for order_position in sql_info:
            if article_list.get(order_position[0]) is None:
                new = {order_position[0]: {"name": order_position[1], "seb": 0, "value_in": order_position[2], "sum_in": 0,
                                           "value_out": 0, "sum_out": 0, "profit": 0, "seb_out": 0, "price": order_position[3]}}
                article_list.update(new)

        # Получим проданые артикула
        query = """ SELECT product_article_parametrs.Id, CONCAT(product_article.Article, '(', product_article_size.Size, ')[', product_article_parametrs.Name, ']'),
                        order_position.Value, IF(clients.No_Nds, order_position.Price * (order_position.NDS / 100 + 1), order_position.Price), product_article_parametrs.Price
                      FROM order_position LEFT JOIN `order` ON order_position.Order_Id = `order`.Id
                        LEFT JOIN clients ON `order`.Client_Id = clients.Id
                        LEFT JOIN product_article_parametrs ON order_position.Product_Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE `order`.Date_Shipment >= %s AND `order`.Date_Shipment <= %s """
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения проданых позиций", sql_info.msg, QMessageBox.Ok)
            return False

        for order_position in sql_info:
            if article_list.get(order_position[0]) is None:
                new = {order_position[0]: {"name": order_position[1], "seb": 0, "value_in": 0, "sum_in": 0, "price": order_position[4],
                                           "value_out": order_position[2], "sum_out": order_position[3] * order_position[2], "profit": 0, "seb_out": 0}}
                article_list.update(new)
            else:
                article_list[order_position[0]]["value_out"] += order_position[2]
                article_list[order_position[0]]["sum_out"] += order_position[3] * order_position[2]

        # Найдем себестоимость

        all_value_in, all_sum_in, all_value_out, all_sum_out, all_profit, all_seb_out, all_sun_sel_in = 0, 0, 0, 0, 0, 0, 0

        for key, value in article_list.items():

            self.statusBar.showMessage("Расчет артикула (таблица 1) %s" % value["name"])

            # Возьмем то количество которое бвльше (Проданого или пороеного)
            if value["value_out"] > value["value_in"]:
                val_sql = value["value_out"]
            else:
                val_sql = value["value_in"]

            query = """SELECT pack.Id FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id JOIN (SELECT @sum := 0) t
                          WHERE pack.Article_Parametr_Id = %s AND cut.Date_Cut <= %s AND (@sum := @sum + pack.Value_Pieces) <= %s"""
            sql_pack_id_info = my_sql.sql_select(query, (key, self.de_date_to.date().toPyDate(), val_sql + 200))
            if "mysql.connector.errors" in str(type(sql_pack_id_info)):
                QMessageBox.critical(self, "Ошибка sql получения id пачек для подсчета себестоимости", sql_pack_id_info.msg, QMessageBox.Ok)
                return False

            v = int(len(sql_pack_id_info)/5) + 1

            sebest_pack_list = []
            if sql_pack_id_info:  # Если найдены предыдущие кроя! (Если нет то возьмем расчетную себестоимость из артикула)
                for i in range(len(sql_pack_id_info)):
                    if i % v != 0:
                        continue

                    pack_id = sql_pack_id_info[i][0]
                    # Узнаем всю себестоимость
                    query = """SELECT(
                                      SELECT AVG(DISTINCT material_supplyposition.Price) * (SELECT (pack.Weight * (1 + cut.Rest_Percent / 100)) / pack.Value_Pieces
                                                                                            FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
                                                                                            WHERE pack.Id = pm.Id)
                                      FROM pack LEFT JOIN transaction_records_material ON transaction_records_material.Cut_Material_Id = pack.Cut_Id
                                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                      WHERE pack.Id = pm.Id AND transaction_records_material.Note NOT LIKE '%доп. тк%'
                                      ),(
                                          SELECT SUM(((pack_add_material.Weight + pack_add_material.Weight_Rest) / pack.Value_Pieces) * pack_add_material.Price)
                                            FROM pack_add_material LEFT JOIN pack ON pack_add_material.Pack_Id = pack.Id
                                            WHERE pack.Id = pm.Id
                                      ),(
                                          SELECT SUM(avg) FROM (
                                            SELECT AVG(accessories_supplyposition.Price) * pack_accessories.Value_Thing AS avg
                                            FROM pack
                                              LEFT JOIN pack_accessories ON pack.Id = pack_accessories.Pack_Id
                                              LEFT JOIN transaction_records_accessories ON transaction_records_accessories.Pack_Accessories_Id = pack_accessories.Id
                                              LEFT JOIN accessories_balance ON transaction_records_accessories.Supply_Balance_Id = accessories_balance.Id
                                              LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                                            WHERE pack.Id = %s
                                            GROUP BY pack_accessories.Id) t
                                      ),(
                                          SELECT SUM(pack_operation.Price) FROM pack_operation WHERE pack_operation.Pack_Id = pm.Id
                                )
                                FROM pack as pm WHERE pm.Id = %s"""
                    sql_info = my_sql.sql_select(query, (pack_id, pack_id))
                    if "mysql.connector.errors" in str(type(sql_info)):
                        QMessageBox.critical(self, "Ошибка sql получения средней себестоимости", sql_info.msg, QMessageBox.Ok)
                        print(pack_id)
                        return False

                    sebest_pack_list.append(sum([0 if i is None else i for i in sql_info[0]]))

                # Находим среднюю себестоимость на артикул
                if sebest_pack_list:
                    value["seb"] = sum(sebest_pack_list) / len(sebest_pack_list)

            else:  # Если нет прошлых краев, то возьмем расчетную себестоимость
                # Узнаем всю расчетную себестоимость
                query = """SELECT (
                                      SELECT SUM(operations.Price)
                                        FROM product_article_operation LEFT JOIN operations ON product_article_operation.Operation_Id = operations.Id
                                        WHERE product_article_operation.Product_Article_Parametrs_Id = pr.Id
                                  ),(
                                      SELECT SUM(s)
                                      FROM (SELECT material_supplyposition.Price * product_article_material.Value AS s
                                              FROM product_article_material
                                                LEFT JOIN material_supplyposition ON product_article_material.Material_Id = material_supplyposition.Material_NameId
                                                LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                                LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                                              WHERE product_article_material.Product_Article_Parametrs_Id = %s AND product_article_material.Material_Id IS NOT NULL
                                                AND material_balance.BalanceWeight > 0
                                              GROUP BY product_article_material.Material_Id) t
                                  ),(
                                      SELECT SUM(s)
                                      FROM (SELECT accessories_supplyposition.Price * product_article_material.Value AS s
                                              FROM product_article_material
                                                LEFT JOIN accessories_supplyposition ON product_article_material.Accessories_Id = accessories_supplyposition.Accessories_NameId
                                                LEFT JOIN accessories_supply ON accessories_supplyposition.Accessories_SupplyId = accessories_supply.Id
                                                LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.Accessories_SupplyPositionId
                                              WHERE product_article_material.Product_Article_Parametrs_Id = %s AND product_article_material.Accessories_Id IS NOT NULL
                                                    AND accessories_balance.BalanceValue > 0
                                              GROUP BY product_article_material.Accessories_Id) t
                                  )
                              FROM product_article_parametrs AS pr WHERE pr.Id = %s"""
                sql_info = my_sql.sql_select(query, (key, key, key))
                if "mysql.connector.errors" in str(type(sql_info)):
                    QMessageBox.critical(self, "Ошибка sql получения расчетной себестоимости", sql_info.msg, QMessageBox.Ok)
                    return False

                # Считаем себестоимость
                if sql_info[0][0]:
                    article_list[key]["seb"] = sql_info[0][0] + sql_info[0][1] + sql_info[0][2]
                    article_list[key]["name"] = "Б/К " + article_list[key]["name"]

            # посчитаем весь артикул
            value["sum_in"] = value["value_in"] * value["seb"]
            value["profit"] = value["sum_out"] - (value["value_out"] * value["seb"])
            value["seb_out"] += value["value_out"] * value["seb"]

            all_sun_sel_in += value["value_in"] * value["price"]  # Считаем сколько покроили в рублях на продажу

            # Вставим артикул

            self.tw_product_1.insertRow(self.tw_product_1.rowCount())

            item = QTableWidgetItem(str(value["name"]))
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 0, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["seb"], 2)))
            item = QTableWidgetItem(str(text))
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 1, item)

            all_value_in += value["value_in"]
            item = QTableWidgetItem(str(value["value_in"]))
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 2, item)

            all_sum_in += value["sum_in"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["sum_in"], 2)))
            item = QTableWidgetItem(text)
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 3, item)

            all_value_out += value["value_out"]
            item = QTableWidgetItem(str(value["value_out"]))
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 4, item)

            all_seb_out += value["seb_out"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["seb_out"], 2)))
            item = QTableWidgetItem(text)
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 5, item)

            all_sum_out += value["sum_out"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["sum_out"], 2)))
            item = QTableWidgetItem(text)
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 6, item)

            all_profit += value["profit"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value["profit"], 2)))
            item = QTableWidgetItem(text)
            if value["profit"] > 0:
                color = QBrush(QColor(150, 255, 161, 255))
            else:
                color = QBrush(QColor(255, 255, 153, 255))

            item.setBackground(color)
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 7, item)

        else:

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_value_in, 2)))
            item = QTableWidgetItem(text)
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 2, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_in, 2)))
            item = QTableWidgetItem(text)
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 3, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_value_out, 2)))
            item = QTableWidgetItem(text)
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 4, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_seb_out, 2)))
            item = QTableWidgetItem(text)
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 5, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_out, 2)))
            item = QTableWidgetItem(text)
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 6, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_profit, 2)))
            item = QTableWidgetItem(text)
            self.tw_product_1.setItem(self.tw_product_1.rowCount() - 1, 7, item)

            self.le_supply_value_article.setText(str(all_value_in))
            self.le_supply_sum_seb_article.setText(str(round(all_sum_in, 2)))
            self.le_supply_sum_price_article.setText(str(round(all_sun_sel_in, 2)))
            self.le_supply_sum_balance_article.setText(str(round(all_sun_sel_in - all_sum_in, 2)))

            self.le_supply_sum_seb_article_total.setText(str(round(all_sum_in, 2)))

            self.le_sel_value_article.setText(str(all_value_out))

        # Заполним таблицу отгруженого клиенту
        self.tw_product_2.clearContents()
        self.tw_product_2.setRowCount(0)

        query = """SELECT clients.Id, clients.Name, `order`.Number_Doc, `order`.Number_Order, `order`.Date_Shipment,
                         `order`.Sum_Off_Nds, `order`.Sum_In_Nds, SUM(order_position.Value)
                      FROM `order` LEFT JOIN order_position ON `order`.Id = order_position.Order_Id
                        LEFT JOIN clients ON `order`.Client_Id = clients.Id
                      WHERE `order`.Date_Shipment >= %s AND `order`.Date_Shipment <= %s AND `order`.Shipped = 1 GROUP BY `order`.Id ORDER BY clients.Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения отгруженных зказов", sql_info.msg, QMessageBox.Ok)
            return False

        sum_off_nds, sum_in_nds, sum_value = 0, 0, 0
        all_sum_off_nds, all_sum_in_nds, all_sum_value = 0, 0, 0
        old_client_id = None
        for order in sql_info:

            if order[0] != old_client_id:  # Если новый клиент не равен предыдущемо делаем подсчет!

                if old_client_id is None:  # Если это первая итерация то просто белем ID клиента и мдем дальше!
                    old_client_id = order[0]

                else:
                    all_sum_off_nds += sum_off_nds
                    all_sum_in_nds += sum_in_nds
                    all_sum_value += sum_value

                    self.tw_product_2.insertRow(self.tw_product_2.rowCount())
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_off_nds, 2)))
                    item = QTableWidgetItem(text)
                    item.setData(5, order[0])
                    self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 4, item)

                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_in_nds, 2)))
                    item = QTableWidgetItem(text)
                    item.setData(5, order[0])
                    self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 5, item)

                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sum_value))
                    item = QTableWidgetItem(text)
                    item.setData(5, order[0])
                    self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 6, item)

                    sum_off_nds, sum_in_nds, sum_value = 0, 0, 0
                    old_client_id = order[0]

            self.tw_product_2.insertRow(self.tw_product_2.rowCount())

            item = QTableWidgetItem(order[1])
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 0, item)

            item = QTableWidgetItem(str(order[2]))
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 1, item)

            item = QTableWidgetItem(str(order[3]))
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 2, item)

            item = QTableWidgetItem(order[4].strftime("%d.%m.%Y"))
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 3, item)

            sum_off_nds += order[5]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(order[5], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 4, item)

            sum_in_nds += order[6]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(order[6], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 5, item)

            sum_value += order[7]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(order[7]))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 6, item)

        else:
            # Вставляем сумму для последнего клиента
            all_sum_off_nds += sum_off_nds
            all_sum_in_nds += sum_in_nds
            all_sum_value += sum_value

            self.tw_product_2.insertRow(self.tw_product_2.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_off_nds, 2)))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 4, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sum_in_nds, 2)))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 5, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sum_value))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 6, item)

            # Вставляем итоговоую сумму
            self.tw_product_2.insertRow(self.tw_product_2.rowCount())
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_sum_off_nds))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 4, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_sum_in_nds))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 5, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_sum_value))
            item = QTableWidgetItem(text)
            item.setData(5, order[0])
            self.tw_product_2.setItem(self.tw_product_2.rowCount() - 1, 6, item)

            self.le_sel_sum_price_article.setText(str(round(all_sum_in_nds, 2)))
            self.le_sel_sum_seb_article.setText(str(round(all_seb_out, 2)))
            self.le_sel_sum_balance_article.setText(str(round(all_sum_in_nds - all_seb_out, 2)))

            self.le_sel_sum_price_article_total.setText(str(round(all_sum_in_nds, 2)))
            self.le_sel_sum_seb_article_total.setText(str(round(all_seb_out, 2)))

            warehouse1_value = (old_balance_value + all_value_in) - all_value_out
            warehouse1_sum = (old_balance_sum + all_sum_in) - all_seb_out
            self.le_warehouse1_value_article.setText(str(round(warehouse1_value, 2)))
            self.le_warehouse1_sum_article.setText(str(round(warehouse1_sum, 2)))

        # Получим остаток склада
        # Получаем артикула
        self.tw_product_3.clearContents()
        self.tw_product_3.setRowCount(0)

        article_list = {}

        query = """SELECT product_article_parametrs.Id, CONCAT(product_article.Article, '(', product_article_size.Size, ')[', product_article_parametrs.Name, ']'),
                        product_article_parametrs.Price,
                        war.Value_In_Warehouse - IFNULL((SELECT SUM(transaction_records_warehouse.Balance) FROM transaction_records_warehouse
                                                          WHERE transaction_records_warehouse.Article_Parametr_Id = war.Id_Article_Parametr
                                                            AND transaction_records_warehouse.Date > %s), 0)
                      FROM product_article_warehouse AS war
                        LEFT JOIN product_article_parametrs ON war.Id_Article_Parametr = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_to.date().toPyDate(), ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения артикулов склада", sql_info.msg, QMessageBox.Ok)
            return False

        # добавляем артикула в словарь
        for article in sql_info:
            article_list.update({article[0]: {"warehouse_value": article[3], "cut_value": 0, "seb": None, "price": article[2], "name": article[1]}})

        # Смотрим сколько еще артикулов было в цеху на эту дату
        query = """SELECT product_article_parametrs.Id, SUM(pack.Value_Pieces)
                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                      LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                      WHERE cut.Date_Cut <= %s AND (pack.Date_Make > %s OR pack.Date_Make IS NULL) GROUP BY product_article_parametrs.Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_to.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения артикулов в цеху", sql_info.msg, QMessageBox.Ok)
            return False

        for article in sql_info:
            if article[0]:
                article_list[article[0]]["cut_value"] = article[1]
            else:
                continue

        # Считаем себестоимость
        all_warehouse, all_warehouse_seb, all_warehouse_price = 0, 0, 0
        all_cut, all_cut_seb, all_cut_price = 0, 0, 0
        for key, value in article_list.items():

            self.statusBar.showMessage("Расчет артикула (таблица 3) %s" % article_list[key]["name"])

            if article_list[key]["warehouse_value"] == 0 and article_list[key]["cut_value"] == 0:
                continue

            query = """SELECT (
                                  SELECT SUM(operations.Price)
                                    FROM product_article_operation LEFT JOIN operations ON product_article_operation.Operation_Id = operations.Id
                                    WHERE product_article_operation.Product_Article_Parametrs_Id = pr.Id
                              ),(
                                  SELECT SUM(s)
                                  FROM (SELECT material_supplyposition.Price * product_article_material.Value AS s
                                          FROM product_article_material
                                            LEFT JOIN material_supplyposition ON product_article_material.Material_Id = material_supplyposition.Material_NameId
                                            LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                                            LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                                          WHERE product_article_material.Product_Article_Parametrs_Id = %s AND product_article_material.Material_Id IS NOT NULL
                                            AND material_balance.BalanceWeight > 0
                                          GROUP BY product_article_material.Material_Id) t
                              ),(
                                  SELECT SUM(s)
                                  FROM (SELECT accessories_supplyposition.Price * product_article_material.Value AS s
                                          FROM product_article_material
                                            LEFT JOIN accessories_supplyposition ON product_article_material.Accessories_Id = accessories_supplyposition.Accessories_NameId
                                            LEFT JOIN accessories_supply ON accessories_supplyposition.Accessories_SupplyId = accessories_supply.Id
                                            LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.Accessories_SupplyPositionId
                                          WHERE product_article_material.Product_Article_Parametrs_Id = %s AND product_article_material.Accessories_Id IS NOT NULL
                                                AND accessories_balance.BalanceValue > 0
                                          GROUP BY product_article_material.Accessories_Id) t
                              )
                          FROM product_article_parametrs AS pr WHERE pr.Id = %s"""
            sql_info = my_sql.sql_select(query, (key, key, key))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения расчетной себестоимости", sql_info.msg, QMessageBox.Ok)
                return False

            if sql_info[0][0]:
                article_list[key]["seb"] = sql_info[0][0] + sql_info[0][1] + sql_info[0][2]
            else:
                article_list[key]["seb"] = 0

            # Вставляем расчитаный артикул
            self.tw_product_3.insertRow(self.tw_product_3.rowCount())

            seb = article_list[key]["seb"]
            price = article_list[key]["price"]

            item = QTableWidgetItem(article_list[key]["name"])
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 0, item)

            item = QTableWidgetItem(str(round(seb, 4)))
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 1, item)

            item = QTableWidgetItem(str(price))
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 2, item)

            all_warehouse += article_list[key]["warehouse_value"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(article_list[key]["warehouse_value"]))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 3, item)

            all_warehouse_price += article_list[key]["warehouse_value"] * price
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["warehouse_value"] * price, 4)))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 4, item)

            all_warehouse_seb += article_list[key]["warehouse_value"] * seb
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["warehouse_value"] * seb, 4)))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 5, item)

            all_cut += article_list[key]["cut_value"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(article_list[key]["cut_value"]))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 6, item)

            all_cut_price += article_list[key]["cut_value"] * price
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["cut_value"] * price, 4)))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 7, item)

            all_cut_seb += article_list[key]["cut_value"] * seb
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["cut_value"] * seb, 4)))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 8, item)

        else:
            self.tw_product_3.insertRow(self.tw_product_3.rowCount())

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_warehouse))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 3, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_warehouse_price, 4)))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 4, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_warehouse_seb, 4)))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 5, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_cut))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 6, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_cut_price, 4)))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 7, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_cut_seb, 4)))
            item = QTableWidgetItem(text)
            self.tw_product_3.setItem(self.tw_product_3.rowCount() - 1, 8, item)

            warehouse2_value = all_warehouse + all_cut
            warehouse2_sum = all_cut_seb + all_warehouse_seb

            self.le_warehouse2_value_article.setText(str(warehouse2_value))
            self.le_warehouse2_sum_article.setText(str(round(warehouse2_sum, 2)))

            self.le_warehouse2_sum_article_total.setText(str(round(warehouse2_sum, 2)))

            self.le_difference_warehouse_value.setText(str(warehouse2_value - warehouse1_value))
            self.le_difference_warehouse_sum.setText(str(round(warehouse2_sum - warehouse1_sum, 2)))



        # Получим суммы транзакций по групам
        query = """SELECT Note, SUM(Balance) FROM transaction_records_warehouse WHERE Date >= %s AND Date <= %s GROUP BY Code"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения суммы транзкций по групам", sql_info.msg, QMessageBox.Ok)
            return False

        all_transaction = 0

        self.tw_product_4.clearContents()
        self.tw_product_4.setRowCount(0)

        for trans in sql_info:
            self.tw_product_4.insertRow(self.tw_product_4.rowCount())

            item = QTableWidgetItem(trans[0])
            self.tw_product_4.setItem(self.tw_product_4.rowCount() - 1, 0, item)

            all_transaction += trans[1]
            item = QTableWidgetItem(str(trans[1]))
            self.tw_product_4.setItem(self.tw_product_4.rowCount() - 1, 1, item)

        else:
            self.tw_product_4.insertRow(self.tw_product_4.rowCount())
            item = QTableWidgetItem(str(all_transaction))
            self.tw_product_4.setItem(self.tw_product_4.rowCount() - 1, 1, item)

    def print_production(self):
        up_html = """
          <table>
          <caption>#head#</caption>
          <tr> <th>Произвели шт.</th> <th>Произвели по себест</th><th>Произвели по продаже</th><th>Прибыль прогнозируемая</th> </tr>
          <tr> <td>#le_supply_value_article#</td><td>#le_supply_sum_seb_article#</td><td>#le_supply_sum_price_article#</td><td>#le_supply_sum_balance_article#</td> </tr>
          
          <tr> <th>Продали шт.</th> <th>Продали по продажно</th><th>Продали по себест</th><th>Прибыль</th> </tr>
          <tr> <td>#le_sel_value_article#</td><td>#le_sel_sum_price_article#</td><td>#le_sel_sum_seb_article#</td><td>#le_sel_sum_balance_article#</td> </tr>
          </table>
          <table>       
          <tr> <th> </th> <th>Остаток штук</th> <th>Остаток рублей</th> </tr>
          <tr> <th>Прошлый</th><td>#le_last_balance_value_article#</td><td>#le_last_balance_sum_article#</td> </tr>
          <tr> <th>Живой</th><td>#le_warehouse1_value_article#</td><td>#le_warehouse1_sum_article#</td> </tr>
          <tr> <th>Не живой</th><td>#le_warehouse2_value_article#</td><td>#le_warehouse2_sum_article#</td> </tr>
          <tr> <th>Разница</th><td>#le_difference_warehouse_value#</td><td>#le_difference_warehouse_sum#</td> </tr>
          </table>"""

        head = "Отчет по продукции %s - %s" % (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate))
        up_html = up_html.replace("#head#", head)

        up_html = up_html.replace("#le_supply_value_article#", self.le_supply_value_article.text())
        up_html = up_html.replace("#le_supply_sum_seb_article#", self.le_supply_sum_seb_article.text())
        up_html = up_html.replace("#le_supply_sum_price_article#", self.le_supply_sum_price_article.text())
        up_html = up_html.replace("#le_supply_sum_balance_article#", self.le_supply_sum_balance_article.text())

        up_html = up_html.replace("#le_sel_value_article#", self.le_sel_value_article.text())
        up_html = up_html.replace("#le_sel_sum_price_article#", self.le_sel_sum_price_article.text())
        up_html = up_html.replace("#le_sel_sum_seb_article#", self.le_sel_sum_seb_article.text())
        up_html = up_html.replace("#le_sel_sum_balance_article#", self.le_sel_sum_balance_article.text())

        up_html = up_html.replace("#le_last_balance_value_article#", self.le_last_balance_value_article.text())
        up_html = up_html.replace("#le_last_balance_sum_article#", self.le_last_balance_sum_article.text())
        up_html = up_html.replace("#le_warehouse1_value_article#", self.le_warehouse1_value_article.text())
        up_html = up_html.replace("#le_warehouse1_sum_article#", self.le_warehouse1_sum_article.text())
        up_html = up_html.replace("#le_warehouse2_value_article#", self.le_warehouse2_value_article.text())
        up_html = up_html.replace("#le_warehouse2_sum_article#", self.le_warehouse2_sum_article.text())
        up_html = up_html.replace("#le_difference_warehouse_value#", self.le_difference_warehouse_value.text())
        up_html = up_html.replace("#le_difference_warehouse_sum#", self.le_difference_warehouse_sum.text())

        html = table_to_html.tab_html(self.tw_product_1, table_head="Произведено / Продано (Себестоимость покроеная!)",  up_template=up_html)
        html += '<div style="display: inline-block; width: 100%">'
        html += table_to_html.tab_html(self.tw_product_2, table_head="Отгружено клиенту")
        html += '</div> <div style="display: inline-block; width: 100%">'
        html += table_to_html.tab_html(self.tw_product_3, table_head="Остаток склада (Себестоимость расчетная!)")
        html += '</div> <div style="display: inline-block; width: 100%">'
        html += table_to_html.tab_html(self.tw_product_4, table_head="Изменения по транзпкциям")
        html += '</div>'

        self.print_class = print_qt.PrintHtml(self, html)

    def ui_product_save(self):
        query = """INSERT INTO report_all_article_save (Date_Save, Date_From, Date_To, Last_Balance_Value_Article, Last_Balance_Sum_Article,
                                                        Supply_Value_Article, Supply_Sum_Seb_Article,
                                                        Supply_Sum_Price_Article, Supply_Sum_Balance_Article, Sel_Value_Article,
                                                        Sel_Sum_Price_Article, Sel_Sum_Seb_Article, Sel_Sum_Balance_Article,
                                                        Warehouse1_Value_Article, Warehouse1_Sum_Article, Warehouse2_Value_Article,
                                                        Warehouse2_Sum_Article, Difference_Warehouse_Value, Difference_Warehouse_Sum)
                      VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        parametrs = (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate(), self.le_last_balance_value_article.text(),
                     self.le_last_balance_sum_article.text(), self.le_supply_value_article.text(),
                     self.le_supply_sum_seb_article.text(), self.le_supply_sum_price_article.text(), self.le_supply_sum_balance_article.text(),
                     self.le_sel_value_article.text(), self.le_sel_sum_price_article.text(), self.le_sel_sum_seb_article.text(),
                     self.le_sel_sum_balance_article.text(), self.le_warehouse1_value_article.text(),
                     self.le_warehouse1_sum_article.text(), self.le_warehouse2_value_article.text(), self.le_warehouse2_sum_article.text(),
                     self.le_difference_warehouse_value.text(), self.le_difference_warehouse_sum.text())

        sql_info = my_sql.sql_change(query, parametrs)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql сохранения отчета!", sql_info.msg, QMessageBox.Ok)
            return False
        else:
            QMessageBox.information(self, "Сохранено", "Отчет успешно сохранен!", QMessageBox.Ok)

    def ui_view_save_report_product(self):
        self.save_date_window = SaveReportArticle()
        self.save_date_window.setModal(True)
        self.save_date_window.show()

        if self.save_date_window.exec_() != 1:
            return False

        self.le_last_balance_value_article.setText(str(self.save_date_window.balance_value))
        self.le_last_balance_sum_article.setText(str(self.save_date_window.balance_sum))

    # Расчет ИТОГО
    def calc_total(self):
        try:
            i1 = float(self.le_last_balance_material_total.text())
            i2 = float(self.le_last_balance_accessories_total.text())
            self.le_last_balance_total.setText(str(round(i1 + i2, 2)))

            i1 = float(self.le_supply_sum_material_total.text())
            i2 = float(self.le_supply_sum_accessories_total.text())
            self.le_supply_sum_total.setText(str(round(i1 + i2, 2)))

            i1 = float(self.le_adjustments_plus_material.text())
            i2 = float(self.le_adjustments_plus_accessories.text())
            self.le_adjustments_plus_total.setText(str(round(i1 + i2, 2)))

            i1 = float(self.le_consumption_sum_material_total.text())
            i2 = float(self.le_consumption_sum_accessories_total.text())
            self.le_consumption_sum_total.setText(str(round(i1 + i2, 2)))

            i1 = float(self.le_adjustments_minus_material.text())
            i2 = float(self.le_adjustments_minus_accessories.text())
            self.le_adjustments_minus_total.setText(str(round(i1 + i2, 2)))

            i1 = float(self.le_transaction_balance_material.text())
            i2 = float(self.le_transaction_balance_accessories.text())
            self.le_transaction_balance_total.setText(str(round(i1 + i2, 2)))
        except:
            QMessageBox.critical(self, "Ошибка подсчета", "Чего то не хватает в материалах", QMessageBox.Ok)
            return False

        try:
            i1 = float(self.le_sel_sum_price_article_total.text())
            i2 = float(self.le_sel_sum_seb_article_total.text())
            self.le_profit_article_total.setText(str(round(i1 - i2, 2)))

            i0 = float(self.le_old_balance_article_total.text())

            i1 = float(self.le_supply_sum_seb_article_total.text())
            i2 = float(self.le_profit_article_total.text())

            i3 = float(self.le_sel_sum_price_article_total.text())

            i4 = float(self.le_warehouse2_sum_article_total.text())

            ii = i4 - (i0 + i1 + i2) - i3

            if ii > 0:
                self.le_adjustments_plus_article_total.setText(str(round(ii, 2)))
            elif ii < 0:
                self.le_adjustments_minus_article_total.setText(str(round(ii, 2)))

        except:
            QMessageBox.critical(self, "Ошибка подсчета", "Чего то не хватает в продукции", QMessageBox.Ok)
            return False

    # Прошлые расчеты
    def view_save(self):

        self.tw_save_material.clearContents()
        self.tw_save_material.setRowCount(0)
        self.tw_save_accessories.clearContents()
        self.tw_save_accessories.setRowCount(0)
        self.tw_save_comparing.clearContents()
        self.tw_save_comparing.setRowCount(0)
        self.tw_save_product.clearContents()
        self.tw_save_product.setRowCount(0)


        query = """SELECT Id, Date_Save, Date_From, Date_To, Last_Balance_Value, Last_Balance_Sum, Supply_Value, Supply_Sum, Consumption_Value,
                        Consumption_Sum, New_Balance_Value, New_Balance_Sum, Transaction_Balance_Value, Transaction_Balance_Sum,
                        Difference_Value, Difference_Sum
                      FROM report_all_material_save"""

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения сохраненых данных ткани", sql_info.msg, QMessageBox.Ok)
            return False

        for table_typle in sql_info:
            self.tw_save_material.insertRow(self.tw_save_material.rowCount())

            for column in range(1, len(table_typle)):

                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(table_typle[column], 2)))
                    item = QTableWidgetItem(text)

                elif isinstance(table_typle[column], datetime.date):
                    date = QDate(table_typle[column].year, table_typle[column].month, table_typle[column].day)
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, date)

                else:
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, table_typle[column])

                item.setData(5, table_typle[0])
                self.tw_save_material.setItem(self.tw_save_material.rowCount() - 1, column - 1, item)

        query = """SELECT Id, Date_Save Date_From, Date_To, Last_Balance_Value, Last_Balance_Sum, Supply_Value, Supply_Sum, Consumption_Value,
                        Consumption_Sum, New_Balance_Value, New_Balance_Sum, Transaction_Balance_Value, Transaction_Balance_Sum,
                        Difference_Value, Difference_Sum
                      FROM report_all_accessories_save"""

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения сохраненых данных фурнитуры", sql_info.msg, QMessageBox.Ok)
            return False

        for table_typle in sql_info:
            self.tw_save_accessories.insertRow(self.tw_save_accessories.rowCount())

            for column in range(1, len(table_typle)):

                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(table_typle[column], 2)))
                    item = QTableWidgetItem(text)

                elif isinstance(table_typle[column], datetime.date):
                    date = QDate(table_typle[column].year, table_typle[column].month, table_typle[column].day)
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, date)

                else:
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, table_typle[column])

                item.setData(5, table_typle[0])
                self.tw_save_accessories.setItem(self.tw_save_accessories.rowCount() - 1, column - 1, item)

        query = """SELECT Id, Date_Save, Date_From, Date_To, Comparing_Material, Comparing_Accessories, Comparing_Sum
                      FROM report_all_comparing_save"""

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения сохраненых прочих растрат", sql_info.msg, QMessageBox.Ok)
            return False

        for table_typle in sql_info:
            self.tw_save_comparing.insertRow(self.tw_save_comparing.rowCount())

            for column in range(1, len(table_typle)):

                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(table_typle[column], 2)))
                    item = QTableWidgetItem(text)

                elif isinstance(table_typle[column], datetime.date):
                    date = QDate(table_typle[column].year, table_typle[column].month, table_typle[column].day)
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, date)

                else:
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, table_typle[column])

                item.setData(5, table_typle[0])
                self.tw_save_comparing.setItem(self.tw_save_comparing.rowCount() - 1, column - 1, item)

        query = """SELECT Id, Date_Save, Date_From, Date_To, Last_Balance_Value_Article, Last_Balance_Sum_Article, Supply_Value_Article,
                            Supply_Sum_Seb_Article, Supply_Sum_Price_Article, Supply_Sum_Balance_Article, Sel_Value_Article,
                            Sel_Sum_Price_Article, Sel_Sum_Seb_Article, Sel_Sum_Balance_Article, Warehouse1_Value_Article, Warehouse1_Sum_Article,
                            Warehouse2_Value_Article, Warehouse2_Sum_Article, Difference_Warehouse_Value, Difference_Warehouse_Sum
                      FROM report_all_article_save"""

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения сохраненых артикулов", sql_info.msg, QMessageBox.Ok)
            return False

        for table_typle in sql_info:
            self.tw_save_product.insertRow(self.tw_save_product.rowCount())

            for column in range(1, len(table_typle)):

                if isinstance(table_typle[column], Decimal):
                    text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(table_typle[column], 2)))
                    item = QTableWidgetItem(text)

                elif isinstance(table_typle[column], datetime.date):
                    date = QDate(table_typle[column].year, table_typle[column].month, table_typle[column].day)
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, date)

                else:
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, table_typle[column])

                item.setData(5, table_typle[0])
                self.tw_save_product.setItem(self.tw_save_product.rowCount() - 1, column - 1, item)

    def print_save(self):
        up_html = """
          <table>
          <caption>#head#</caption>
          </table>"""

        head = "Все отчеты"
        up_html = up_html.replace("#head#", head)

        html = table_to_html.tab_html(self.tw_save_material, table_head="Ткань", up_template=up_html)
        html += '<div style="display: inline-block; width: 100%">'
        html += table_to_html.tab_html(self.tw_save_accessories, table_head="Фурнитуры")
        html += '</div> <div style="display: inline-block; width: 100%">'
        html += table_to_html.tab_html(self.tw_save_comparing, table_head="Прочие")
        html += '</div> <div style="display: inline-block; width: 100%">'
        html += table_to_html.tab_html(self.tw_save_product, table_head="Продукция")
        html += '</div>'

        self.print_class = print_qt.PrintHtml(self, html)

    def ui_del_material(self):
        try:
            id = self.tw_save_material.currentItem().data(5)
        except:
            QMessageBox.information(self, "Ошибка", "Выберите запись", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить запись?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            query = "DELETE FROM report_all_material_save WHERE Id = %s"

            sql_info = my_sql.sql_change(query, (id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql удаления записи ткани", sql_info.msg, QMessageBox.Ok)
                return False

            self.view_save()

    def ui_del_accessories(self):
        try:
            id = self.tw_save_accessories.currentItem().data(5)
        except:
            QMessageBox.information(self, "Ошибка", "Выберите запись", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить запись?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            query = "DELETE FROM report_all_accessories_save WHERE Id = %s"

            sql_info = my_sql.sql_change(query, (id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql удаления записи фурнитуры", sql_info.msg, QMessageBox.Ok)
                return False

            self.view_save()

    def ui_del_comparing(self):
        try:
            id = self.tw_save_comparing.currentItem().data(5)
        except:
            QMessageBox.information(self, "Ошибка", "Выберите запись", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить запись?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            query = "DELETE FROM report_all_comparing_save WHERE Id = %s"

            sql_info = my_sql.sql_change(query, (id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql удаления записи прочего", sql_info.msg, QMessageBox.Ok)
                return False

            self.view_save()

    def ui_del_product(self):
        try:
            id = self.tw_save_product.currentItem().data(5)
        except:
            QMessageBox.information(self, "Ошибка", "Выберите запись", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить запись?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            query = "DELETE FROM report_all_accessories_save WHERE Id = %s"

            sql_info = my_sql.sql_change(query, (id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql удаления записи продукции", sql_info.msg, QMessageBox.Ok)
                return False

            self.view_save()


class SaveReportMaterial(QDialog):
    def __init__(self, type_report):
        super(SaveReportMaterial, self).__init__()
        loadUi(getcwd() + '/ui/save_report_material.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.type = type_report

        self.start_sql_info()

    def start_sql_info(self):
        self.listWidget.clear()

        if self.type == "ткань":
            query = """SELECT Id, Date_Save FROM report_all_material_save ORDER BY Date_Save"""
        elif self.type == "фурнитура":
            query = """SELECT Id, Date_Save FROM report_all_accessories_save ORDER BY Date_Save"""
        else:
            QMessageBox.critical(self, "Ошибка типа", "Неизвестный тип", QMessageBox.Ok)
            return False
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения сохраненых дат", sql_info.msg, QMessageBox.Ok)
            return False

        for save_date in sql_info:
            item = QListWidgetItem(save_date[1].strftime("%d.%m.%Y %H:%M:%S"))
            item.setData(5, save_date[0])
            self.listWidget.addItem(item)

    def ui_select_date(self, item):
        if self.type == "ткань":
            query = """SELECT Date_From, Date_To, Last_Balance_Value, Last_Balance_Sum, Supply_Value, Supply_Sum, Consumption_Value,
                            Consumption_Sum, New_Balance_Value, New_Balance_Sum, Transaction_Balance_Value, Transaction_Balance_Sum,
                            Difference_Value, Difference_Sum
                      FROM report_all_material_save WHERE Id = %s"""
        elif self.type == "фурнитура":
            query = """SELECT Date_From, Date_To, Last_Balance_Value, Last_Balance_Sum, Supply_Value, Supply_Sum, Consumption_Value,
                            Consumption_Sum, New_Balance_Value, New_Balance_Sum, Transaction_Balance_Value, Transaction_Balance_Sum,
                            Difference_Value, Difference_Sum
                      FROM report_all_accessories_save WHERE Id = %s"""
        else:
            return False

        sql_info = my_sql.sql_select(query, (item.data(5), ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения сохраненых данных", sql_info.msg, QMessageBox.Ok)
            return False

        if not sql_info:
            return False

        sql_info = sql_info[0]

        self.balance_value = sql_info[10]
        self.balance_sum = sql_info[11]

        self.de_from.setDate(sql_info[0])
        self.de_to.setDate(sql_info[1])
        self.le_last_balance_value.setText(str(sql_info[2]))
        self.le_last_balance_sum.setText(str(sql_info[3]))
        self.le_supply_value.setText(str(sql_info[4]))
        self.le_supply_sum.setText(str(sql_info[5]))
        self.le_consumption_value.setText(str(sql_info[6]))
        self.le_consumption_sum.setText(str(sql_info[7]))
        self.le_transaction_balance_value.setText(str(sql_info[8]))
        self.le_transaction_balance_sum.setText(str(sql_info[9]))
        self.le_new_balance_value.setText(str(sql_info[10]))
        self.le_new_balance_sum.setText(str(sql_info[11]))
        self.le_difference_value.setText(str(sql_info[12]))
        self.le_difference_sum.setText(str(sql_info[13]))

    def ui_acc(self):
        self.done(1)
        self.close()
        self.destroy()

    def ui_del(self):
        try:
            id = self.listWidget.currentItem().data(5)
        except:
            QMessageBox.information(self, "Ошибка", "Выберите запись", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить запись?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            if self.type == "ткань":
                query = "DELETE FROM report_all_material_save WHERE Id = %s"
            elif self.type == "фурнитура":
                query = "DELETE FROM report_all_accessories_save WHERE Id = %s"
            else:
                return False

            sql_info = my_sql.sql_change(query, (id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения сохраненых данных", sql_info.msg, QMessageBox.Ok)
                return False

            self.start_sql_info()


class SaveReportArticle(QDialog):
    def __init__(self):
        super(SaveReportArticle, self).__init__()
        loadUi(getcwd() + '/ui/save_report_article.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_sql_info()

    def start_sql_info(self):
        self.listWidget.clear()

        query = """SELECT Id, Date_Save FROM report_all_article_save ORDER BY Date_Save"""

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения сохраненых дат", sql_info.msg, QMessageBox.Ok)
            return False

        for save_date in sql_info:
            item = QListWidgetItem(save_date[1].strftime("%d.%m.%Y %H:%M:%S"))
            item.setData(5, save_date[0])
            self.listWidget.addItem(item)

    def ui_select_date(self, item):
        query = """SELECT Date_From, Date_To, Last_Balance_Value_Article, Last_Balance_Sum_Article, Supply_Value_Article,
                            Supply_Sum_Seb_Article, Supply_Sum_Price_Article, Supply_Sum_Balance_Article, Sel_Value_Article,
                            Sel_Sum_Price_Article, Sel_Sum_Seb_Article, Sel_Sum_Balance_Article, Warehouse1_Value_Article, Warehouse1_Sum_Article,
                            Warehouse2_Value_Article, Warehouse2_Sum_Article, Difference_Warehouse_Value, Difference_Warehouse_Sum
                  FROM report_all_article_save WHERE Id = %s"""

        sql_info = my_sql.sql_select(query, (item.data(5), ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения сохраненых данных", sql_info.msg, QMessageBox.Ok)
            return False

        if not sql_info:
            return False

        sql_info = sql_info[0]

        self.balance_value = sql_info[14]
        self.balance_sum = sql_info[15]

        self.de_from.setDate(sql_info[0])
        self.de_to.setDate(sql_info[1])
        self.le_last_balance_value_article.setText(str(sql_info[2]))
        self.le_last_balance_sum_article.setText(str(sql_info[3]))
        self.le_supply_value_article.setText(str(sql_info[4]))
        self.le_supply_sum_seb_article.setText(str(sql_info[5]))
        self.le_supply_sum_price_article.setText(str(sql_info[6]))
        self.le_supply_sum_balance_article.setText(str(sql_info[7]))
        self.le_sel_value_article.setText(str(sql_info[8]))
        self.le_sel_sum_price_article.setText(str(sql_info[9]))
        self.le_sel_sum_seb_article.setText(str(sql_info[10]))
        self.le_sel_sum_balance_article.setText(str(sql_info[11]))
        self.le_warehouse1_value_article.setText(str(sql_info[12]))
        self.le_warehouse1_sum_article.setText(str(sql_info[13]))
        self.le_warehouse2_value_article.setText(str(sql_info[14]))
        self.le_warehouse2_sum_article.setText(str(sql_info[15]))
        self.le_difference_warehouse_value.setText(str(sql_info[16]))
        self.le_difference_warehouse_sum.setText(str(sql_info[17]))

    def ui_acc(self):
        self.done(1)
        self.close()
        self.destroy()

    def ui_del(self):
        try:
            id = self.listWidget.currentItem().data(5)
        except:
            QMessageBox.information(self, "Ошибка", "Выберите запись", QMessageBox.Ok)
            return False

        result = QMessageBox.question(self, "Удалить?", "Точно удалить запись?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == 16384:

            query = "DELETE FROM report_all_article_save WHERE Id = %s"

            sql_info = my_sql.sql_change(query, (id, ))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения сохраненых данных", sql_info.msg, QMessageBox.Ok)
                return False

            self.start_sql_info()


