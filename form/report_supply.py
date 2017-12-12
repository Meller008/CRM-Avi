from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, Qt
from form import supply_material, supply_accessories, provider, comparing
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

        self.de_accessories_from.setDate(from_date)
        self.de_accessories_to.setDate(to_date)

        self.de_comparing_from.setDate(from_date)
        self.de_comparing_to.setDate(to_date)

    def set_table_size(self):
        self.tw_material.horizontalHeader().resizeSection(0, 230)
        self.tw_material.horizontalHeader().resizeSection(1, 80)
        self.tw_material.horizontalHeader().resizeSection(2, 70)
        self.tw_material.horizontalHeader().resizeSection(3, 100)

        self.tw_accessories.horizontalHeader().resizeSection(0, 230)
        self.tw_accessories.horizontalHeader().resizeSection(1, 80)
        self.tw_accessories.horizontalHeader().resizeSection(2, 70)
        self.tw_accessories.horizontalHeader().resizeSection(3, 100)

        self.tw_comparing.horizontalHeader().resizeSection(0, 230)
        self.tw_comparing.horizontalHeader().resizeSection(1, 80)
        self.tw_comparing.horizontalHeader().resizeSection(2, 70)
        self.tw_comparing.horizontalHeader().resizeSection(3, 100)

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
        all_value = 0
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
            all_value += material[1]

        else:

            self.tw_material.insertRow(row)
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_material.setItem(row, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_material.setItem(row, 3, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum, 2)))
        self.le_material_sum.setText(text)

    def ui_view_accessories_name(self):
        self.accessories_name = supply_accessories.AccessoriesName(self, True)
        self.accessories_name.setWindowModality(Qt.ApplicationModal)
        self.accessories_name.show()

    def ui_view_provider_accessories(self):
        self.provider_accessories = provider.ProviderAccessories(self, True)
        self.provider_accessories.setWindowModality(Qt.ApplicationModal)
        self.provider_accessories.show()

    def ui_calc_accessories_supply(self):
        sql_where = "WHERE accessories_supply.Data BETWEEN '%s' AND '%s' " % (self.de_accessories_from.date().toString(Qt.ISODate), self.de_accessories_to.date().toString(Qt.ISODate))
        if self.le_material_type.text():
            sql_where += "AND accessories_name.Id = %s " % self.le_accessories_type.whatsThis()
        if self.le_material_provider.text():
            sql_where += "AND accessories_supply.Accessories_SupplyId = %s " % self.le_accessories_provider.whatsThis()

        query = """SELECT accessories_name.Name, SUM(accessories_supplyposition.Value), COUNT(accessories_supply.Id), SUM(accessories_supplyposition.Value * accessories_supplyposition.Price)
                      FROM accessories_supply LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.Accessories_SupplyId
                        LEFT JOIN accessories_name ON accessories_supplyposition.Accessories_NameId = accessories_name.Id
                      WHERE
                      GROUP BY accessories_name.Id"""
        query = query.replace("WHERE", sql_where)

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение приходов фурнитуры", sql_info.msg, QMessageBox.Ok)
                return False

        self.tw_accessories.clearContents()
        self.tw_accessories.setRowCount(0)

        if not sql_info:
            return False

        row = 0
        all_sum = 0
        all_value = 0
        for accessories in sql_info:
            self.tw_accessories.insertRow(row)
            item = QTableWidgetItem(accessories[0])
            self.tw_accessories.setItem(row, 0, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(accessories[1], 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories.setItem(row, 1, item)

            item = QTableWidgetItem(str(accessories[2]))
            self.tw_accessories.setItem(row, 2, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(accessories[3], 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories.setItem(row, 3, item)

            row += 1
            all_sum += accessories[3]
            all_value += accessories[1]

        else:

            self.tw_accessories.insertRow(row)
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories.setItem(row, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_accessories.setItem(row, 3, item)



        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum, 2)))
        self.le_accessories_sum.setText(text)

    def ui_view_comparing_name(self):
        self.comparing = comparing.ComparingName(self, True)
        self.comparing.setWindowModality(Qt.ApplicationModal)
        self.comparing.show()

    def ui_calc_comparing_supply(self):
        if self.cb_material_on.isChecked() and self.cb_accessories_on.isChecked():
            sql_where = """WHERE ((comparing_supplyposition.Comparing_NameId IS NOT NULL AND material_supply.Data BETWEEN '%(from)s' AND '%(to)s') OR
                            (comparing_supplyposition.Accessories_SupplyId IS NOT NULL AND accessories_supply.Data BETWEEN '%(from)s' AND '%(to)s'))""" %\
                                        {"from": self.de_comparing_from.date().toString(Qt.ISODate), "to": self.de_comparing_to.date().toString(Qt.ISODate)}

        elif self.cb_material_on.isChecked():
            sql_where = "WHERE (comparing_supplyposition.Comparing_NameId IS NOT NULL AND material_supply.Data BETWEEN '%s' AND '%s')" %\
                                (self.de_comparing_from.date().toString(Qt.ISODate), self.de_comparing_to.date().toString(Qt.ISODate))

        elif self.cb_accessories_on.isChecked():
            sql_where = "WHERE (comparing_supplyposition.Accessories_SupplyId IS NOT NULL AND accessories_supply.Data BETWEEN '%s' AND '%s')" %\
                                (self.de_comparing_from.date().toString(Qt.ISODate), self.de_comparing_to.date().toString(Qt.ISODate))
        else:
            QMessageBox.information(self, "Ошибка", "Выберите каокой тип затрат показывать (можно оба)", QMessageBox.Ok)
            return False

        if self.le_comparing_type.text():
            sql_where += " AND comparing_name.Id = %s" % self.le_comparing_type.whatsThis()


        query = """SELECT comparing_name.Name, SUM(comparing_supplyposition.Value), COUNT(material_supply.Id) + COUNT(accessories_supply.Id),
                        SUM(comparing_supplyposition.Value * comparing_supplyposition.Price)
                      FROM comparing_name LEFT JOIN comparing_supplyposition ON comparing_name.Id = comparing_supplyposition.Comparing_NameId
                        LEFT JOIN material_supply ON comparing_supplyposition.Material_SupplyId = material_supply.Id
                        LEFT JOIN accessories_supply ON comparing_supplyposition.Accessories_SupplyId = accessories_supply.Id
                      WHERE"""
        query = query.replace("WHERE", sql_where)

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение расходов", sql_info.msg, QMessageBox.Ok)
                return False

        self.tw_comparing.clearContents()
        self.tw_comparing.setRowCount(0)

        if not sql_info or sql_info[0][0] is None:
            return False

        row = 0
        all_sum = 0
        all_value = 0
        for comparing in sql_info:
            self.tw_comparing.insertRow(row)
            item = QTableWidgetItem(comparing[0])
            self.tw_comparing.setItem(row, 0, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(comparing[1], 2)))
            item = QTableWidgetItem(text)
            self.tw_comparing.setItem(row, 1, item)

            item = QTableWidgetItem(str(comparing[2]))
            self.tw_comparing.setItem(row, 2, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(comparing[3], 2)))
            item = QTableWidgetItem(text)
            self.tw_comparing.setItem(row, 3, item)

            row += 1
            all_sum += comparing[3]
            all_value += comparing[1]
        else:

            self.tw_comparing.insertRow(row)
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_value, 2)))
            item = QTableWidgetItem(text)
            self.tw_comparing.setItem(row, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum, 2)))
            item = QTableWidgetItem(text)
            self.tw_comparing.setItem(row, 3, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum, 2)))
        self.le_comparing_sum.setText(text)

    def ui_print_report(self):
        up_html = """
          <table>
          <tr>
          <th>Тип</th><th>Поставщик</th><th>Дата с</th><th>Дата по</th><th>ИТОГО</th>
          </tr>
          <tr>
          <td>#type#</td><td>#provider#</td><td>#data_from#</td><td>#data_to#</td><td>#sum#</td>
          </tr>
          </table>
          """

        if self.tabWidget.currentIndex() == 0:
            head = "Отчет по приходу ткани"
            up_html = up_html.replace("#type#", self.le_material_type.text())
            up_html = up_html.replace("#provider#", self.le_material_provider.text())
            up_html = up_html.replace("#data_from#", self.de_material_from.date().toString("dd.MM.yyyy"))
            up_html = up_html.replace("#data_to#", self.de_material_to.date().toString("dd.MM.yyyy"))
            up_html = up_html.replace("#sum#", self.le_material_sum.text())
            table_widget = self.tw_material
        elif self.tabWidget.currentIndex() == 1:
            head = "Отчет по приходу фурнитуры"
            up_html = up_html.replace("#type#", self.le_accessories_type.text())
            up_html = up_html.replace("#provider#", self.le_accessories_provider.text())
            up_html = up_html.replace("#data_from#", self.de_accessories_from.date().toString("dd.MM.yyyy"))
            up_html = up_html.replace("#data_to#", self.de_accessories_to.date().toString("dd.MM.yyyy"))
            up_html = up_html.replace("#sum#", self.le_accessories_sum.text())
            table_widget = self.tw_accessories

        elif self.tabWidget.currentIndex() == 2:
            head = "Отчет по расходам на поставки"
            up_html = up_html.replace("#type#", self.le_comparing_type.text())
            up_html = up_html.replace("#provider#", "")
            up_html = up_html.replace("#data_from#", self.de_comparing_from.date().toString("dd.MM.yyyy"))
            up_html = up_html.replace("#data_to#", self.de_comparing_to.date().toString("dd.MM.yyyy"))
            up_html = up_html.replace("#sum#", self.le_comparing_sum.text())
            table_widget = self.tw_comparing
        else:
            return False

        html = table_to_html.tab_html(table_widget, table_head=head, up_template=up_html)
        self.print_class = print_qt.PrintHtml(self, html)

    def of_list_material_name(self, item):
        self.le_material_type.setWhatsThis(str(item[0]))
        self.le_material_type.setText(item[1])

    def of_list_reason_provider_material(self, item):
        self.le_material_provider.setWhatsThis(str(item[0]))
        self.le_material_provider.setText(item[1])

    def of_list_accessories_name(self, item):
        self.le_accessories_type.setWhatsThis(str(item[0]))
        self.le_accessories_type.setText(item[1])

    def of_list_reason_provider_accessories(self, item):
        self.le_accessories_provider.setWhatsThis(str(item[0]))
        self.le_accessories_provider.setText(item[1])

    def of_list_reason_comparing_material(self, item):
        self.le_comparing_type.setWhatsThis(str(item[0]))
        self.le_comparing_type.setText(item[1])