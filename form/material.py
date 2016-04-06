from os import getcwd
from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.uic import loadUiType
from PyQt5 import QtCore
from function import my_sql
from form import material_provider

material_class, material_base_class = loadUiType(getcwd() + '/ui/material.ui')
add_material_class, add_material_base_class = loadUiType(getcwd() + '/ui/add_material.ui')
add_material_pozition_class, add_material_pozition_base_class = loadUiType(getcwd() + '/ui/add_material_pozition.ui')

class Material(QMainWindow, material_class):
    def __init__(self, *args):
        super(Material, self).__init__()
        self.setupUi(self)

    def add_material(self):
        self.add_mat = AddMaterial()
        self.add_mat.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_mat.show()


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


class AddMaterial(QMainWindow, add_material_class):
    def __init__(self, *args):
        super(AddMaterial, self).__init__()
        self.setupUi(self)

    def add_materia_pozition(self):
        self.add_mat_poz = AddMaterialPozition()
        self.add_mat_poz.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_mat_poz.show()


class AddMaterialPozition(QDialog, add_material_pozition_class):
    def __init__(self, *args):
        super(AddMaterialPozition, self).__init__()
        self.setupUi(self)

    def view_material_name(self):
        self.mat_name = MaterialName()
        self.mat_name.setWindowModality(QtCore.Qt.ApplicationModal)
        self.mat_name.show()


