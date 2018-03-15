from os import getcwd
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from function import my_sql


class TransactionWarehouse(QMainWindow):
    def __init__(self):
        super(TransactionWarehouse, self).__init__()
        loadUi(getcwd() + '/ui/transaction_warehouse.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.set_start_settings()

    def set_start_settings(self):
        self.de_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_to.setDate(QDate.currentDate())

        self.tw_product.horizontalHeader().resizeSection(0, 40)
        self.tw_product.horizontalHeader().resizeSection(1, 100)
        self.tw_product.horizontalHeader().resizeSection(2, 60)
        self.tw_product.horizontalHeader().resizeSection(3, 200)

    def ui_calc(self):
        if self.tabWidget.currentIndex() == 2:
            query = self.where_product()
            sql_info = my_sql.sql_select(query, (self.de_date_from.date().toPyDate(), self.de_date_to.date().toPyDate()))
            if "mysql.connector.errors" in str(type(sql_info)):
                QMessageBox.critical(self, "Ошибка sql получения транзакций продукта", sql_info.msg, QMessageBox.Ok)
                return False

            table = self.tw_product

            table.clearContents()
            table.setRowCount(0)

            all_balance = 0

            for transaction in sql_info:
                table.insertRow(table.rowCount())

                item = QTableWidgetItem(str(transaction[0]))
                table.setItem(table.rowCount() - 1, 0, item)

                item = QTableWidgetItem(transaction[1].strftime("%d.%m.%Y %H:%M:%S"))
                table.setItem(table.rowCount() - 1, 1, item)

                all_balance += transaction[2]
                item = QTableWidgetItem(str(transaction[2]))
                table.setItem(table.rowCount() - 1, 2, item)

                item = QTableWidgetItem(str(transaction[3]))
                table.setItem(table.rowCount() - 1, 3, item)

            else:
                table.insertRow(table.rowCount())

                item = QTableWidgetItem(str(all_balance))
                table.setItem(table.rowCount() - 1, 2, item)

    def where_product(self):
        query = "SELECT Id, Date, Balance, Note FROM transaction_records_warehouse WHERE Date >= %s AND Date <= %s"
        where = ""

        #  Блок остального
        if self.gb_product_other.isChecked():
            if self.cb_product_other_other.isChecked():
                where = self.add_filter(where, "Note NOT LIKE 'Заказ % - %' AND Note NOT LIKE '%/% - %'")
                query += " AND (" + where + ")"
                return query  # Сразу делаем возврат так как это исключающее условие

        #  Блок пачек
        if self.gb_product_pack.isChecked():
            where_and = ""
            if self.cb_product_pack_in.isChecked():
                where_and = self.add_filter(where_and, "Note LIKE '% - Принята пачка'", and_add=False)

            if self.cb_product_pack_out.isChecked():
                where_and = self.add_filter(where_and, "Note LIKE '% - ачка вернулась со склада'", and_add=False)

            if self.cb_product_pack_change.isChecked():
                where_and = self.add_filter(where_and, "Note LIKE '% - Изменено кол-во принятой пачки'", and_add=False)

            if where_and:
                if where:
                    where = where + " OR (" + where_and + ")"
                else:
                    where = where + " (" + where_and + ")"

        #  Блок заказов
        if self.gb_product_order.isChecked():
            where_and = ""
            if self.cb_product_order_shipped.isChecked():
                where_and = self.add_filter(where_and, "Note LIKE '% - отгружен'", and_add=False)

            if self.cb_product_order_cancel.isChecked():
                where_and = self.add_filter(where_and, "Note LIKE '% - отменен'", and_add=False)

            if where_and:
                if where:
                    where = where + " OR (" + where_and + ")"
                else:
                    where = where + " (" + where_and + ")"

        #  Блок знаковости транзакций
        if self.gb_product_sign.isChecked():
            where_and = ""
            if self.cb_product_sign_plus.isChecked():
                where_and = self.add_filter(where_and, "Balance > 0", and_add=False)

            if self.cb_product_sign_minus.isChecked():
                where_and = self.add_filter(where_and, "Balance < 0", and_add=False)

            if self.cb_product_sign_nul.isChecked():
                where_and = self.add_filter(where_and, "Balance = 0", and_add=False)

            if where_and:
                if where:
                    where = where + " AND (" + where_and + ")"
                else:
                    where = where + " (" + where_and + ")"

        if where:
            query += " AND (" + where + ")"

        return query

    def add_filter(self, where, add, and_add=True):
        if where:
            if and_add:
                where += " AND " + add
            else:
                where += " OR " + add
        else:
            where = add

        return where