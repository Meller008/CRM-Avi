from os import getcwd, path, mkdir, listdir
from form.templates import tree
from form import operation, supply_material, supply_accessories, print_label, article
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QMainWindow, QInputDialog, QTableWidgetItem, QShortcut, QListWidgetItem, QLineEdit, QWidget, QSizePolicy, QProgressDialog
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt, QObject, QDate, QCoreApplication
from function import my_sql, table_to_html
from classes.my_class import User
from classes import print_qt, cut
from decimal import Decimal

sibest_class = loadUiType(getcwd() + '/ui/report_sibestoimost.ui')[0]


class ReportSibestoimost(QMainWindow, sibest_class):
    def __init__(self):
        super(ReportSibestoimost, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_settings()

    def start_settings(self):
        self.de_date_in.setDate(QDate.currentDate().addMonths(-1))
        self.de_date_from.setDate(QDate.currentDate())

        self.table_widget.horizontalHeader().resizeSection(0, 65)
        self.table_widget.horizontalHeader().resizeSection(1, 65)
        self.table_widget.horizontalHeader().resizeSection(2, 35)
        self.table_widget.horizontalHeader().resizeSection(3, 155)
        self.table_widget.horizontalHeader().resizeSection(4, 35)
        self.table_widget.horizontalHeader().resizeSection(5, 35)
        self.table_widget.horizontalHeader().resizeSection(6, 40)
        self.table_widget.horizontalHeader().resizeSection(7, 100)
        self.table_widget.horizontalHeader().resizeSection(8, 70)
        self.table_widget.horizontalHeader().resizeSection(9, 70)
        self.table_widget.horizontalHeader().resizeSection(10, 70)
        self.table_widget.horizontalHeader().resizeSection(11, 70)
        self.table_widget.horizontalHeader().resizeSection(12, 70)
        self.table_widget.horizontalHeader().resizeSection(13, 70)
        self.table_widget.horizontalHeader().resizeSection(14, 70)
        self.table_widget.horizontalHeader().resizeSection(15, 70)
        self.table_widget.horizontalHeader().resizeSection(16, 70)
        self.table_widget.horizontalHeader().resizeSection(17, 70)
        self.table_widget.horizontalHeader().resizeSection(18, 70)
        self.table_widget.horizontalHeader().resizeSection(19, 70)
        self.table_widget.horizontalHeader().resizeSection(20, 70)

    def ui_calc(self):
        self.pb_awg.setEnabled(True)
        # Составим sql запрос
        sql_quere = """SELECT cut.Id, pack.Id
                  FROM cut LEFT JOIN pack ON cut.Id = pack.Cut_Id
                    LEFT JOIN product_article_parametrs ON pack.Article_Parametr_Id = product_article_parametrs.Id
                    LEFT JOIN product_article_size ON product_article_parametrs.Product_Article_Size_Id = product_article_size.Id
                    LEFT JOIN product_article ON product_article_size.Article_Id = product_article.Id"""

        where = self.build_sql_where()

        if where:
            sql_quere += " WHERE %s" % where

        sql_quere += " ORDER BY cut.Date_Cut"

        query = sql_quere
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения номеров кроя", sql_info.msg, QMessageBox.Ok)
            return False

        # разобьем полученый список на два Крой и пачки
        sql_cut = set()
        sql_pack = []
        for item in sql_info:
            sql_cut.add(item[0])
            sql_pack.append(item)

        # обнуляем таблицу
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        # Создаем прогресс полосу
        progress_bar = QProgressDialog("Построение отчета всего %s пачек" % len(sql_pack), "Отмена", 0, len(sql_pack))
        progress_bar.setMinimumDuration(0)

        # Создаем список для кроев и счетчик кроев
        cut_list = []
        i = 0

        # получаем классы кроев из списка id плученных из sql
        for cut_id in sql_cut:
            cut_list.append(cut.Cut(cut_id))

        # Начинаем перебор кроев, в которых будем перебирать их пачки
        for cut_class in cut_list:
            # Вставляем значение в прогресс полосу
            progress_bar.setValue(i)
            QCoreApplication.processEvents()

            # Если нажали отмену то останавливаем построение
            if progress_bar.wasCanceled():
                break

            # перебираем id пачек из этого кроя
            for pack_id in sql_pack:
                # Проверяем относиться ли id пачки к данному крою, если нет смотрим следующий id
                if pack_id[0] != cut_class.id():
                    continue

                # Добавляем счетчик
                i += 1

                pack_class = cut.Pack(pack_id[1])
                # Получим фурнитуру и операции в пачке
                pack_class.take_accessories_pack()
                pack_class.take_operation_pack()
                pack_class.take_add_material()

                # Расчет показателей
                material_price = pack_class.material_price()
                value = pack_class.value()
                weight_piece = pack_class.weight_piece()
                price_material_in_piece = round(material_price * weight_piece, 4)
                accessories_price_piece = self.calc_accessories_piece(pack_class.accessories())
                operation_price_piece = self.calc_operation_piece(pack_class.operations())
                percent_damage = pack_class.percent_damage()
                rest_percent = cut_class.rest_percent()
                material_add_rest_in_piece = round(weight_piece + (weight_piece / 100 * rest_percent), 4)
                price_material_add_rest_in_piece = round(material_add_rest_in_piece * material_price, 4)
                add_material_weight, add_material_price_sum = self.calc_add_material_piece_wight_price(pack_class.add_materials())
                all_material_price_in_piece = round(price_material_add_rest_in_piece + Decimal(add_material_price_sum / value), 4)
                all_material_weight_in_piece = round(material_add_rest_in_piece + Decimal(add_material_weight / value), 4)

                sebest = Decimal(operation_price_piece + accessories_price_piece + all_material_price_in_piece)
                sebest_add_percent = round(sebest + (sebest / 100 * Decimal(self.le_add_percent.text())), 4)

                self.table_widget.insertRow(self.table_widget.rowCount())

                # Встааляем дату кроя
                item = QTableWidgetItem(str(cut_class.date().strftime("%d.%m.%Y")))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 0, item)

                # Встааляем артикул
                item = QTableWidgetItem(str(pack_class.article()))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 1, item)

                # Встааляем размер
                item = QTableWidgetItem(str(pack_class.size()))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 2, item)

                # Встааляем параметр
                item = QTableWidgetItem(str(pack_class.parametr_name()))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 3, item)

                # Встааляем колво в пачке
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 4, item)

                # Встааляем номер кроя
                item = QTableWidgetItem(str(pack_class.number_cut()))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 5, item)

                # Встааляем номер пачки
                item = QTableWidgetItem(str(pack_class.number_pack()))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 6, item)

                # Встааляем имя раскройщика
                item = QTableWidgetItem(str(cut_class.worker_name()))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 7, item)

                # Вставляем себестоймость
                item = QTableWidgetItem(str(sebest))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 8, item)

                # Встааляем цену ткани
                item = QTableWidgetItem(str(material_price))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 9, item)

                # Встааляем цена ткани на еденицу
                item = QTableWidgetItem(str(price_material_in_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 10, item)

                # Встааляем цена ткани на еденицу + обрезь
                item = QTableWidgetItem(str(price_material_add_rest_in_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 11, item)

                # Встааляем цена ткани на еденицу + обрезь + доп ткань
                item = QTableWidgetItem(str(all_material_price_in_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 12, item)

                # Встааляем процент обрези
                item = QTableWidgetItem(str(rest_percent))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 13, item)

                # Встааляем цену операций на еденицу
                item = QTableWidgetItem(str(operation_price_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 14, item)

                # Встааляем цену фурнитуры на еденицу
                item = QTableWidgetItem(str(accessories_price_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 15, item)

                # Встааляем процент брака
                item = QTableWidgetItem(str(percent_damage))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 16, item)

                # Встааляем себестоймость + %
                item = QTableWidgetItem(str(sebest_add_percent))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 17, item)

                # Вставляем сколько ткани в штуке
                item = QTableWidgetItem(str(weight_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 18, item)

                # Вставляем сколько ткани в штуке + обрези
                item = QTableWidgetItem(str(material_add_rest_in_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 19, item)

                # Вставляем сколько ткани в штуке + обрези + доп ткани
                item = QTableWidgetItem(str(all_material_weight_in_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 20, item)

    def ui_calc_awg(self):

        self.pb_awg.setEnabled(False)

        self.table_widget.insertRow(0)
        self.table_widget.insertRow(0)

        self.table_widget.setSpan(0, 0, 1, 20)
        item = QTableWidgetItem("СРЕДНИЕ ЗНАЧЕНИЯ")
        item.setTextAlignment(Qt.AlignHCenter)
        self.table_widget.setItem(0, 0, item)

        for col in range(8, self.table_widget.columnCount()):
            list = []
            for row in range(2, self.table_widget.rowCount()):
                list.append(float(self.table_widget.item(row, col).text()))
            else:
                item = QTableWidgetItem(str(round(sum(list) / len(list), 4)))
                self.table_widget.setItem(1, col, item)



    def ui_view_art(self):
        self.but_name = QObject.sender(self).objectName()

        self.article_list = article.ArticleList(self, True)
        self.article_list.setWindowModality(Qt.ApplicationModal)
        self.article_list.show()

    def calc_accessories_piece(self, accessories):
        sum = 0
        for item in accessories:
            sum += item["value_thing"] * item["price"]

        return round(sum, 4)

    def calc_operation_piece(self, operations):
        sum = 0
        for item in operations:
            sum += item["price"]

        return round(sum, 4)

    def calc_add_material_piece_wight_price(self, add_material):
        sum_price = 0
        sum_weight = 0
        for item in add_material:
            sum_weight += item["weight"] + item["weight_rest"]
            sum_price += (item["weight"] + item["weight_rest"]) * item["price"]

        return (round(sum_weight, 4), round(sum_price, 4))

    def build_sql_where(self):
        where = ""

        # Проверяем по какому пункту будем сортировать
        if self.le_param.text():
            where += " product_article_parametrs.Id = %s" % self.le_param.whatsThis()
        elif self.le_size.text():
            where += " product_article_size.Id = %s" % self.le_size.whatsThis()
        elif self.le_art.text():
            where += " product_article.Id = %s" % self.le_art.whatsThis()

        if self.gb_date.isChecked():
            sql_date = "(cut.Date_Cut >= '%s' AND cut.Date_Cut <= '%s')" % (self.de_date_in.date().toString(Qt.ISODate), self.de_date_from.date().toString(Qt.ISODate))

            # Если что то есть в Where тогда приверку на дату доьбавляем через AND
            if where:
                where += " AND %s" % sql_date
            else:
                where += sql_date

        return where

    def of_tree_select_article(self, article):
        if self.but_name == "pb_parametr":
            self.le_art.setWhatsThis(str(article["article_id"]))
            self.le_art.setText(str(article["article"]))
            self.le_size.setWhatsThis(str(article["size_id"]))
            self.le_size.setText(str(article["size"]))
            self.le_param.setWhatsThis(str(article["parametr_id"]))
            self.le_param.setText(str(article["parametr"]))

        elif self.but_name == "pb_size":
            self.le_art.setWhatsThis(str(article["article_id"]))
            self.le_art.setText(str(article["article"]))
            self.le_size.setWhatsThis(str(article["size_id"]))
            self.le_size.setText(str(article["size"]))

        else:
            self.le_art.setWhatsThis(str(article["article_id"]))
            self.le_art.setText(str(article["article"]))

        self.article_list.close()
        self.article_list.destroy()

