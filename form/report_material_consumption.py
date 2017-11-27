from os import getcwd
import re
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QMainWindow,  QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate
from function import my_sql
from classes import print_qt
from function import table_to_html, to_excel

material_consumption_class = loadUiType(getcwd() + '/ui/report_material_consumption.ui')[0]


class ReportMaterialConsumption(QMainWindow, material_consumption_class):
    def __init__(self):
        super(ReportMaterialConsumption, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_settings()

    def start_settings(self):
        self.de_material_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_material_to.setDate(QDate.currentDate())
        self.de_accessories_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_accessories_to.setDate(QDate.currentDate())
        self.de_comparing_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_comparing_to.setDate(QDate.currentDate())

        self.tw_material.horizontalHeader().resizeSection(0, 150)
        self.tw_material.horizontalHeader().resizeSection(1, 70)
        self.tw_material.horizontalHeader().resizeSection(2, 80)
        self.tw_material.horizontalHeader().resizeSection(3, 70)
        self.tw_material.horizontalHeader().resizeSection(4, 80)

        self.tw_material_info.horizontalHeader().resizeSection(0, 100)
        self.tw_material_info.horizontalHeader().resizeSection(1, 90)
        self.tw_material_info.horizontalHeader().resizeSection(2, 90)

        self.tw_accessories.horizontalHeader().resizeSection(0, 150)
        self.tw_accessories.horizontalHeader().resizeSection(1, 85)
        self.tw_accessories.horizontalHeader().resizeSection(2, 80)
        self.tw_accessories.horizontalHeader().resizeSection(3, 85)
        self.tw_accessories.horizontalHeader().resizeSection(4, 80)

        self.tw_accesories_info.horizontalHeader().resizeSection(0, 100)
        self.tw_accesories_info.horizontalHeader().resizeSection(1, 90)
        self.tw_accesories_info.horizontalHeader().resizeSection(2, 90)

        self.tw_comparing.horizontalHeader().resizeSection(0, 150)
        self.tw_comparing.horizontalHeader().resizeSection(1, 70)
        self.tw_comparing.horizontalHeader().resizeSection(2, 80)

    def ui_calc_material(self):
        # Расчет общего расхода ткани
        query = """SELECT material_name.Id, material_name.Name, SUM(material_supplyposition.Weight),
                        SUM(material_supplyposition.Weight * material_supplyposition.Price)
                      FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                        LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                      WHERE material_supply.Data >= %s AND material_supply.Data <= %s
                      GROUP BY material_name.Id"""
        sql_material_in = my_sql.sql_select(query, (self.de_material_from.date().toString(Qt.ISODate), self.de_material_to.date().toString(Qt.ISODate)))
        if "mysql.connector.errors" in str(type(sql_material_in)):
            QMessageBox.critical(self, "Ошибка sql получения приходов ткани", sql_material_in.msg, QMessageBox.Ok)
            return False

        query = """SELECT material_name.Id, material_name.Name, SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                      LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                        LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                        LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                      WHERE transaction_records_material.Cut_Material_Id IN (SELECT cut.Id FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)
                          OR transaction_records_material.Beika_Id IN (SELECT beika.Id FROM beika WHERE Date >= %s AND Date <= %s)
                          OR (transaction_records_material.Note LIKE 'Продажа%' AND transaction_records_material.Date >= %s 
                            AND transaction_records_material.Date <= DATE_FORMAT(%s,'%Y-%m-%d 23:59:59'))
                      GROUP BY material_name.Id"""
        sql_material_out = my_sql.sql_select(query, (self.de_material_from.date().toString(Qt.ISODate), self.de_material_to.date().toString(Qt.ISODate))*3)
        if "mysql.connector.errors" in str(type(sql_material_out)):
            QMessageBox.critical(self, "Ошибка sql получения расходов ткани", sql_material_out.msg, QMessageBox.Ok)
            return False

        all_list_consumption = []
        for out in sql_material_out:
            fillst = list(filter(lambda s: s[0] == out[0], sql_material_in))

            if fillst:
                newlst = [out[0], out[1], fillst[0][2], fillst[0][3], out[2], out[3]]
            else:
                newlst = [out[0], out[1], 0, 0, out[2], out[3]]

            all_list_consumption.append(newlst)

        self.tw_material.clearContents()
        self.tw_material.setRowCount(0)

        all_weight_in = 0
        all_weight_out = 0
        all_sum_in = 0
        all_sum_out = 0

        for i in all_list_consumption:
            self.tw_material.insertRow(self.tw_material.rowCount())

            item = QTableWidgetItem(str(i[1]))
            item.setData(5, i[0])
            self.tw_material.setItem(self.tw_material.rowCount() - 1, 0, item)

            all_weight_in += i[2]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_material.setItem(self.tw_material.rowCount() - 1, 1, item)

            all_sum_in += i[3]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[3], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_material.setItem(self.tw_material.rowCount() - 1, 2, item)

            all_weight_out += i[4]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[4], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_material.setItem(self.tw_material.rowCount() - 1, 3, item)

            all_sum_out += i[5]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[5], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_material.setItem(self.tw_material.rowCount() - 1, 4, item)

        self.tw_material.insertRow(self.tw_material.rowCount())

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_weight_in, 2)))
        item = QTableWidgetItem(text)
        self.tw_material.setItem(self.tw_material.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_in, 2)))
        item = QTableWidgetItem(text)
        self.tw_material.setItem(self.tw_material.rowCount() - 1, 2, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_weight_out, 2)))
        item = QTableWidgetItem(text)
        self.tw_material.setItem(self.tw_material.rowCount() - 1, 3, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_out, 2)))
        item = QTableWidgetItem(text)
        self.tw_material.setItem(self.tw_material.rowCount() - 1, 4, item)

    def ui_calc_material_info(self):
        # Расчет подробный
        self.tw_material_info.clearContents()
        self.tw_material_info.setRowCount(0)

        filter_date = (self.de_material_from.date().toString(Qt.ISODate), self.de_material_to.date().toString(Qt.ISODate))

        query = """SELECT SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Note LIKE '%пачк%'
                        AND transaction_records_material.Cut_Material_Id IN (SELECT cut.Id FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на пачки", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_material_info.insertRow(self.tw_material_info.rowCount())

        item = QTableWidgetItem("Пачки")
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 2, item)

        query = """SELECT SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Note LIKE '%обрез%'
                        AND transaction_records_material.Cut_Material_Id IN (SELECT cut.Id FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на обрезь", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_material_info.insertRow(self.tw_material_info.rowCount())

        item = QTableWidgetItem("Обрезь")
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 2, item)

        query = """SELECT SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Note LIKE '%доп.%'
                        AND transaction_records_material.Cut_Material_Id IN (SELECT cut.Id FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на доп ткань", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_material_info.insertRow(self.tw_material_info.rowCount())

        item = QTableWidgetItem("Доп. ткань")
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 2, item)

        query = """SELECT SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Note LIKE '%бейк%'
                        AND transaction_records_material.Beika_Id IN (SELECT beika.Id FROM beika WHERE Date >= %s AND Date <= %s)"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на бйеку", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_material_info.insertRow(self.tw_material_info.rowCount())

        item = QTableWidgetItem("Бейка")
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 2, item)

        query = """SELECT SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Note LIKE '%продаж%'
                        AND transaction_records_material.Date >= %s AND transaction_records_material.Date <= DATE_FORMAT(%s,'%Y-%m-%d 23:59:59')"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на продажу ткани", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_material_info.insertRow(self.tw_material_info.rowCount())

        item = QTableWidgetItem("Продажа ткани")
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 2, item)

    def ui_print_material(self):
        head = "Расход ткани с %s По %s" % (self.de_material_from.date().toString("dd.MM.yyyy"), self.de_material_to.date().toString("dd.MM.yyyy"))
        html = table_to_html.tab_html(self.tw_material, table_head=head)
        html += table_to_html.tab_html(self.tw_material_info, table_head="Подробно")
        self.print_class = print_qt.PrintHtml(self, html)

    def ui_calc_accessories(self):
        # Расчет общего расхода Фурнитуры
        query = """SELECT accessories_name.Id, accessories_name.Name, SUM(accessories_supplyposition.Value), 
                        SUM(accessories_supplyposition.Value * accessories_supplyposition.Price)
                      FROM accessories_supply LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.Accessories_SupplyId
                        LEFT JOIN accessories_name ON accessories_supplyposition.Accessories_NameId = accessories_name.Id
                      WHERE accessories_supply.Data >= %s and accessories_supply.Data <= %s
                      GROUP BY accessories_name.Id"""
        sql_material_in = my_sql.sql_select(query, (self.de_accessories_from.date().toString(Qt.ISODate), self.de_accessories_to.date().toString(Qt.ISODate)))
        if "mysql.connector.errors" in str(type(sql_material_in)):
            QMessageBox.critical(self, "Ошибка sql получения приходов Фурнитуры", sql_material_in.msg, QMessageBox.Ok)
            return False

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
        sql_material_out = my_sql.sql_select(query, (self.de_accessories_from.date().toString(Qt.ISODate), self.de_accessories_to.date().toString(Qt.ISODate)))
        if "mysql.connector.errors" in str(type(sql_material_out)):
            QMessageBox.critical(self, "Ошибка sql получения расходов фурнитуры", sql_material_out.msg, QMessageBox.Ok)
            return False

        all_list_consumption = []
        for out in sql_material_out:
            fillst = list(filter(lambda s: s[0] == out[0], sql_material_in))

            if fillst:
                newlst = [out[0], out[1], fillst[0][2], fillst[0][3], out[2], out[3]]
            else:
                newlst = [out[0], out[1], 0, 0, out[2], out[3]]

            all_list_consumption.append(newlst)

        self.tw_accessories.clearContents()
        self.tw_accessories.setRowCount(0)

        all_weight_in = 0
        all_weight_out = 0
        all_sum_in = 0
        all_sum_out = 0

        for i in all_list_consumption:
            self.tw_accessories.insertRow(self.tw_accessories.rowCount())

            item = QTableWidgetItem(str(i[1]))
            item.setData(5, i[0])
            self.tw_accessories.setItem(self.tw_accessories.rowCount() - 1, 0, item)

            all_weight_in += i[2]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_accessories.setItem(self.tw_accessories.rowCount() - 1, 1, item)

            all_sum_in += i[3]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[3], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_accessories.setItem(self.tw_accessories.rowCount() - 1, 2, item)

            all_weight_out += i[4]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[4], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_accessories.setItem(self.tw_accessories.rowCount() - 1, 3, item)

            all_sum_out += i[5]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[5], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_accessories.setItem(self.tw_accessories.rowCount() - 1, 4, item)

        self.tw_accessories.insertRow(self.tw_accessories.rowCount())

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_weight_in, 2)))
        item = QTableWidgetItem(text)
        self.tw_accessories.setItem(self.tw_accessories.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_in, 2)))
        item = QTableWidgetItem(text)
        self.tw_accessories.setItem(self.tw_accessories.rowCount() - 1, 2, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_weight_out, 2)))
        item = QTableWidgetItem(text)
        self.tw_accessories.setItem(self.tw_accessories.rowCount() - 1, 3, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_out, 2)))
        item = QTableWidgetItem(text)
        self.tw_accessories.setItem(self.tw_accessories.rowCount() - 1, 4, item)

    def ui_calc_accessories_info(self):
        # Расчет подробный фурнитуры
        self.tw_accesories_info.clearContents()
        self.tw_accesories_info.setRowCount(0)

        filter_date = (self.de_accessories_from.date().toString(Qt.ISODate), self.de_accessories_to.date().toString(Qt.ISODate))

        query = """SELECT SUM(transaction_records_accessories.Balance),
                        SUM(transaction_records_accessories.Balance * accessories_supplyposition.Price)
                      FROM transaction_records_accessories
                        LEFT JOIN accessories_balance ON transaction_records_accessories.Supply_Balance_Id = accessories_balance.Id
                        LEFT JOIN accessories_supplyposition ON accessories_balance.accessories_SupplyPositionId = accessories_supplyposition.Id
                      WHERE transaction_records_accessories.Pack_Accessories_Id IN (SELECT pack_accessories.Id
                                                                                      FROM pack_accessories LEFT JOIN pack ON pack_accessories.Pack_Id = pack.Id
                                                                                        LEFT JOIN cut ON pack.Cut_Id = cut.Id
                                                                                      WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s)"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на пачки", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_accesories_info.insertRow(self.tw_accesories_info.rowCount())

        item = QTableWidgetItem("Пачки")
        self.tw_accesories_info.setItem(self.tw_accesories_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_accesories_info.setItem(self.tw_accesories_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_accesories_info.setItem(self.tw_accesories_info.rowCount() - 1, 2, item)

    def ui_print_accessories(self):
        head = "Расход фурнитуры с %s По %s" % (self.de_accessories_from.date().toString("dd.MM.yyyy"), self.de_accessories_to.date().toString("dd.MM.yyyy"))
        html = table_to_html.tab_html(self.tw_accessories, table_head=head)
        html += table_to_html.tab_html(self.tw_accesories_info, table_head="Подробно")
        self.print_class = print_qt.PrintHtml(self, html)

    def ui_calc_comparing(self):
        # Расчет прочих затрат
        self.tw_comparing.clearContents()
        self.tw_comparing.setRowCount(0)

        filter_date = (self.de_comparing_from.date().toString(Qt.ISODate), self.de_comparing_to.date().toString(Qt.ISODate))

        query = """SELECT comparing_name.Name, SUM(comparing_supplyposition.Value), SUM(comparing_supplyposition.Value * comparing_supplyposition.Price)
                    FROM comparing_supplyposition LEFT JOIN material_supply ON comparing_supplyposition.Material_SupplyId = material_supply.Id
                      LEFT JOIN accessories_supply ON comparing_supplyposition.Accessories_SupplyId = accessories_supply.Id
                      LEFT JOIN comparing_name ON comparing_supplyposition.Comparing_NameId = comparing_name.Id
                      WHERE (material_supply.Data >= %s AND material_supply.Data <= %s) OR (accessories_supply.Data >= %s AND accessories_supply.Data <= %s)
                      GROUP BY comparing_name.Id"""
        sql_info = my_sql.sql_select(query, filter_date*2)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения прочих расходоа", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_comparing.insertRow(self.tw_comparing.rowCount())

        all_value = 0
        all_sum = 0
        for i in sql_info:
            self.tw_comparing.insertRow(self.tw_comparing.rowCount())

            item = QTableWidgetItem(str(i[0]))
            self.tw_comparing.setItem(self.tw_comparing.rowCount() - 1, 0, item)

            all_value += i[1]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[1], 2)))
            item = QTableWidgetItem(text)
            self.tw_comparing.setItem(self.tw_comparing.rowCount() - 1, 1, item)

            all_sum += i[2]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2], 2)))
            item = QTableWidgetItem(text)
            self.tw_comparing.setItem(self.tw_comparing.rowCount() - 1, 2, item)

        self.tw_comparing.insertRow(self.tw_comparing.rowCount())

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_value, 2)))
        item = QTableWidgetItem(text)
        self.tw_comparing.setItem(self.tw_comparing.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum, 2)))
        item = QTableWidgetItem(text)
        self.tw_comparing.setItem(self.tw_comparing.rowCount() - 1, 2, item)

    def ui_print_comparing(self):
        head = "Прочие расходы с %s По %s" % (self.de_comparing_from.date().toString("dd.MM.yyyy"), self.de_comparing_to.date().toString("dd.MM.yyyy"))
        html = table_to_html.tab_html(self.tw_comparing, table_head=head)
        self.print_class = print_qt.PrintHtml(self, html)