from os import getcwd
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QBrush, QColor
from form.supply_material import MaterialName
from form.pack import PackBrows
import statistics
from decimal import Decimal
from function import my_sql


class MaterialInPack(QMainWindow):
    def __init__(self):
        super(MaterialInPack, self).__init__()
        loadUi(getcwd() + '/ui/report_material_in_pack.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.start_settings()

    def start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-3))
        self.de_date_to.setDate(QDate.currentDate())

        self.tw_pack.horizontalHeader().resizeSection(0, 50)
        self.tw_pack.horizontalHeader().resizeSection(1, 50)
        self.tw_pack.horizontalHeader().resizeSection(2, 50)
        self.tw_pack.horizontalHeader().resizeSection(3, 50)
        self.tw_pack.horizontalHeader().resizeSection(4, 80)
        self.tw_pack.horizontalHeader().resizeSection(5, 80)
        self.tw_pack.horizontalHeader().resizeSection(6, 80)

    def ui_view_material(self):
        self.material_name = MaterialName(self, True)
        self.material_name.setWindowModality(Qt.ApplicationModal)
        self.material_name.show()

    def ui_calc(self):
        self.tw_pack.clearContents()
        self.tw_pack.setRowCount(0)

        # Получить пачки с нужной тканью
        query = """SELECT pack.Article_Parametr_Id, pack.Id, cut.Id, pack.Number, pack.Value_Pieces,
                          pack.Weight, pack.Weight / 100 * cut.Rest_Percent
                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                      WHERE cut.Date_Cut BETWEEN %s AND %s AND cut.Material_Id = %s"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate(), self.le_matrial.whatsThis()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения пачек", sql_info.msg, QMessageBox.Ok)
            return False

        # Получить пачки с доп тканью
        query = """SELECT pack.Article_Parametr_Id, pack.Id, cut.Id, pack.Number, pack.Value_Pieces,
                      pack_add_material.Weight_Rest + pack_add_material.Weight
                    FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                      LEFT JOIN pack_add_material ON pack.Id = pack_add_material.Pack_Id
                    WHERE cut.Date_Cut BETWEEN %s AND %s AND pack_add_material.Material_Name_Id = %s"""
        sql_info_add = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate(), self.le_matrial.whatsThis()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения пачек c доп тканью", sql_info.msg, QMessageBox.Ok)
            return False

        # Составить словать из полученых значений
        # {Артикул: [[Id п, Id к, Номер пачк, кол-во, Вес, обрезь, Доп.тк], ...] , ...}

        article = {}
        for pack in sql_info:
            if pack[1] is not None:
                new = [pack[1], pack[2], pack[3], pack[4], pack[5]/pack[4], pack[6]/pack[4], None]
                article.setdefault(pack[0], []).append(new)

        for pack in sql_info_add:
            if pack[1] is not None:
                new = [pack[1], pack[2], pack[3], pack[4], None, None, pack[5]/pack[4]]
                article.setdefault(pack[0], []).append(new)

        color_g = QBrush(QColor(150, 255, 161, 255))
        color_y = QBrush(QColor(255, 255, 153, 255))
        color_w = QBrush(QColor(255, 255, 255, 255))

        for key, values in article.items():
            # Вставить шапку артикула
            self.tw_pack.insertRow(self.tw_pack.rowCount())
            self.tw_pack.setSpan(self.tw_pack.rowCount() - 1, 0, 1, 7)

            item = QTableWidgetItem("Артикул %s" % key)
            self.tw_pack.setItem(self.tw_pack.rowCount() - 1, 0, item)

            # Найти средние значения и разлеты
            mass = [i[4] for i in values if i[4] is not None]
            if mass:
                m = statistics.mean(mass)
                w_ = m * Decimal(1.15)
                _w = m * Decimal(0.75)
            else:
                w_ = 0
                _w = 0

            mass = [i[5] for i in values if i[5] is not None]
            if mass:
                m = statistics.mean(mass)
                r_ = m * Decimal(1.15)
                _r = m * Decimal(0.75)
            else:
                r_ = 0
                _r = 0

            mass = [i[6] for i in values if i[6] is not None]
            if mass:
                m = statistics.mean(mass)
                a_ = m * Decimal(1.15)
                _a = m * Decimal(0.75)
            else:
                a_ = 0
                _a = 0

            # print("Артикул %s w %s-%s  r %s-%s  a %s-%s " % (key, _w, w_, _r, r_, _a, a_,))

            for value in values:
                # Вставить значения
                self.tw_pack.insertRow(self.tw_pack.rowCount())

                item = QTableWidgetItem(str(value[0]))
                item.setData(5, value[0])
                self.tw_pack.setItem(self.tw_pack.rowCount() - 1, 0, item)

                item = QTableWidgetItem(str(value[1]))
                self.tw_pack.setItem(self.tw_pack.rowCount() - 1, 1, item)

                item = QTableWidgetItem(str(value[2]))
                self.tw_pack.setItem(self.tw_pack.rowCount() - 1, 2, item)

                item = QTableWidgetItem(str(value[3]))
                self.tw_pack.setItem(self.tw_pack.rowCount() - 1, 3, item)

                if value[4] is None:
                    color = color_w
                elif _w < value[4] < w_:
                    color = color_g
                else:
                    color = color_y

                try:
                    txt = str(round(value[4], 7))
                except TypeError:
                    txt = "None"
                item = QTableWidgetItem(txt)
                item.setBackground(color)
                self.tw_pack.setItem(self.tw_pack.rowCount() - 1, 4, item)

                if value[5] is None:
                    color = color_w
                elif _r < value[5] < r_:
                    color = color_g
                else:
                    color = color_y

                try:
                    txt = str(round(value[5], 7))
                except TypeError:
                    txt = "None"
                item = QTableWidgetItem(txt)
                item.setBackground(color)
                self.tw_pack.setItem(self.tw_pack.rowCount() - 1, 5, item)

                if value[6] is None:
                    color = color_w
                elif _a < value[6] < a_:
                    color = color_g
                else:
                    color = color_y

                try:
                    txt = str(round(value[6], 7))
                except TypeError:
                    txt = "None"
                item = QTableWidgetItem(txt)
                item.setBackground(color)
                self.tw_pack.setItem(self.tw_pack.rowCount() - 1, 6, item)

    def ui_dc_row(self, row):
        _id = self.tw_pack.item(row, 0).data(5)
        self.cut_window = PackBrows(self, pack_id=_id)
        self.cut_window.setModal(True)
        self.cut_window.show()

    def of_list_material_name(self, item):
        self.le_matrial.setWhatsThis(str(item[0]))
        self.le_matrial.setText(item[1])