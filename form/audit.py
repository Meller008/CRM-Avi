from os import getcwd
from form import order, staff
from datetime import datetime
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QTreeWidgetItem, QPushButton
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import Qt, QDate, QObject
from form.material import MaterialName
from form.pack import PackBrows
import re
import json
import openpyxl
import random
from openpyxl.styles import Border, Side, Alignment

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
        with open(self.le_dir.text(), 'r', encoding='utf-8') as fh:
            base = json.load(fh)

        book = openpyxl.load_workbook(filename=getcwd() + '/templates/audit/verification/verification_journal.xlsx')
        sheet = book["Лист1"]

        row = 3
        start_date = datetime.strptime(self.de_date.date().toString("dd.MM.yyyy"), "%d.%m.%Y")

        if self.cb_material.isChecked():
            for base_item in base:
                print(base_item["FLD491"])
                if base_item["FLD491"] is not None and datetime.strptime(base_item["FLD491"], "%d.%m.%Y") > start_date:
                    sheet["A%s" % row] = base_item["FLD491"]

                    if base_item["FLD500"] == 13:
                        post_name = "Декна"
                    elif base_item["FLD500"] == 28:
                        post_name = "Сим текс"
                    else:
                        if random.randrange(0, 2, 1) == 0:
                            post_name = "Декна"
                        else:
                            post_name = "Сим текс"
                    sheet["B%s" % row] = post_name

                    sheet["C%s" % row] = "Кулирное полотно"

                    if post_name == "Декна":
                        sert = "TC RU Д-TR.AB82.B.02881"
                    else:
                        sert = "TC N RU Д-TR.CC04.B.00247"
                    sheet["D%s" % row] = sert

                    sheet["E%s" % row] = "пакет"

                    sheet["F%s" % row] = base_item["FLD501"]

                    mon = str(datetime.strptime(base_item["FLD491"], "%d.%m.%Y").month - 1)
                    year = str(datetime.strptime(base_item["FLD491"], "%d.%m.%Y").year)

                    sheet["G%s" % row] = mon + "." + year

                    sheet["H%s" % row] = "Склад"

                    sheet["I%s" % row] = base_item["FLD491"]

                    sheet["J%s" % row] = "Хорошее кач."



                    f = open(getcwd() + '/templates/audit/verification/act.xml', "r", -1, "utf-8")
                    xml = f.read()
                    f.close()

                    xml = xml.replace("ПОСТ", post_name)
                    xml = xml.replace("ДАТА", base_item["FLD491"])
                    xml = xml.replace("НОМЕР", re.sub(r', сумма+.*', "", base_item["FLD498"]))
                    xml = xml.replace("КОЛ-ВО", str(base_item["FLD501"]))
                    xml = xml.replace("ПРОБЫ", str(int(base_item["FLD501"] // 1000)))

                    file_name = "АКТ%s.xml" % (row-2, )
                    f = open('%s/%s' % ("C:/Users/cs007/Desktop/aud/mater/act", file_name), "w", -1, "utf-8")
                    f.write(xml)
                    f.close()


                    row += 1

            book.save("C:/Users/cs007/Desktop/aud/mater/verification_journal.xlsx")
        else:
            for base_item in base:
                print(base_item["DAT"])
                if base_item["DAT"] is not None and datetime.strptime(base_item["DAT"], "%d.%m.%Y") > start_date:

                    if base_item["POST"] == 18:
                        if 1:

                            vid = "Эткетки"
                            pack = "Бумажная"
                            post_name = "Визови"

                            sheet["A%s" % row] = base_item["DAT"]

                            sheet["B%s" % row] = post_name

                            sheet["C%s" % row] = vid

                            sert = " "
                            sheet["D%s" % row] = sert

                            sheet["E%s" % row] = pack

                            sheet["F%s" % row] = base_item["SUM"]

                            mon = str(datetime.strptime(base_item["DAT"], "%d.%m.%Y").month - 1)
                            year = str(datetime.strptime(base_item["DAT"], "%d.%m.%Y").year)
                            if mon == 0:
                                mon = 12
                                year -= 1

                            sheet["G%s" % row] = mon + "." + year

                            sheet["H%s" % row] = "Склад"

                            sheet["I%s" % row] = base_item["DAT"]

                            sheet["J%s" % row] = "Хорошее кач."



                            f = open(getcwd() + '/templates/audit/verification/act.xml', "r", -1, "utf-8")
                            xml = f.read()
                            f.close()

                            xml = xml.replace("ВИД", vid)
                            xml = xml.replace("ПОСТ", post_name)
                            xml = xml.replace("УПАКОВКА", pack)
                            xml = xml.replace("ДАТА", base_item["DAT"])
                            xml = xml.replace("НОМЕР", re.sub(r', сумма+.*', "", base_item["NOTE"]))
                            xml = xml.replace("КОЛ-ВО", str(base_item["SUM"]))
                            # xml = xml.replace("ПРОБЫ", str(int(base_item["SUM"] // 1000000)))
                            xml = xml.replace("ПРОБЫ", "10-50")

                            file_name = "АКТ%s.xml" % (row-2, )
                            f = open('%s/%s' % ("C:/Users/cs007/Desktop/aud/furn/etiket/act", file_name), "w", -1, "utf-8")
                            f.write(xml)
                            f.close()


                            row += 1

            book.save("C:/Users/cs007/Desktop/aud/furn/etiket/verification_journal.xlsx")



