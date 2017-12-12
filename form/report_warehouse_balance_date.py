from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
import re
from function import my_sql
from function import table_to_html
from classes import print_qt


report_warehouse_balance_date_class = loadUiType(getcwd() + '/ui/report_warehouse_balance_date.ui')[0]


class ReportWarehouseBalanceDate(QMainWindow, report_warehouse_balance_date_class):
    def __init__(self):
        super(ReportWarehouseBalanceDate, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.de_date_to.setDate(QDate.currentDate())

        self.tableWidget.horizontalHeader().resizeSection(0, 150)
        self.tableWidget.horizontalHeader().resizeSection(1, 65)
        self.tableWidget.horizontalHeader().resizeSection(2, 70)
        self.tableWidget.horizontalHeader().resizeSection(3, 70)
        self.tableWidget.horizontalHeader().resizeSection(4, 95)
        self.tableWidget.horizontalHeader().resizeSection(5, 95)
        self.tableWidget.horizontalHeader().resizeSection(6, 70)
        self.tableWidget.horizontalHeader().resizeSection(7, 95)
        self.tableWidget.horizontalHeader().resizeSection(8, 95)

    def ui_calc(self):

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        query = """SELECT SUM(trm.Balance), SUM(trm.Balance * material_supplyposition.Price) AS sum_m
                      FROM transaction_records_material AS trm LEFT JOIN material_balance ON trm.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                        LEFT JOIN cut ON trm.Cut_Material_Id = cut.Id
                        LEFT JOIN beika ON trm.Beika_Id = beika.Id
                      WHERE cut.Date_Cut <= %s OR trm.Date <= DATE_FORMAT(%s,'%Y-%m-%d 23:59:59') OR beika.Date <= %s"""
        sql_info = my_sql.sql_select(query, (self.de_date_to.date().toPyDate(), self.de_date_to.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения остатков ткани", sql_info.msg, QMessageBox.Ok)
            return False
        self.le_material_balance.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0])))
        self.le_material_sum.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][1])))

        query = """SELECT SUM(tra.Balance), SUM(tra.Balance * accessories_supplyposition.Price) AS sum_m
                      FROM transaction_records_accessories AS tra LEFT JOIN accessories_balance ON tra.Supply_Balance_Id = accessories_balance.Id
                        LEFT JOIN accessories_supplyposition ON accessories_balance.Accessories_SupplyPositionId = accessories_supplyposition.Id
                        LEFT JOIN pack_accessories ON tra.Pack_Accessories_Id = pack_accessories.Id
                        LEFT JOIN pack ON pack_accessories.Pack_Id = pack.Id
                        LEFT JOIN cut ON pack.Cut_Id = cut.Id
                      WHERE cut.Date_Cut <= %s OR tra.Date <= DATE_FORMAT(%s,'%Y-%m-%d 23:59:59')"""
        sql_info = my_sql.sql_select(query, (self.de_date_to.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения остатков фурнитуры", sql_info.msg, QMessageBox.Ok)
            return False

        self.le_accessories_balance.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0])))
        self.le_accessories_sum.setText(re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][1])))

        # Получаем пртикула
        article_list = {}
        query = """SELECT product_article_parametrs.Id, CONCAT(product_article.Article, '(', product_article_size.Size, ')[', product_article_parametrs.Name, ']'),
                        product_article_parametrs.Price,
                        war.Value_In_Warehouse - IFNULL((SELECT SUM(transaction_records_warehouse.Balance) FROM transaction_records_warehouse
                                                          WHERE transaction_records_warehouse.Article_Parametr_Id = war.Id_Article_Parametr
                                                            AND transaction_records_warehouse.Date > %s), 0)
                      FROM product_article_warehouse AS war
                        LEFT JOIN product_article_parametrs ON war.Id_Article_Parametr = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_to.date().toPyDate(), ))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения артикулов склада", sql_info.msg, QMessageBox.Ok)
            return False

        # добавляем артикула в словарь
        for article in sql_info:
            article_list.update({article[0]: {"warehouse_value": article[3], "cut_value": 0, "seb": None, "price": article[2], "name": article[1]}})

        # Смотрим сколько еще артикулов было в цеху на эту дату
        query = """SELECT product_article_parametrs.Id, SUM(pack.Value_Pieces)
                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                      LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                      WHERE cut.Date_Cut <= %s AND (pack.Date_Make > %s OR pack.Date_Make IS NULL) GROUP BY product_article_parametrs.Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_to.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения артикулов в цеху", sql_info.msg, QMessageBox.Ok)
            return False

        for article in sql_info:
            article_list[article[0]]["cut_value"] = article[1]

        # Считаем себестоимость
        all_warehouse, all_warehouse_seb, all_warehouse_price = 0, 0, 0
        all_cut, all_cut_seb, all_cut_price = 0, 0, 0
        for key, value in article_list.items():

            self.statusBar.showMessage("Расчет артикула %s" % article_list[key]["name"])

            if article_list[key]["warehouse_value"] == 0 and article_list[key]["cut_value"] == 0:
                continue

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

            if sql_info[0][0]:
                article_list[key]["seb"] = sql_info[0][0] + sql_info[0][1] + sql_info[0][2]
            else:
                article_list[key]["seb"] = 0

            # Вставляем расчитаный артикул
            self.tableWidget.insertRow(self.tableWidget.rowCount())

            seb = article_list[key]["seb"]
            price = article_list[key]["price"]

            item = QTableWidgetItem(article_list[key]["name"])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            item = QTableWidgetItem(str(round(seb, 4)))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            item = QTableWidgetItem(str(price))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            all_warehouse += article_list[key]["warehouse_value"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(article_list[key]["warehouse_value"]))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

            all_warehouse_price += article_list[key]["warehouse_value"] * price
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["warehouse_value"] * price, 4)))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

            all_warehouse_seb += article_list[key]["warehouse_value"] * seb
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["warehouse_value"] * seb, 4)))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, item)

            all_cut += article_list[key]["cut_value"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(article_list[key]["cut_value"]))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 6, item)

            all_cut_price += article_list[key]["cut_value"] * price
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["cut_value"] * price, 4)))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 7, item)

            all_cut_seb += article_list[key]["cut_value"] * seb
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["cut_value"] * seb, 4)))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 8, item)

        else:
            self.tableWidget.insertRow(self.tableWidget.rowCount())

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_warehouse))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_warehouse_price, 4)))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_warehouse_seb, 4)))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_cut))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 6, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_cut_price, 4)))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 7, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_cut_seb, 4)))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 8, item)

    def ui_print(self):
        up_html = """
          <table>
          <tr> <th>Остаток ткани</th><th>На сумму</th><th>Остаток фурнитуры</th><th>На сумму</th> </tr>
          <tr> <td>#material_balance#</td><td>#material_sum#</td><td>#accessories_balance#</td><td>#accessories_sum#</td> </tr>
          </table>"""
        up_html = up_html.replace("#material_balance#", self.le_material_balance.text())
        up_html = up_html.replace("#material_sum#", self.le_material_sum.text())
        up_html = up_html.replace("#accessories_balance#", self.le_accessories_balance.text())
        up_html = up_html.replace("#accessories_sum#", self.le_accessories_sum.text())

        head = "Остаток склада на %s" % (self.de_date_to.date().toString(Qt.ISODate))

        html = table_to_html.tab_html(self.tableWidget, table_head=head, up_template=up_html)
        self.print_class = print_qt.PrintHtml(self, html)
