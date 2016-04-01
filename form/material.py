from os import getcwd
from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.uic import loadUiType
from function import my_sql

material_class, material_base_class = loadUiType(getcwd() + '/ui/material.ui')


class Material(QMainWindow, material_class):
    def __init__(self, *args):
        super(Material, self).__init__()
        self.setupUi(self)

