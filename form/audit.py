from os import getcwd
import random
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
import re
import openpyxl

from function import my_sql
from form.supply_material import MaterialSupplyList
from form.provider import ProviderMaterial, ProviderAccessories

# Типы материалов
# 0 - Ткани
# 1 - Нитки
# 2 - Резинка
# 3 - Пуговицы
# 4 - Этикетки

class AuditVerification(QDialog):
    def __init__(self):
        super(AuditVerification, self).__init__()
        loadUi(getcwd() + '/ui/audit.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.tip = 0

        self.update()

    def update(self):

        if self.tip == 0:
            table = self.ui_tw_0
        elif self.tip == 1:
            table = self.ui_tw_1
        elif self.tip == 2:
            table = self.ui_tw_2
        elif self.tip == 3:
            table = self.ui_tw_3
        elif self.tip == 4:
            table = self.ui_tw_4
        else:
            return

        query = """SELECT supply_date, supply_provider, type_material, sertificat, type_pack,
                           supply_value, supply_date, audit_location, audit_date, quality
                    FROM audit WHERE type_supply = %s ORDER BY audit_date"""
        sql_info = my_sql.sql_select(query, (self.tip, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql при получении информации", sql_info.msg, QMessageBox.Ok)
            return False

        table.clearContents()
        table.setRowCount(len(sql_info))
        for row, data in enumerate(sql_info):
            item = QTableWidgetItem(data[0].strftime("%d.%m.%Y"))
            table.setItem(row, 0, item)

            item = QTableWidgetItem(data[1])
            table.setItem(row, 1, item)

            item = QTableWidgetItem(data[2])
            table.setItem(row, 2, item)

            item = QTableWidgetItem(data[3])
            table.setItem(row, 3, item)

            item = QTableWidgetItem(data[4])
            table.setItem(row, 4, item)

            item = QTableWidgetItem(str(data[5]))
            table.setItem(row, 5, item)

            item = QTableWidgetItem(data[6].strftime("%m.%Y"))
            table.setItem(row, 6, item)

            item = QTableWidgetItem(data[7])
            table.setItem(row, 7, item)

            item = QTableWidgetItem(data[8].strftime("%d.%m.%Y"))
            table.setItem(row, 8, item)

            item = QTableWidgetItem(data[9])
            table.setItem(row, 9, item)

    def ui_change_type(self, tab):
        self.tip = tab
        self.update()

    def ui_add(self):
        act_window = AuditAct(self.tip)
        act_window.show()
        act_window.setModal(True)
        act_window.exec()

    def ui_generate(self):
        act_window = AuditGeneration(self.tip)
        act_window.show()
        act_window.setModal(True)
        act_window.exec()


class AuditAct(QDialog):
    def __init__(self, tip, act_id=None):
        """
        tip: Тип материала 0-ткань 1++ - фурнитура
        """
        super(AuditAct, self).__init__()
        loadUi(getcwd() + '/ui/audit_act.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.tip = tip

    def ui_viev_supply_list(self):
        if self.tip == 0:
            self.supply_list = MaterialSupplyList(self, dc_select=True)
            self.supply_list.show()

    def of_select_material_supply(self, data):
        self.ui_le_supply.setText(data[0])


class AuditGeneration(QDialog):
    def __init__(self, tip):
        """
        tip: Тип материала 0-ткань 1++ - фурнитура
        """
        super(AuditGeneration, self).__init__()
        loadUi(getcwd() + '/ui/audit_generation.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.tip = tip
        self.provider_id = None
        self.new_table = None

    def ui_view_provider(self):
        if self.tip == 0:
            self.provider_window = ProviderMaterial(self, True)
        else:
            self.provider_window = ProviderAccessories(self, True)

        self.provider_window.show()

    def ui_acc(self):
        if not self.provider_id:
            QMessageBox.critical(self, "Ошибка ID", "Выберите поставщика", QMessageBox.Ok)
            return

        if (not self.ui_le_density_from.text() or not self.ui_le_density_to.text()) and self.tip == 0:
            QMessageBox.critical(self, "Ошибка плотности", "Введите плотность ткани", QMessageBox.Ok)
            return

        date_from = self.ui_de_from.date().toPyDate()
        date_to = self.ui_de_to.date().toPyDate()

        if self.tip == 0:
            query = """SELECT material_supply.Id, material_supply.Data, material_supply.Note, SUM(msp.Weight)
                        FROM material_supply LEFT JOIN material_supplyposition msp on material_supply.Id = msp.Material_SupplyId
                        WHERE material_supply.Material_ProviderId = %s AND material_supply.Data BETWEEN %s AND %s
                        GROUP BY material_supply.Id"""
            sql_info = my_sql.sql_select(query, (self.provider_id, date_from, date_to))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql при получении информации", sql_info.msg, QMessageBox.Ok)
                return False
        else:
            query = """SELECT accessories_supply.Id, accessories_supply.Data, accessories_supply.Note, SUM(msp.Value)
                                    FROM accessories_supply LEFT JOIN accessories_supplyposition msp on accessories_supply.Id = msp.accessories_SupplyId
                                    WHERE accessories_supply.accessories_ProviderId = %s AND accessories_supply.Data BETWEEN %s AND %s
                                    GROUP BY accessories_supply.Id"""
            sql_info = my_sql.sql_select(query, (self.provider_id, date_from, date_to))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql при получении информации", sql_info.msg, QMessageBox.Ok)
                return False

        new_audit = []
        for supply in sql_info:
            if self.tip == 0:
                density = random.randint(int(self.ui_le_density_from.text()), int(self.ui_le_density_to.text()))
            else:
                density = None

            new_row = [
                supply[0],
                self.tip,
                supply[1],
                self.ui_le_sertificat.text(),
                self.ui_le_type_pack.text(),
                random.randint(1, 4),
                self.ui_le_audit_location.text(),
                self.ui_cb_quality.currentText(),
                self.ui_le_workers.text(),
                self.ui_le_provider.text(),
                supply[1],
                supply[2],
                self.ui_le_type_material.text(),
                supply[3],
                self.ui_le_gost.text(),
                density
            ]

            new_audit.append(new_row)

        if new_audit:
            self.new_table = new_audit
            self.set_table(new_audit)
            self.pushButton_3.setEnabled(True)

    def ui_save_sql(self):
        for row in self.new_table:
            query = """INSERT INTO audit (supply_id, type_supply, audit_date, sertificat,
                                          type_pack, audit_value, audit_location, quality, workers, supply_provider,
                                          supply_date, supply_act, type_material, supply_value, gost, density)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            sql_info = my_sql.sql_change(query, row)
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql при сохранении", sql_info.msg, QMessageBox.Ok)
                return False

        self.done(1)
        self.close()
        self.destroy()

    def ui_can(self):
        self.done(0)
        self.close()
        self.destroy()

    def set_table(self, data):
        self.ui_tw_generate.setColumnCount(len(data[0]))
        self.ui_tw_generate.setRowCount(len(data))

        for row, data_row in enumerate(data):
            for col, data in enumerate(data_row):
                item = QTableWidgetItem(str(data))
                self.ui_tw_generate.setItem(row, col, item)

    def of_list_reason_provider_material(self, item):
        self.ui_le_provider.setText(item[1])
        self.provider_id = item[0]

        self.pushButton_2.setEnabled(True)

    def of_list_reason_provider_accessories(self, item):
        self.ui_le_provider.setText(item[1])
        self.provider_id = item[0]

        self.pushButton_2.setEnabled(True)