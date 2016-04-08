from os import getcwd
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUiType
from function import my_sql

material_provider_class, material_provider_base_class = loadUiType(getcwd() + '/ui/material_provider.ui')
add_material_provider_class, add_material_provider_base_class = loadUiType(getcwd() + '/ui/add_material_provider.ui')
change_material_provider_class, change_material_provider_base_class = loadUiType(getcwd() + '/ui/change_material_provider.ui')


class MaterialProvider(QMainWindow, material_provider_class):
    def __init__(self, m_class=0):
        super(MaterialProvider, self).__init__()
        self.setupUi(self)
        self.set_settings()
        self.set_sql_query()
        self.list_provider()
        self.m_class = m_class

    def set_settings(self):
        self.setWindowTitle("Поставщики ткани")
        self.toolBar.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.add_title = "Добавить поставщика"
        self.change_title = "Изменить поставщика"


    def set_sql_query(self):
        self.sql_list = "SELECT material_provider.Name FROM material_provider"
        self.sql_add = "INSERT INTO avi_crm.material_provider (Name, Information) VALUES (%s, %s)"
        self.sql_change_select = "SELECT material_provider.Name, material_provider.Information FROM material_provider WHERE  Name = %s"
        self.sql_update_select = 'UPDATE material_provider SET material_provider.Name = %s, material_provider.Information = %s ' \
                                 'WHERE material_provider.Name = %s'
        self.sql_dell = "DELETE FROM material_provider WHERE material_provider.Name = %s"

    def list_provider(self):
        sql_result = my_sql.sql_select(self.sql_list)
        self.lw_provider.clear()
        if "mysql.connector.errors.IntegrityError" in str(type(sql_result)):
            QMessageBox.critical(self, "Ошибка sql", sql_result.msg)
        else:
            for prov in sql_result:
                self.lw_provider.addItem(prov[0])

    def add_provider(self):
        self.add_provider = AddMaterialProvider(self)
        self.add_provider.show()

    def change_provider(self):
        select = self.lw_provider.selectedItems()
        if select:
            self.change_provider = ChangeMaterialProvider(self, select[0].text())
            self.change_provider.show()

    def dell_provider(self):
        select = self.lw_provider.selectedItems()
        if select:
            par = (select[0].text(), )
            sql_ret = my_sql.sql_change(self.sql_dell, par)
            if "mysql.connector.errors.IntegrityError" in str(type(sql_ret)):
                QMessageBox.critical(self, "Ошибка sql", sql_ret.msg)
            self.list_provider()

    def double_click_provider(self, select_prov):
        self.change_provider = ChangeMaterialProvider(self, select_prov.text())
        self.change_provider.show()


class AddMaterialProvider(QDialog, add_material_provider_class):
    def __init__(self, *args):
        self.main = args[0]
        super(AddMaterialProvider, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(self.main.add_title)
        self.setModal(True)

    def add_provider(self):
        name = self.le_name.text()
        info = self.le_info.toPlainText()
        par = (name, info)
        sql_ret = my_sql.sql_change(self.main.sql_add, par)
        if "mysql.connector.errors.IntegrityError" in str(type(sql_ret)):
            QMessageBox.critical(self, "Ошибка sql", sql_ret.msg)
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
        self.setWindowTitle(self.main.change_title)
        self.setModal(True)

        par = (self.change_provider,)
        sql_ret = my_sql.sql_select(self.main.sql_change_select, par)
        if "mysql.connector.errors.IntegrityError" in str(type(sql_ret)):
            QMessageBox.critical(self, "Ошибка sql", sql_ret.msg)
        else:
            self.le_name.setText(sql_ret[0][0])
            self.le_info.appendPlainText(sql_ret[0][1])

    def cancel_change(self):
        self.close()
        self.destroy()

    def chan_provider(self):
        name = self.le_name.text()
        info = self.le_info.toPlainText()
        par = (name, info, self.change_provider)
        sql_ret = my_sql.sql_change(self.main.sql_update_select, par)
        if "mysql.connector.errors.IntegrityError" in str(type(sql_ret)):
            QMessageBox.critical(self, "Ошибка sql", sql_ret.msg)
        self.main.list_provider()
        self.close()
        self.destroy()
