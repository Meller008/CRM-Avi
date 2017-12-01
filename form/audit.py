from os import getcwd
from datetime import datetime
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
import re
import json
import openpyxl
import random

from function import my_sql

verification_class = loadUiType(getcwd() + '/ui/audit_verification.ui')[0]


class AuditVerification(QMainWindow, verification_class):
    def __init__(self):
        super(AuditVerification, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.de_date.setDate(QDate.currentDate())

    def ui_file_json(self):
        file_dir = QFileDialog.getOpenFileName(self, "Выберите базу", "C:/", "*.json")
        if file_dir[1] == "":
            return False

        self.le_dir.setText(file_dir[0])

    def ui_start(self):
        book = openpyxl.load_workbook(filename=getcwd() + '/templates/audit/verification/verification_journal.xlsx')
        sheet = book["Лист1"]

        row = 3
        start_date = datetime.strptime(self.de_date.date().toString("dd.MM.yyyy"), "%d.%m.%Y")

        if self.cb_material.isChecked():
            query = """SELECT material_supply.Data, material_provider.Name, SUM(material_supplyposition.Weight), material_supply.Note
                        FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                          LEFT JOIN material_provider ON material_supply.Material_ProviderId = material_provider.Id
                        WHERE material_supply.Data > '2017-10-31'
                        GROUP BY material_supply.Id"""
            sql_info = my_sql.sql_select(query)
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения ткани", sql_info.msg, QMessageBox.Ok)
                return False
            for base_item in sql_info:
                print(base_item[0])
                if base_item[0] is not None and base_item[0] > start_date.date():
                    sheet["A%s" % row] = base_item[0].strftime("%d.%m.%Y")

                    post_name = base_item[1]

                    sheet["B%s" % row] = post_name
                    sheet["C%s" % row] = "Кулирное полотно"

                    if post_name == "Мадио Декна ООО":
                        sert = "RU Д-UZ.AB71.B.34983"
                    else:
                        sert = "RU Д-UZ.ГР01.B.09974"

                    sheet["D%s" % row] = sert
                    sheet["E%s" % row] = "пакет"
                    sheet["F%s" % row] = base_item[2]

                    mon = str(base_item[0].month - 1)
                    year = str(base_item[0].year)

                    if mon == 0:
                        mon = 12
                        year -= 1

                    sheet["G%s" % row] = mon + "." + year
                    sheet["H%s" % row] = "Склад"
                    sheet["I%s" % row] = base_item[0].strftime("%d.%m.%Y")
                    sheet["J%s" % row] = "Хорошее кач."

                    f = open(getcwd() + '/templates/audit/verification/act.xml', "r", -1, "utf-8")
                    xml = f.read()
                    f.close()

                    xml = xml.replace("ПОСТ", post_name)
                    xml = xml.replace("ДАТА", base_item[0].strftime("%d.%m.%Y"))
                    xml = xml.replace("НОМЕР", re.sub(r', сумма+.*', "", str(base_item[3])))
                    xml = xml.replace("КОЛ-ВО", str(base_item[2]))
                    xml = xml.replace("ПРОБЫ", str(int(base_item[2] // 1000)))

                    file_name = "АКТ%s.xml" % (row-2, )
                    f = open('%s/%s' % ("C:/Users/Meller/Desktop/aud/mater/act", file_name), "w", -1, "utf-8")
                    f.write(xml)
                    f.close()

                    row += 1

            book.save("C:/Users/Meller/Desktop/aud/mater/verification_journal.xlsx")
        else:
            query = """SELECT accessories_supply.Data, accessories_provider.Name, SUM(accessories_supplyposition.Value), accessories_supply.Note
                        FROM accessories_supply LEFT JOIN accessories_supplyposition ON accessories_supply.Id = accessories_supplyposition.Accessories_SupplyId
                          LEFT JOIN accessories_provider ON accessories_supply.Accessories_ProviderId = accessories_provider.Id
                        WHERE accessories_supply.Data > '2017-10-31' AND accessories_provider.Id = 14
                        GROUP BY accessories_supply.Id"""
            sql_info = my_sql.sql_select(query)
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения фурн", sql_info.msg, QMessageBox.Ok)
                return False
            for base_item in sql_info:
                print(base_item[0])
                if base_item[0] is not None and base_item[0] > start_date.date():

                    vid = "Резинка"
                    pack = "Гофрокартон"
                    post_name = base_item[1]
                    sert = "РОСС RU.AB51.H00287"

                    sheet["A%s" % row] = base_item[0].strftime("%d.%m.%Y")
                    sheet["B%s" % row] = post_name
                    sheet["C%s" % row] = vid
                    sheet["D%s" % row] = sert
                    sheet["E%s" % row] = pack
                    sheet["F%s" % row] = base_item[2]

                    mon = str(base_item[0].month - 1)
                    year = str(base_item[0].year)
                    if mon == 0:
                        mon = 12
                        year -= 1

                    sheet["G%s" % row] = mon + "." + year
                    sheet["H%s" % row] = "Склад"
                    sheet["I%s" % row] = base_item[0].strftime("%d.%m.%Y")
                    sheet["J%s" % row] = "Хорошее кач."

                    f = open(getcwd() + '/templates/audit/verification/act.xml', "r", -1, "utf-8")
                    xml = f.read()
                    f.close()

                    xml = xml.replace("ВИД", vid)
                    xml = xml.replace("ПОСТ", post_name)
                    xml = xml.replace("УПАКОВКА", pack)
                    xml = xml.replace("ДАТА", base_item[0].strftime("%d.%m.%Y"))
                    xml = xml.replace("НОМЕР", re.sub(r', сумма+.*', "", base_item[3]))
                    xml = xml.replace("КОЛ-ВО", str(base_item[2]))
                    xml = xml.replace("ПРОБЫ", "10-50")

                    file_name = "АКТ%s.xml" % (row-2, )
                    f = open('%s/%s' % ("C:/Users/Meller/Desktop/aud/furn/rez/act", file_name), "w", -1, "utf-8")
                    f.write(xml)
                    f.close()

                    row += 1

            book.save("C:/Users/Meller/Desktop/aud/furn/rez/verification_journal.xlsx")



