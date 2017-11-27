from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QBrush, QColor
import re
from function import my_sql
from function import table_to_html, to_excel
from classes import print_qt


report_reject_class = loadUiType(getcwd() + '/ui/report_reject.ui')[0]


class ReportReject(QMainWindow, report_reject_class):
    def __init__(self):
        super(ReportReject, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

        self.tableWidget.horizontalHeader().resizeSection(0, 150)
        self.tableWidget.horizontalHeader().resizeSection(1, 60)
        self.tableWidget.horizontalHeader().resizeSection(2, 60)
        self.tableWidget.horizontalHeader().resizeSection(3, 60)
        self.tableWidget.horizontalHeader().resizeSection(4, 60)
        self.tableWidget.horizontalHeader().resizeSection(5, 75)

    def ui_calc(self):

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        query = """SELECT product_article_parametrs.Id, CONCAT(product_article.Article, '(', product_article_size.Size, ')[', product_article_parametrs.Name, ']'),
                      SUM(pack.Value_Pieces + pack.Value_Damage), SUM(pack.Value_Damage), (SUM(pack.Value_Damage) * 100 / SUM(pack.Value_Pieces + pack.Value_Damage))
                      FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE pack.Value_Damage != 0 AND cut.Date_Cut >= %s AND cut.Date_Cut <= %s
                      GROUP BY product_article_parametrs.Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения брака", sql_info.msg, QMessageBox.Ok)
            return False

        all_value, all_value_damage = 0, 0

        for article in sql_info:

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            item = QTableWidgetItem(article[1])
            item.setData(5, article[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            all_value += article[2]
            item = QTableWidgetItem(str(article[2]))
            item.setData(5, article[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            all_value_damage += article[3]
            item = QTableWidgetItem(str(article[3]))
            item.setData(5, article[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            item = QTableWidgetItem(str(round(article[4], 4)))
            item.setData(5, article[0])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

        else:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            item = QTableWidgetItem(str(all_value))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            item = QTableWidgetItem(str(all_value_damage))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            avg = all_value_damage * 100 / all_value
            item = QTableWidgetItem(str(round(avg, 4)))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

            self.pb_calc_sum.setEnabled(True)

    def ui_calc_sum(self):
        # Получаем id разных пачек для подсчета
        all_sum = 0
        for row in range(self.tableWidget.rowCount() - 1):
            key = self.tableWidget.item(row, 0).data(5)
            value_pc = int(self.tableWidget.item(row, 1).text())

            self.statusBar.showMessage("Расчет ID артикула %s" % key)

            query = """SELECT pack.Id FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id JOIN (SELECT @sum := 0) t
                          WHERE pack.Article_Parametr_Id = %s AND cut.Date_Cut <= %s AND (@sum := @sum + pack.Value_Pieces) <= %s"""
            sql_pack_id_info = my_sql.sql_select(query, (key, self.de_date_to.date().toPyDate(), value_pc + 200))
            if "mysql.connector.errors" in str(type(sql_pack_id_info)):
                QMessageBox.critical(self, "Ошибка sql получения id пачек для артикула", sql_pack_id_info.msg, QMessageBox.Ok)
                return False

            v = int(len(sql_pack_id_info)/5) + 1

            sebest_pack_list = []
            if sql_pack_id_info:  # Если найдены предыдущие кроя!
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
                                          SELECT ((pack_add_material.Weight + pack_add_material.Weight_Rest) / pack.Value_Pieces) * pack_add_material.Price
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
                        QMessageBox.critical(self, "Ошибка sql получения средней цены ткани для кроя", sql_info.msg, QMessageBox.Ok)
                        return False

                    sebest_pack_list.append(sum([0 if i is None else i for i in sql_info[0]]))

                # Находим среднюю себестоимость на артикул
                if sebest_pack_list:
                    seb = round(sum(sebest_pack_list) / len(sebest_pack_list), 4)
                else:
                    seb = None

                item = QTableWidgetItem(str(seb))
                self.tableWidget.setItem(row, 4, item)

                value_dmg = int(self.tableWidget.item(row, 2).text())
                all_sum += seb * value_dmg
                item = QTableWidgetItem(str(seb * value_dmg))
                self.tableWidget.setItem(row, 5, item)

        else:
            item = QTableWidgetItem(str(all_sum))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, item)

