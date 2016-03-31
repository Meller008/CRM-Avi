from os import getcwd
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUiType
from function import my_sql

material_provider_class, material_provider_base_class = loadUiType(getcwd() + '/ui/material_provider.ui')
add_material_provider_class, add_material_provider_base_class = loadUiType(getcwd() + '/ui/add_material_provider.ui')
change_material_provider_class, change_material_provider_base_class = loadUiType(
    getcwd() + '/ui/change_material_provider.ui')


class MaterialProvider(QDialog, material_provider_class):
    def __init__(self, *args):
        super(MaterialProvider, self).__init__()
        self.setupUi(self)
        self.list_provider()

    def list_provider(self):
        query = "SELECT material_provider.Name FROM material_provider"
        sql_result = my_sql.sql_select(query)
        self.lw_provider.clear()
        for prov in sql_result:
            self.lw_provider.addItem(prov[0])

    def view_add_provider(self):
        self.add_provider = AddMaterialProvider(self)
        self.add_provider.show()

    def select_provider(self, select_prov):
        self.change_provider = ChangeMaterialProvider(self, select_prov.text())
        self.change_provider.show()

    def exit_provider(self):
        self.close()
        self.destroy()


class AddMaterialProvider(QDialog, add_material_provider_class):
    def __init__(self, *args):
        self.main = args[0]
        super(AddMaterialProvider, self).__init__()
        self.setupUi(self)
        self.setModal(True)

    def add_provider(self):
        query = 'INSERT INTO avi_crm.material_provider (Name, Information) VALUES (%s, %s)'
        name = self.le_name.text()
        info = self.le_info.toPlainText()
        par = (name, info)
        my_sql.sql_change(query, par)
        self.main.list_provider()
        self.close()
        self.destroy()

    def cansel_add(self):
        self.close()
        self.destroy()


class ChangeMaterialProvider(QDialog, change_material_provider_class):
    def __init__(self, *args):
        self.main = args[0]
        self.change_provider = args[1]
        super(ChangeMaterialProvider, self).__init__()
        self.setupUi(self)
        self.setModal(True)

        query = "SELECT material_provider.Name, material_provider.Information FROM material_provider WHERE  Name = %s"
        parametr = (self.change_provider,)
        sql_result = my_sql.sql_select(query, parametr)

        self.le_name.setText(sql_result[0][0])
        self.le_info.appendPlainText(sql_result[0][1])

    def cancel_change(self):
        self.close()
        self.destroy()

    def chan_provider(self):
        name = self.le_name.text()
        if name != self.change_provider:
            query = 'UPDATE material_provider SET material_provider.Name = %s, material_provider.Information = %s ' \
                    'WHERE material_provider.Name = %s'
            info = self.le_info.toPlainText()
            par = (name, info, self.change_provider)
            my_sql.sql_change(query, par)
        self.main.list_provider()
        self.close()
        self.destroy()
