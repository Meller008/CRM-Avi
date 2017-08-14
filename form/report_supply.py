from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, Qt
from form import supply_material, provider
from function import my_sql, to_excel, table_to_html
from classes import print_qt
from decimal import Decimal
import datetime
import re

report_supply_class = loadUiType(getcwd() + '/ui/report_supply.ui')[0]


class ReportSupply(QMainWindow, report_supply_class):
    def __init__(self):
        super(ReportSupply, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()
        self.set_table_size()

    def set_start_settings(self):
        to_date = QDate.currentDate()
        from_date = to_date.addMonths(-1)

        self.de_material_from.setDate(from_date)
        self.de_material_to.setDate(to_date)

    def set_table_size(self):
        self.tw_material.horizontalHeader().resizeSection(0, 230)
        self.tw_material.horizontalHeader().resizeSection(1, 80)
        self.tw_material.horizontalHeader().resizeSection(2, 70)
        self.tw_material.horizontalHeader().resizeSection(3, 100)

    def ui_view_material_name(self):
        self.material_name = supply_material.MaterialName(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_view_provider_material(self):
        self.provider = provider.ProviderMaterial(self, True)
        self.provider.setWindowModality(Qt.ApplicationModal)
        self.provider.show()

    def ui_calc_material_supply(self):
        sql_where = "WHERE material_supply.Data BETWEEN '%s' AND '%s' " % (self.de_material_from.date().toString(Qt.ISODate), self.de_material_to.date().toString(Qt.ISODate))
        if self.le_material_type.text():
            sql_where += "AND material_name.Id = %s " % self.le_material_type.whatsThis()
        if self.le_material_provider.text():
            sql_where += "AND material_supply.Material_ProviderId = %s " % self.le_material_provider.whatsThis()

        query = """SELECT material_name.Name, SUM(material_supplyposition.Weight), COUNT(material_supply.Id), SUM(material_supplyposition.Weight * material_supplyposition.Price)
                      FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                        LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                      WHERE
                      GROUP BY material_name.Id"""
        query = query.replace("WHERE", sql_where)

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение приходов материала", sql_info.msg, QMessageBox.Ok)
                return False

        self.tw_material.clearContents()
        self.tw_material.setRowCount(0)

        if not sql_info:
            return False

        row = 0
        all_sum = 0
        for material in sql_info:
            self.tw_material.insertRow(row)
            item = QTableWidgetItem(material[0])
            self.tw_material.setItem(row, 0, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(material[1], 2)))
            item = QTableWidgetItem(text)
            self.tw_material.setItem(row, 1, item)

            item = QTableWidgetItem(str(material[2]))
            self.tw_material.setItem(row, 2, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(material[3], 2)))
            item = QTableWidgetItem(text)
            self.tw_material.setItem(row, 3, item)

            row += 1
            all_sum += material[3]

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum, 2)))
        self.le_material_sum.setText(text)

    def of_list_material_name(self, item):
        self.le_material_type.setWhatsThis(str(item[0]))
        self.le_material_type.setText(item[1])

    def of_list_reason_provider_material(self, item):
        self.le_material_provider.setWhatsThis(str(item[0]))
        self.le_material_provider.setText(item[1])