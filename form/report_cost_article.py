from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, Qt
from form import article
from function import my_sql, to_excel, table_to_html
from classes import print_qt
from decimal import Decimal
import datetime
import re

report_cost_article = loadUiType(getcwd() + '/ui/report_cost_article.ui')[0]


class ReportCostArticle(QMainWindow, report_cost_article):
    def __init__(self):
        super(ReportCostArticle, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_table_size()

    def set_table_size(self):
        self.tableWidget.horizontalHeader().resizeSection(0, 65)
        self.tableWidget.horizontalHeader().resizeSection(1, 50)
        self.tableWidget.horizontalHeader().resizeSection(2, 110)
        self.tableWidget.horizontalHeader().resizeSection(3, 70)
        self.tableWidget.horizontalHeader().resizeSection(4, 70)
        self.tableWidget.horizontalHeader().resizeSection(5, 70)
        self.tableWidget.horizontalHeader().resizeSection(6, 85)

    def ui_view_article(self):
        self.article_list = article.ArticleList(self, True)
        self.article_list.setWindowModality(Qt.ApplicationModal)
        self.article_list.show()

    def ui_calc_cost(self):
        query = """SELECT product_article.Article, product_article_size.Size, product_article_parametrs.Name,
                    (SELECT SUM(operations.Price)
                      FROM product_article_operation LEFT JOIN operations ON product_article_operation.Operation_Id = operations.Id
                      WHERE product_article_operation.Product_Article_Parametrs_Id = product_article_parametrs.Id),
                    (SELECT material_supplyposition.Price * product_article_material.Value
                      FROM product_article_material LEFT JOIN material_name ON product_article_material.Material_Id = material_name.Id
                        LEFT JOIN material_supplyposition ON material_name.Id = material_supplyposition.Material_NameId
                        LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                        LEFT JOIN material_balance ON material_supplyposition.Id = material_balance.Material_SupplyPositionId
                      WHERE product_article_material.Product_Article_Parametrs_Id = product_article_parametrs.Id AND product_article_material.Material_Id IS NOT NULL
                        AND material_balance.BalanceWeight > 0
                      ORDER BY material_supply.Data LIMIT 1),
                    (SELECT SUM(product_article_material.Value * (SELECT accessories_supplyposition.Price
                                              FROM accessories_supplyposition LEFT JOIN accessories_supply ON accessories_supplyposition.Accessories_SupplyId = accessories_supply.Id
                                                  LEFT JOIN accessories_balance ON accessories_supplyposition.Id = accessories_balance.Accessories_SupplyPositionId
                                                WHERE accessories_supplyposition.Accessories_NameId = accessories_name.Id AND accessories_balance.BalanceValue > 0
                                                ORDER BY accessories_supply.Data LIMIT 1))
                      FROM product_article_material LEFT JOIN accessories_name ON product_article_material.Accessories_Id = accessories_name.Id
                      WHERE product_article_material.Product_Article_Parametrs_Id = product_article_parametrs.Id AND product_article_material.Accessories_Id IS NOT NULL)
                  FROM product_article LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id
                    LEFT JOIN product_article_parametrs ON product_article_size.Id = product_article_parametrs.Product_Article_Size_Id"""


        if self.le_article.text():
            query += " WHERE product_article.Id = %s" % self.le_article.whatsThis()

        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получение приходов материала", sql_info.msg, QMessageBox.Ok)
                return False

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        if not sql_info:
            return False

        row = 0
        all_sum = 0
        for material in sql_info:
            self.tableWidget.insertRow(row)

            item = QTableWidgetItem(material[0])
            self.tableWidget.setItem(row, 0, item)

            item = QTableWidgetItem(str(material[1]))
            self.tableWidget.setItem(row, 1, item)

            item = QTableWidgetItem(str(material[2]))
            self.tableWidget.setItem(row, 2, item)

            if material[3]:
                text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(material[3], 2)))
            else:
                text = "N O N E"
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(row, 3, item)

            if material[4]:
                text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(material[4], 2)))
            else:
                text = "N O N E"
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(row, 4, item)

            if material[5]:
                text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(material[5], 2)))
            else:
                text = "N O N E"
            item = QTableWidgetItem(text)
            self.tableWidget.setItem(row, 5, item)

            try:
                sum = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round( material[3] + material[4] + material[5], 2)))
            except:
                sum = "N O N E"
            item = QTableWidgetItem(sum)
            self.tableWidget.setItem(row, 6, item)

            row += 1

    def of_tree_select_article(self, article):
        self.article_list.close()
        self.article_list.destroy()
        self.le_article.setText(article["article"])
        self.le_article.setWhatsThis(str(article["article_id"]))