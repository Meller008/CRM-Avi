from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QBrush, QColor
import re
from function import my_sql
from function import table_to_html, to_excel
from classes import print_qt


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

        self.tableWidget.horizontalHeader().resizeSection(0, 150)
        self.tableWidget.horizontalHeader().resizeSection(1, 70)
        self.tableWidget.horizontalHeader().resizeSection(2, 90)
        self.tableWidget.horizontalHeader().resizeSection(3, 80)
        self.tableWidget.horizontalHeader().resizeSection(4, 80)

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

        # Получаем id разных пачек для подсчета
        for key, value in article_list.items():

            self.statusBar.showMessage("Расчет артикула %s" % article_list[key]["name"])

            query = """SELECT pack.Id FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id JOIN (SELECT @sum := 0) t
                          WHERE pack.Article_Parametr_Id = %s AND cut.Date_Cut <= %s AND (@sum := @sum + pack.Value_Pieces) <= %s"""
            sql_pack_id_info = my_sql.sql_select(query, (key, self.de_date_to.date().toPyDate(), value["value"] + 200))
            if "mysql.connector.errors" in str(type(sql_pack_id_info)):
                QMessageBox.critical(self, "Ошибка sql получения id пачек для артикула", sql_pack_id_info.msg, QMessageBox.Ok)
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
                    article_list[key]["seb"] = sum(sebest_pack_list) / len(sebest_pack_list)
                else:
                    article_list[key]["seb"] = None

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
                else:
                    article_list[key]["seb"] = 0
                    article_list[key]["name"] = "Б/К " + article_list[key]["name"]

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            # Вставляем расчитаный артикул
            # Цвет зависит от положительной или отрицательной прибыли
            if article_list[key]["seb"]:
                profit = (article_list[key]["sum"] - (article_list[key]["seb"] * article_list[key]["value"]))
                if profit > 0:
                    color = QBrush(QColor(150, 255, 161, 255))
                else:
                    color = QBrush(QColor(255, 255, 153, 255))
            else:
                color = QBrush(QColor(252, 141, 141, 255))

            item = QTableWidgetItem(article_list[key]["name"])
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(article_list[key]["value"]))
            item = QTableWidgetItem(text)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["sum"], 4)))
            item = QTableWidgetItem(text)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            if article_list[key]["seb"]:
                text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["seb"], 4)))
            else:
                text = "None"
            item = QTableWidgetItem(text)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

            if article_list[key]["seb"]:
                text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(profit, 4)))
            else:
                text = "None"
            item = QTableWidgetItem(text)
            item.setBackground(color)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

    def ui_calc_sum(self):
        value_sum, sold_sum, seb_sum = 0, 0, 0
        for row in range(self.tableWidget.rowCount()):
            value_row = int(self.tableWidget.item(row, 1).text().replace(" ", ""))
            sold_row = float(self.tableWidget.item(row, 2).text().replace(" ", ""))
            value_sum += value_row
            sold_sum += sold_row

            if self.tableWidget.item(row, 3).text() != "None":
                try:
                    seb_row = float(self.tableWidget.item(row, 3).text().replace(",", ".").replace(" ", ""))
                    seb_sum += (value_row * seb_row)
                except:
                    QMessageBox.critical(self, "Ошибка Себестоимости", "Ошибка в артикуле %s" % self.tableWidget.item(row, 0).text(), QMessageBox.Ok)
                    return False
        self.le_value_sum.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(value_sum, 4))))
        self.le_sold_sum.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sold_sum, 4))))
        self.le_seb_sum.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(seb_sum, 4))))
        self.le_profit_sum.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sold_sum - seb_sum, 4))))

    def ui_print(self):
        up_html = """
          <table>
          <tr> <th>Продано товара</th><th>На сумму</th><th>Затрачено рублей</th><th>ИТОГО прибыль</th> </tr>
          <tr> <td>#value_sum#</td><td>#sold_sum#</td><td>#seb_sum#</td><td>#all_sum#</td> </tr>
          </table>"""
        up_html = up_html.replace("#value_sum#", self.le_value_sum.text())
        up_html = up_html.replace("#sold_sum#", self.le_sold_sum.text())
        up_html = up_html.replace("#seb_sum#", self.le_seb_sum.text())
        up_html = up_html.replace("#all_sum#", self.le_profit_sum.text())

        head = "Прибыль предприятия %s-%s" % (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate))

        html = table_to_html.tab_html(self.tableWidget, table_head=head, up_template=up_html)
        self.print_class = print_qt.PrintHtml(self, html)

    def ui_export(self):
        path = QFileDialog.getSaveFileName(self, "Сохранение")
        if path[0]:
            to_excel.table_to_excel(self.tableWidget, path[0])
