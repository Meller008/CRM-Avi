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

sibest_class = loadUiType(getcwd() + '/ui/report_sibestoimost.ui')[0]


class ReportSibestoimost(QMainWindow, sibest_class):
    def __init__(self):
        super(ReportSibestoimost, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_settings()

    def start_settings(self):
        self.de_date_in.setDate(QDate.currentDate().addMonths(-3))
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

    def ui_calc(self):
        query = "SELECT cut.Id FROM cut"
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения номеров кроя", sql_info.msg, QMessageBox.Ok)
            return False

        # обнуляем таблицу
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        # Создаем прогресс полосу
        progress_bar = QProgressDialog("Построение отчета всего %s кроев" % len(sql_info), "Отмена", 0, len(sql_info))
        progress_bar.setMinimumDuration(0)

        # Создаем список для кроев и счетчик кроев
        cut_list = []
        i = 0

        # получаем классы кроев из списка id плученных из sql
        for cut_id in sql_info:
            cut_list.append(cut.Cut(cut_id[0]))

        # Начинаем перебор кроев, в которых будем перебирать их пачки
        for cut_class in cut_list:
            cut_class.take_pack_sql()
            pack_list_class = cut_class.pack_list()

            # Добавляем счетчик и вставляем значение в прогресс полосу
            i += 1
            progress_bar.setValue(i)
            QCoreApplication.processEvents()

            # Если нажали отмену то останавливаем построение
            if progress_bar.wasCanceled():
                break

            # перебираем пачки кроя
            for pack_class in pack_list_class.values():

                # Получим фурнитуру и операции в пачке
                pack_class.take_accessories_pack()
                pack_class.take_operation_pack()

                # Расчет показателей
                material_price = pack_class.material_price()
                value = pack_class.value()
                weight_piece = pack_class.weight_piece()
                price_material_in_piece = round(material_price * weight_piece, 4)
                accessories_price_piece = self.calc_accessories_piece(pack_class.accessories())
                operation_price_piece = self.calc_operation_piece(pack_class.operations())
                percent_damage = pack_class.percent_damage()
                material_add_rest_in_piece = round(weight_piece + (cut_class.rest_in_pack() / value), 4)

                sebest = operation_price_piece + accessories_price_piece + weight_piece
                sebest_add_percent = round(float(sebest + (sebest / 100)) * float(self.le_add_percent.text()), 4)

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

                # Встааляем процент обрези
                item = QTableWidgetItem(str(cut_class.rest_percent()))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 11, item)

                # Встааляем цену операций на еденицу
                item = QTableWidgetItem(str(operation_price_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 12, item)

                # Встааляем цену фурнитуры на еденицу
                item = QTableWidgetItem(str(accessories_price_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 13, item)

                # Встааляем процент брака
                item = QTableWidgetItem(str(percent_damage))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 14, item)

                # Встааляем себестоймость + %
                item = QTableWidgetItem(str(sebest_add_percent))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 15, item)

                # Вставляем сколько ткани в штуке
                item = QTableWidgetItem(str(weight_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 16, item)

                # Вставляем сколько ткани в штуке + обрези
                item = QTableWidgetItem(str(material_add_rest_in_piece))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, 17, item)

    def ui_view_art(self):
        but_name = QObject.sender(self).objectName()

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

    def build_sql_where(self):
        pass

    def of_tree_select_article(self, article):
        self.article_list.close()
        self.article_list.destroy()

