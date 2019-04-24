from os import getcwd
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
import re
from function import my_sql
from function import table_to_html
from classes import print_qt


class ReportPerformanceCompany(QMainWindow):
    def __init__(self):
        super(ReportPerformanceCompany, self).__init__()
        loadUi(getcwd() + '/ui/report_performance_company.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

        self.tableWidget.horizontalHeader().resizeSection(0, 150)
        self.tableWidget.horizontalHeader().resizeSection(1, 80)
        self.tableWidget.horizontalHeader().resizeSection(2, 80)
        self.tableWidget.horizontalHeader().resizeSection(3, 100)

    def ui_calc(self):
        date = (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate())

        query = """SELECT COUNT(cut.Id) FROM cut WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s"""
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения кол-ва кроев", sql_info.msg, QMessageBox.Ok)
            return False
        
        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0]))
        self.le_cut.setText(text)

        query = """SELECT COUNT(pack.Id) FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s"""
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения кол-ва пачек", sql_info.msg, QMessageBox.Ok)
            return False

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0]))
        self.le_pack.setText(text)

        query = """SELECT COUNT(pack_operation.Id) FROM pack_operation
                      LEFT JOIN pack ON pack_operation.Pack_Id = pack.Id LEFT JOIN cut ON pack.Cut_Id = cut.Id WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s"""
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения кол-ва операций", sql_info.msg, QMessageBox.Ok)
            return False

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0]))
        self.le_operation.setText(text)

        query = """SELECT SUM(pack.Value_Pieces - pack.Value_Damage) FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s"""
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения кол-ва изделий", sql_info.msg, QMessageBox.Ok)
            return False

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0]))
        self.le_product.setText(text)

        query = """SELECT SUM(pack.Value_Damage) FROM pack LEFT JOIN cut ON pack.Cut_Id = cut.Id WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s"""
        sql_info = my_sql.sql_select(query, date)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения кол-ва брака", sql_info.msg, QMessageBox.Ok)
            return False

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(sql_info[0][0]))
        self.le_damage.setText(text)

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        article_list = {}

        query = """SELECT product_article_parametrs.Id, CONCAT(product_article.Article, '(', product_article_size.Size, ')[', product_article_parametrs.Name, ']'),
                        SUM(pack.Value_Pieces - pack.Value_Damage)
                      FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                        LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                        LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                        LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id
                      WHERE cut.Date_Cut >= %s AND cut.Date_Cut <= %s AND product_article_parametrs.Id IS NOT NULL 
                      GROUP BY product_article_parametrs.Id"""
        sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения покроеных пачек", sql_info.msg, QMessageBox.Ok)
            return False

        for order_position in sql_info:
            if article_list.get(order_position[0]) is None:
                article_list.update({order_position[0]: {"value": order_position[2], "sum": 0, "seb": None, "name": order_position[1]}})

        all_value, all_sum = 0, 0

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
                                          SELECT SUM(((pack_add_material.Weight + pack_add_material.Weight_Rest) / pack.Value_Pieces) * pack_add_material.Price)
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
                    article_list[key]["sum"] = article_list[key]["seb"] * article_list[key]["value"]
                else:
                    article_list[key]["seb"] = None
                    article_list[key]["sum"] = None

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            # Вставляем расчитаный артикул
            # Цвет зависит от положительной или отрицательной прибыли
            item = QTableWidgetItem(article_list[key]["name"])
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

            all_value += article_list[key]["value"]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(article_list[key]["value"]))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            if article_list[key]["seb"]:
                text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["seb"], 4)))
            else:
                text = "None"
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)

            all_sum += article_list[key]["sum"]
            if article_list[key]["sum"]:
                text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(article_list[key]["sum"], 4)))
            else:
                text = "None"
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

        else:
            self.tableWidget.insertRow(self.tableWidget.rowCount())

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(all_value))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)

            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum, 4)))
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)

            self.le_sum.setText(text)

    def ui_print(self):
        up_html = """
          <table>
          <tr> <th>Кроев</th><th>Пачек</th><th>Операций</th><th>Готовых изделий</th><th>Брака</th><th>На сумму (покроеную)</th> </tr>
          <tr> <th>#le_cut#</th><th>#le_pack#</th><th>#le_operation#</th><th>#le_product#</th><th>#le_damage#</th><th>#le_sum#</th> </tr>
          </table>"""
        up_html = up_html.replace("#le_cut#", self.le_cut.text())
        up_html = up_html.replace("#le_pack#", self.le_pack.text())
        up_html = up_html.replace("#le_operation#", self.le_operation.text())
        up_html = up_html.replace("#le_product#", self.le_product.text())
        up_html = up_html.replace("#le_damage#", self.le_damage.text())
        up_html = up_html.replace("#le_sum#", self.le_sum.text())

        head = "Произведено компанией %s - %s" % (self.de_date_from.date().toString(Qt.ISODate), self.de_date_to.date().toString(Qt.ISODate))

        html = table_to_html.tab_html(self.tableWidget, table_head=head, up_template=up_html)
        self.print_class = print_qt.PrintHtml(self, html)

