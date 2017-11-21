from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
import re
from decimal import Decimal
import datetime
from function import my_sql
from form.templates import table

import time


report_profit_class = loadUiType(getcwd() + '/ui/report_profit.ui')[0]


class ReportProfit(QMainWindow, report_profit_class):
    def __init__(self):
        super(ReportProfit, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

    def ui_calc(self):

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        article_list = {}

        query = """SELECT product_article_parametrs.Id, CONCAT(product_article.Article, '(', product_article_size.Size, ')[', product_article_parametrs.Name, ']'),
                        order_position.Value, IF(clients.No_Nds, order_position.Price * (order_position.NDS / 100 + 1),order_position.Price)
                      FROM order_position LEFT JOIN `order` ON order_position.Order_Id = `order`.Id
                        LEFT JOIN clients ON `order`.Client_Id = clients.Id
                        LEFT JOIN product_article_parametrs ON order_position.Product_Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE `order`.Date_Shipment >= %s AND `order`.Date_Shipment <= %s"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения проданых позиций", sql_info.msg, QMessageBox.Ok)
            return False

        for order_position in sql_info:
            if article_list.get(order_position[0]) is None:
                article_list.update({order_position[0]: {"value": 0, "sum": 0, "seb": None, "name": order_position[1]}})

            article_list[order_position[0]]["value"] += order_position[2]
            article_list[order_position[0]]["sum"] += order_position[2] * order_position[3]

        a = time.time()

        # Получаем id разных пачек для подсчета
        for key, value in article_list.items():
            query = """SELECT pack.Id FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id JOIN (SELECT @sum := 0) t
                          WHERE pack.Article_Parametr_Id = %s AND cut.Date_Cut <= %s AND (@sum := @sum + pack.Value_Pieces) <= %s"""
            sql_pack_id_info = my_sql.sql_select(query, (key, self.de_date_to.date().toPyDate(), value["value"] + 200))
            if "mysql.connector.errors" in str(type(sql_pack_id_info)):
                QMessageBox.critical(self, "Ошибка sql получения id пачек для артикула", sql_pack_id_info.msg, QMessageBox.Ok)
                return False

            v = int(len(sql_pack_id_info)/5) + 1

            sebest_pack_list = []

            for i in range(len(sql_pack_id_info)):
                if i % v != 0:
                    continue

                pack_id = sql_pack_id_info[i][0]
                # Узнаем всю себестоимость
                query = """SELECT(
                                  SELECT AVG(DISTINCT material_supplyposition.Price) * (SELECT (pack.Weight * (1 + cut.Rest_Percent / 100)) / Pack_Value
                                                                                        FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id
                                                                                        WHERE pack.Id = pm.Id)
                                  FROM pack LEFT JOIN transaction_records_material ON transaction_records_material.Cut_Material_Id = pack.Cut_Id
                                    LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                                    LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                                  WHERE pack.Id = pm.Id AND transaction_records_material.Note NOT LIKE '%доп. тк%'
                                  ),(
                                      SELECT (Weight + Weight_Rest) * Price FROM pack_add_material WHERE Pack_Id = pm.Id
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
                article_list[key]["seb"] = sum(sebest_pack_list) / len(sebest_pack_list)
            else:
                article_list[key]["seb"] = None

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            item = QTableWidgetItem(article_list[key]["name"])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(article_list[key]["value"]))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["sum"], 2)))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            if article_list[key]["seb"]:
                text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["seb"], 2)))
            else:
                text = "None"
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)




            #     # Узнаем цену ткани кроя (Если перекресная то просто берем среднюю а+б/2)
            #     query = """SELECT AVG(DISTINCT material_supplyposition.Price)
            #                   FROM pack LEFT JOIN transaction_records_material ON transaction_records_material.Cut_Material_Id = pack.Cut_Id
            #                     LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
            #                     LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
            #                   WHERE pack.Id = %s AND transaction_records_material.Note NOT LIKE '%доп. тк%'"""
            #     sql_info = my_sql.sql_select(query, (pack_id, ))
            #     if "mysql.connector.errors" in str(type(sql_info)):
            #         QMessageBox.critical(self, "Ошибка sql получения средней цены ткани для кроя", sql_info.msg, QMessageBox.Ok)
            #         return False
            #
            #     material_price = sql_info[0][0]
            #
            #     # Узнаем вес пачки и % обрези и кол-во в пачке
            #     query = """SELECT pack.Weight, cut.Rest_Percent, pack.Value_Pieces FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id WHERE pack.Id = %s"""
            #     sql_info = my_sql.sql_select(query, (pack_id, ))
            #     if "mysql.connector.errors" in str(type(sql_info)):
            #         QMessageBox.critical(self, "Ошибка sql получения вес пачки и % обрези", sql_info.msg, QMessageBox.Ok)
            #         return False
            #
            #     # Считаем цену за ткань
            #     pack_value = sql_info[0][2]
            #     pack_material_sum = ((sql_info[0][0] * (1 + sql_info[0][1] / 100)) * material_price) / pack_value
            #
            #     # Считаем доп. ткань
            #     query = """SELECT (Weight + Weight_Rest) * Price FROM pack_add_material WHERE Pack_Id = %s"""
            #     sql_info = my_sql.sql_select(query, (pack_id, ))
            #     if "mysql.connector.errors" in str(type(sql_info)):
            #         QMessageBox.critical(self, "Ошибка sql получения доп. ткань", sql_info.msg, QMessageBox.Ok)
            #         return False
            #
            #     if sql_info:
            #         pack_a_material_sum = sql_info[0][0] / pack_value
            #     else:
            #         pack_a_material_sum = 0
            #
            #     # Считаем фурнитуру
            #     query = """SELECT SUM(avg) FROM (
            #                   SELECT AVG(accessories_supplyposition.Price) * pack_accessories.Value_Thing AS avg
            #                   FROM pack
            #                     LEFT JOIN pack_accessories ON pack.Id = pack_accessories.Pack_Id
            #                     LEFT JOIN transaction_records_accessories ON transaction_records_accessories.Pack_Accessories_Id = pack_accessories.Id
            #                     LEFT JOIN accessories_balance ON transaction_records_accessories.Supply_Balance_Id = accessories_balance.Id
            #                     LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
            #                   WHERE pack.Id = %s
            #                   GROUP BY pack_accessories.Id) t"""
            #     sql_info = my_sql.sql_select(query, (pack_id, ))
            #     if "mysql.connector.errors" in str(type(sql_info)):
            #         QMessageBox.critical(self, "Ошибка sql получения фурнитуры", sql_info.msg, QMessageBox.Ok)
            #         return False
            #
            #     pack_accessories_sum = sql_info[0][0]
            #
            #     # Считаем операции
            #     query = """SELECT SUM(pack_operation.Price) FROM pack_operation WHERE pack_operation.Pack_Id = %s"""
            #     sql_info = my_sql.sql_select(query, (pack_id, ))
            #     if "mysql.connector.errors" in str(type(sql_info)):
            #         QMessageBox.critical(self, "Ошибка sql получения суммы операций", sql_info.msg, QMessageBox.Ok)
            #         return False
            #
            #     pack_operation_sum = sql_info[0][0]
            #
            #     sebest_pack_list.append((pack_material_sum + pack_a_material_sum + pack_accessories_sum + pack_operation_sum))
            #
            # if sebest_pack_list:
            #     article_list[key]["seb"] = sum(sebest_pack_list) / len(sebest_pack_list)
            # else:
            #     article_list[key]["seb"] = None


        print(time.time() - a)
