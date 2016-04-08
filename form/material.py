from os import getcwd
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QBrush, QColor
from PyQt5 import QtCore
from function import my_sql
from form import material_provider, comparing

material_class, material_base_class = loadUiType(getcwd() + '/ui/material.ui')
add_material_class, add_material_base_class = loadUiType(getcwd() + '/ui/add_material.ui')
add_material_pozition_class, add_material_pozition_base_class = loadUiType(getcwd() + '/ui/add_material_pozition.ui')


class AddComparingName(comparing.ComparingName):
    def double_click_provider(self, select_prov):
        self.m_class.le_name.setText(select_prov.text())
        self.close()
        self.destroy()


class MaterialName(material_provider.MaterialProvider):
    def set_sql_query(self):
        self.sql_list = "SELECT material_name.Name FROM material_name"
        self.sql_add = "INSERT INTO material_name (Name, Information) VALUES (%s, %s)"
        self.sql_change_select = "SELECT material_name.Name, material_name.Information FROM material_name WHERE  Name = %s"
        self.sql_update_select = 'UPDATE material_name SET material_name.Name = %s, material_name.Information = %s ' \
                                 'WHERE material_name.Name = %s'
        self.sql_dell = "DELETE FROM material_name WHERE material_name.Name = %s"

    def set_settings(self):
        self.setWindowTitle("Названия тканей")
        self.toolBar.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.add_title = "Добавить ткань"
        self.change_title = "Изменить ткань"

    def double_click_provider(self, select_prov):
        self.m_class.set_material_name(select_prov.text())
        self.close()
        self.destroy()


class MaterialProviderName(material_provider.MaterialProvider):
    def double_click_provider(self, select_prov):
        self.m_class.le_provider.setText(select_prov.text())
        self.close()
        self.destroy()


class Material(QMainWindow, material_class):
    def __init__(self, *args):
        super(Material, self).__init__()
        self.setupUi(self)

    def add_material(self):
        self.add_mat = AddMaterial()
        self.add_mat.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_mat.show()


class AddMaterial(QMainWindow, add_material_class):
    def __init__(self, *args):
        super(AddMaterial, self).__init__()
        self.setupUi(self)
        self.de_data.setDate(QtCore.QDate.currentDate())

    def add_comparing_pozition(self):
        self.add_comp_poz = AddComparingPosition(self)
        self.add_comp_poz.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_comp_poz.show()

    def view_name_provider(self):
        self.view_provider = MaterialProviderName(self)
        self.view_provider.setWindowModality(QtCore.Qt.ApplicationModal)
        self.view_provider.show()

    def add_materia_pozition(self):
        self.add_mat_poz = AddMaterialPosition(self)
        self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_mat_poz.show()

    def add_pozition(self, mat_poz, collor):
        self.j = 0
        self.tw_position.setRowCount(self.tw_position.rowCount()+1)
        for i in mat_poz:
            item = QTableWidgetItem(i)
            brush = QBrush(QColor(collor[0], collor[1], collor[2], 255))
            item.setBackground(brush)
            self.tw_position.setItem(self.tw_position.rowCount()-1, self.j, item)
            self.j += 1
        self.tw_position.horizontalHeader().resizeSection(0, 270)
        self.tw_position.horizontalHeader().resizeSection(1, 75)
        self.tw_position.horizontalHeader().resizeSection(2, 55)
        self.tw_position.horizontalHeader().resizeSection(3, 95)

    def double_click(self, i):
        collor =  self.tw_position.item(i, 0).background().color().red()
        name = self.tw_position.item(i, 0).text()
        value = self.tw_position.item(i, 1).text()
        price = self.tw_position.item(i, 2).text()
        summ = self.tw_position.item(i, 3).text()

        self.add_mat_poz = AddMaterialPosition(self)
        self.add_mat_poz.set_meaning((name, value, price, summ))
        self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_mat_poz.show()

    def add_material(self):
        pass


class AddMaterialPosition(QDialog, add_material_pozition_class):
    def __init__(self, *args):
        super(AddMaterialPosition, self).__init__()
        self.setupUi(self)
        self.main = args[0]
        self.set_settings()

    def set_settings(self):
        pass

    def set_meaning(self, meaning):
        self.le_name.setText(meaning[0])
        self.le_price.setText(meaning[1])
        self.le_value.setText(meaning[2])
        # self.le_name.setText(meaning[3])


    def view_material_name(self):
        self.mat_name = MaterialName(self)
        self.mat_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.mat_name.show()

    def set_material_name(self, change_material):
        self.le_name.setText(change_material)

    def change_price(self):
        if self.le_price.text():
            try:
                self.price = float(self.le_price.text().replace(",", "."))

            except ValueError as error:
                self.price = 0
                QMessageBox.information(self, "Ошибка ввода", "Не верно введена цена, скорее всего вы ввели символ. "
                                                              "\n Ошибка: %s" % error)
        else:
            self.price = 0

        if self.le_value.text():
            try:
                self.value = float(self.le_value.text().replace(",", "."))

            except ValueError as error:
                self.value = 0
                QMessageBox.information(self, "Ошибка ввода", "Не верно введено количество, скорее всего вы ввели символ."
                                                              "\n Ошибка: %s" % error)
        else:
                self.value = 0

        if self.price != 0 and self.value != 0:
            self.lb_summ.setText("Сумма=%s" % str(round(self.price * self.value, 4)))
        else:
            self.lb_summ.setText("Сумма=")

    def add_material_line(self):
        par = (self.le_name.text(), self.le_price.text(), self.le_value.text(), self.lb_summ.text().replace("Сумма=", ""))
        collor = (153, 221, 255)
        self.close()
        self.destroy()
        self.main.add_pozition(par, collor)


class AddComparingPosition(AddMaterialPosition):
    def set_settings(self):
        self.lb_name.setText("Название")
        self.widget.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.lb_value.setText("Кол-во")

    def view_material_name(self):
        self.mat_name = AddComparingName(self)
        self.mat_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.mat_name.show()

    def add_material_line(self):
        par = (self.le_name.text(), self.le_price.text(), self.le_value.text(), self.lb_summ.text().replace("Сумма=", ""))
        collor = (221, 255, 204)
        self.close()
        self.destroy()
        self.main.add_pozition(par, collor)

