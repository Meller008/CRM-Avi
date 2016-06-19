from os import getcwd, path, mkdir, listdir, startfile
from shutil import copy
from form import accessories_provider, staff
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QVariant
from function import my_sql

client_class = loadUiType(getcwd() + '/ui/client.ui')[0]
client_adress_class = loadUiType(getcwd() + '/ui/client_adres.ui')[0]


class ClientsList(accessories_provider.AccessoriesProvider):  # Вывод всех клиентов
    def set_settings(self):
        self.setWindowTitle("Клиенты")
        self.toolBar.setStyleSheet("background-color: rgb(85, 170, 0);")

    def set_sql_query(self):
        self.sql_list = "SELECT clients.Id, clients.Name FROM clients"
        self.sql_dell = "DELETE FROM clients WHERE Id = %s"

    def list_provider(self):
        sql_result = my_sql.sql_select(self.sql_list)
        self.lw_provider.clear()
        if "mysql.connector.errors" in str(type(sql_result)):
            QMessageBox.critical(self, "Ошибка sql", sql_result.msg)
        else:
            for prov in sql_result:
                var = QVariant(prov[0])
                item = QListWidgetItem(prov[1])
                item.setData(-1, var)
                self.lw_provider.addItem(item)

    def add_provider(self):
        self.add_client = Client(self)
        self.add_client.show()

    def change_provider(self):
        try:
            select = self.lw_provider.selectedItems()[0].data(-1)
            self.change_client = Client(self, select)
            self.change_client.show()
        except:
            pass

    def double_click_provider(self, select_prov):
        if not self.dc_select:
            self.change_client = Client(self, select_prov.data(-1))
            self.change_client.show()
        else:
            pass

    def dell_provider(self):
        try:
            select = self.lw_provider.selectedItems()[0].data(-1)
            par = (select, )
            sql_ret = my_sql.sql_change(self.sql_dell, par)
            if "mysql.connector.errors" in str(type(sql_ret)):
                QMessageBox.critical(self, "Ошибка sql кдаление клиента", sql_ret.msg)
            self.list_provider()
        except BaseException as e:
            print(e)


class Client(QDialog, client_class):
    def __init__(self, m, select_id="new"):
        super(Client, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.m = m
        self.select_id = select_id
        self.set_info()
        self.delete_adress = []  # Для запоминания удаленых адрес

    def inspection_path(self, dir_name, sql_dir_name):  # Находим путь работника
        if not hasattr(self, 'path_work'):
            query = 'SELECT `Values` FROM program_settings_path WHERE Name = "%s"' % sql_dir_name
            info_sql = my_sql.sql_select(query)
            if "mysql.connector.errors" in str(type(info_sql)):
                        QMessageBox.critical(self, "Ошибка sql", info_sql.msg, QMessageBox.Ok)
                        return False
            self.path_wor = info_sql[0][0]
            if not path.isdir("%s/%s" % (self.path_wor, dir_name)):
                try:
                    mkdir("%s/%s" % (self.path_wor, dir_name))
                    return "%s/%s" % (self.path_wor, dir_name)
                except:
                    QMessageBox.critical(self, "Ошибка файлы", "Нет доступа к корневому диалогу, файлы недоступны", QMessageBox.Ok)
                    return False
            else:
                return "%s/%s" % (self.path_wor, dir_name)

    def inspection_files(self, dir_name, sql_dir_name):   # Проверяем файлы и даем иконки
        self.path = self.inspection_path(dir_name, sql_dir_name)
        if self.path:
            self.lw_file.clear()
            files = listdir("%s/%s" % (self.path_wor, dir_name))
            for file in files:
                if "~" not in file:
                    r = path.splitext(file)  # Получаем название и расширение
                    if "xlsx" in r[1][1:] or "xlsm" in r[1] or "xls" in r[1] or "xlt" in r[1]:
                        ico = "xlsx"
                    elif "xml" in r[1][1:] or "docx" in r[1] or "doc" in r[1] or "docm" in r[1]:
                        ico = "xml"
                    elif "png" in r[1] or "jpg" in r[1] or "jpeg" in r[1] or "jpe" in r[1] or "gif" in r[1] or "bmp" in r[1]:
                        ico = "image"
                    elif "pdf" in r[1]:
                        ico = "pdf"
                    else:
                        ico = "other"

                    list_item = QListWidgetItem(r[0] + r[1])
                    list_item.setIcon(QIcon(getcwd() + "/images/%s.ico" % ico))
                    self.lw_file.addItem(list_item)

    def select_file(self, file):  # Открываем выбраный фаил
        dir_name = self.le_name.text()
        self.path = self.inspection_path(dir_name, 'Путь корень клиенты')
        if self.path:
            file_name = file.text()
            startfile(r'%s/%s' % (self.path.replace("/", "\\"), file_name.replace("/", "\\")))

    def open_dir(self):  # Открываем выбраную папку
        dir_name = self.le_name.text()
        self.path = self.inspection_path(dir_name, 'Путь корень клиенты')
        if self.path:
            startfile(self.path.replace("/", "\\"))

    def add_file(self):  # Добавляем файлы
        info = staff.AddFile()
        if info.exec() == 0:
            return False
        new_r = path.splitext(info.path_copy_file.text())[1]
        dir_name = self.le_name.text()
        copy(info.path_copy_file.text(), self.inspection_path(dir_name, 'Путь корень клиенты') + "/" + info.le_new_file_name.text() + path.splitext(info.path_copy_file.text())[1])
        self.inspection_files(dir_name, 'Путь корень клиенты')

    def acc(self):
        if self.cb_nds.isChecked():
            no_nds = 1
        else:
            no_nds = 0
        if self.select_id == "new":
            query = """INSERT INTO clients (Name, Legal_Address, Actual_Address, INN, KPP, OGRN, Account, Bank, corres_Account, BIK, Contact_Person, Phone, Mail, Note, No_Nds)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            paremetrs = (self.le_name.text(), self.le_legal_address.text(), self.le_actual_address.text(), self.le_inn.text(), self.le_kpp.text(), self.le_ogrn.text(),
                         self.le_rs.text(), self.le_bank.text(), self.le_ks.text(), self.le_bik.text(), self.le_fio.text(), self.le_phone.text(),
                         self.le_mail.text(), self.le_note.toPlainText(), no_nds)
            new_id = my_sql.sql_change(query, paremetrs)
            if "mysql.connector.errors" in str(type(new_id)):
                    QMessageBox.critical(self, "Ошибка sql добавление клиента", new_id.msg, QMessageBox.Ok)
                    return False
            for row in range(self.tw_adres.rowCount()):
                item = self.tw_adres.item(row, 0)
                if item.data(-2) is not None:
                    if item.data(-2) == "new":
                        query = "INSERT INTO clients_actual_address (Client_Id, Name, Adres, KPP) VALUES (%s, %s, %s, %s)"
                        paremetrs = (new_id, self.tw_adres.item(row, 0).text(), self.tw_adres.item(row, 1).text(), self.tw_adres.item(row, 2).text())
                        info_sql = my_sql.sql_change(query, paremetrs)
                        if "mysql.connector.errors" in str(type(info_sql)):
                            QMessageBox.critical(self, "Ошибка sql добавления адреса", info_sql.msg, QMessageBox.Ok)
        else:
            query = """UPDATE clients SET Name = %s, Legal_Address = %s, Actual_Address = %s, INN = %s, KPP = %s, OGRN = %s, Account = %s, Bank = %s, corres_Account = %s,
                       BIK = %s, Contact_Person = %s, Phone = %s, Mail = %s, Note = %s, No_Nds = %s WHERE Id = %s"""
            paremetrs = (self.le_name.text(), self.le_legal_address.text(), self.le_actual_address.text(), self.le_inn.text(), self.le_kpp.text(), self.le_ogrn.text(),
                         self.le_rs.text(), self.le_bank.text(), self.le_ks.text(), self.le_bik.text(), self.le_fio.text(), self.le_phone.text(),
                         self.le_mail.text(), self.le_note.toPlainText(), no_nds, self.select_id)
            info_sql = my_sql.sql_change(query, paremetrs)
            if "mysql.connector.errors" in str(type(info_sql)):
                    QMessageBox.critical(self, "Ошибка sql изменение клиента", info_sql.msg, QMessageBox.Ok)

            for row in range(self.tw_adres.rowCount()):
                item = self.tw_adres.item(row, 0)
                if item.data(-2) is not None:
                    if item.data(-2) == "new":
                        query = "INSERT INTO clients_actual_address (Client_Id, Name, Adres, KPP) VALUES (%s, %s, %s, %s)"
                        paremetrs = (self.select_id, self.tw_adres.item(row, 0).text(), self.tw_adres.item(row, 1).text(), self.tw_adres.item(row, 2).text())
                        info_sql = my_sql.sql_change(query, paremetrs)
                        if "mysql.connector.errors" in str(type(info_sql)):
                            QMessageBox.critical(self, "Ошибка sql добавления адреса", info_sql.msg, QMessageBox.Ok)
                    elif item.data(-2) == "update":
                        query = "UPDATE clients_actual_address SET Name = %s, Adres = %s, KPP = %s WHERE Id = %s"
                        paremetrs = (self.tw_adres.item(row, 0).text(), self.tw_adres.item(row, 1).text(), self.tw_adres.item(row, 2).text(), item.data(-1))
                        info_sql = my_sql.sql_change(query, paremetrs)
                        if "mysql.connector.errors" in str(type(info_sql)):
                            QMessageBox.critical(self, "Ошибка sql изменение адреса", info_sql.msg, QMessageBox.Ok)

            for del_id in self.delete_adress:
                query = 'DELETE FROM clients_actual_address WHERE Id = %s'
                info_sql = my_sql.sql_change(query, (del_id, ))
                if "mysql.connector.errors" in str(type(info_sql)):
                    QMessageBox.critical(self, "Ошибка sql удаление адреса", info_sql.msg, QMessageBox.Ok)

        self.m.list_provider()
        self.close()
        self.destroy()

    def set_info(self):
        self.tw_adres.horizontalHeader().resizeSection(0, 120)
        self.tw_adres.horizontalHeader().resizeSection(1, 300)
        self.tw_adres.horizontalHeader().resizeSection(2, 80)
        if self.select_id == "new":
            self.pb_add_file.setEnabled(False)
            self.pb_open_file.setEnabled(False)
        else:
            query = """SELECT Name, Legal_Address, Actual_Address, INN, KPP, OGRN, Account, Bank, corres_Account,
                                        BIK, Contact_Person, Phone, Mail, Note, No_Nds FROM clients WHERE Id = %s"""
            info_client = my_sql.sql_select(query, (self.select_id, ))
            if "mysql.connector.errors" in str(type(info_client)):
                    QMessageBox.critical(self, "Ошибка sql вывод клиента", info_client.msg, QMessageBox.Ok)
                    return False

            self.le_name.setText(info_client[0][0])
            self.le_legal_address.setText(info_client[0][1])
            self.le_actual_address.setText(info_client[0][2])
            self.le_inn.setText(info_client[0][3])
            self.le_kpp.setText(info_client[0][4])
            self.le_ogrn.setText(info_client[0][5])
            self.le_rs.setText(info_client[0][6])
            self.le_bank.setText(info_client[0][7])
            self.le_ks.setText(info_client[0][8])
            self.le_bik.setText(info_client[0][9])
            self.le_fio.setText(info_client[0][10])
            self.le_phone.setText(info_client[0][11])
            self.le_mail.setText(info_client[0][12])
            self.le_note.appendPlainText(info_client[0][13])
            if info_client[0][14]:
                self.cb_nds.setChecked(True)

            query = """SELECT Id, Name, Adres, KPP FROM clients_actual_address WHERE Client_Id = %s"""
            info_client = my_sql.sql_select(query, (self.select_id, ))
            if "mysql.connector.errors" in str(type(info_client)):
                    QMessageBox.critical(self, "Ошибка sql вывод клиента", info_client.msg, QMessageBox.Ok)
                    return False

            row = 0
            for item in info_client:
                self.tw_adres.insertRow(self.tw_adres.rowCount())
                table_item = QTableWidgetItem(item[1])
                table_item.setData(-1, item[0])
                self.tw_adres.setItem(row, 0, table_item)
                table_item = QTableWidgetItem(item[2])
                self.tw_adres.setItem(row, 1, table_item)
                table_item = QTableWidgetItem(item[3])
                self.tw_adres.setItem(row, 2, table_item)
                row += 1

            self.inspection_files(self.le_name.text(), "Путь корень клиенты")

    def add_adress(self):
        adress = ClientAdress()
        if adress.exec() == 0:
            return False
        row = self.tw_adres.rowCount()
        self.tw_adres.insertRow(row)
        table_item = QTableWidgetItem(adress.le_name.text())
        table_item.setData(-2, "new")
        self.tw_adres.setItem(row, 0, table_item)
        table_item = QTableWidgetItem(adress.le_adres.text())
        self.tw_adres.setItem(row, 1, table_item)
        table_item = QTableWidgetItem(adress.le_kpp.text())
        self.tw_adres.setItem(row, 2, table_item)

    def double_click_adress(self, select_items):
        row = select_items
        select_adres = (self.tw_adres.item(row, 0).data(-1), self.tw_adres.item(row, 0).text(), self.tw_adres.item(row, 1).text(), self.tw_adres.item(row, 2).text())
        adress = ClientAdress()
        adress.le_name.setText(select_adres[1])
        adress.le_adres.setText(select_adres[2])
        adress.le_kpp.setText(select_adres[3])
        if adress.exec() == 0:
            return False
        table_item = QTableWidgetItem(adress.le_name.text())
        table_item.setData(-1, select_adres[0])
        table_item.setData(-2, "update")
        self.tw_adres.setItem(row, 0, table_item)
        table_item = QTableWidgetItem(adress.le_adres.text())
        self.tw_adres.setItem(row, 1, table_item)
        table_item = QTableWidgetItem(adress.le_kpp.text())
        self.tw_adres.setItem(row, 2, table_item)

    def dell_adress(self):
        try:
            row = self.tw_adres.selectedItems()[0].row()
            id = self.tw_adres.selectedItems()[0].data(-1)
            if id is not None:
                self.delete_adress.append(id)
            self.tw_adres.removeRow(row)
        except:
            pass


class ClientAdress(QDialog, client_adress_class):
    def __init__(self):
        super(ClientAdress, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

