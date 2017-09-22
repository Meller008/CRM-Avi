from os import getcwd, path, mkdir, listdir
from datetime import datetime
from shutil import copy
from form import staff
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
from function import my_sql
from form.templates import list
import subprocess


client_class = loadUiType(getcwd() + '/ui/client.ui')[0]
client_adress_class = loadUiType(getcwd() + '/ui/client_adres.ui')[0]
client_number_class = loadUiType(getcwd() + '/ui/client_number.ui')[0]


class ClientList(list.ListItems):
    def set_settings(self):
        self.setWindowTitle("Клиенты")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(85, 170, 0);")  # Цвет бара
        self.title_new_window = "Клиент"  # Имя вызываемых окон

        self.sql_list = "SELECT clients.Id, clients.Name FROM clients ORDER BY clients.Name"
        self.sql_add = ""
        self.sql_change_select = ""
        self.sql_update_select = ''
        self.sql_dell = "DELETE FROM clients WHERE Id = %s"

        self.set_new_win = {"WinTitle": "Клиент",
                            "WinColor": "(85, 170, 0)",
                            "lb_name": "Название",
                            "lb_note": "Заметка"}

    def ui_add_item(self):
        self.add_client = Client(self)
        self.add_client.show()

    def ui_change_item(self, id=False):
        if id:
            id_select = id
        else:
            try:
                id_select = self.lw_list.selectedItems()[0].data(3)
            except:
                QMessageBox.critical(self, "Ошибка", "Выберете элемент", QMessageBox.Ok)
                return False

        self.change_client = Client(self, id_select)
        self.change_client.show()

    def ui_double_click_item(self, select_prov):
        if not self.dc_select:
            self.ui_change_item(select_prov.data(3))
        else:
            item = (select_prov.data(3), select_prov.text())
            self.m_class.of_list_clients(item)
            self.close()
            self.destroy()


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
        self.delete_numbers = []  # Для запоминания удаленых номеров

    def inspection_path(self, dir_name, sql_dir_name):  # Находим путь работника
        if not hasattr(self, 'path_work'):
            query = 'SELECT `Values` FROM program_settings_path WHERE Name = "%s"' % sql_dir_name
            info_sql = my_sql.sql_select(query)
            if "mysql.connector.errors" in str(type(info_sql)):
                        QMessageBox.critical(self, "Ошибка sql", info_sql.msg, QMessageBox.Ok)
                        return False
            self.path_wor = info_sql[0][0]
            if not path.isdir("%s/%s" % (self.path_wor, dir_name.replace('"', "'"))):
                try:
                    mkdir("%s/%s" % (self.path_wor, dir_name.replace('"', "'")))
                    return "%s/%s" % (self.path_wor, dir_name.replace('"', "'"))
                except:
                    QMessageBox.critical(self, "Ошибка файлы", "Нет доступа к корневому диалогу, файлы недоступны", QMessageBox.Ok)
                    return False
            else:
                return "%s/%s" % (self.path_wor, dir_name.replace('"', "'"))

    def inspection_files(self, dir_name, sql_dir_name):   # Проверяем файлы и даем иконки
        self.path = self.inspection_path(dir_name.replace('"', "'"), sql_dir_name)
        if self.path:
            self.lw_file.clear()
            files = listdir("%s/%s" % (self.path_wor, dir_name.replace('"', "'")))
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
            subprocess.call([r'%s/%s' % (self.path.replace("/", "\\"), file_name.replace("/", "\\"))], shell=True)

    def open_dir(self):  # Открываем выбраную папку
        dir_name = self.le_name.text()
        self.path = self.inspection_path(dir_name, 'Путь корень клиенты')
        if self.path:
            subprocess.call([self.path.replace("/", "\\")], shell=True)

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
            query = """INSERT INTO clients (Name, Legal_Address, Actual_Address, INN, KPP, OGRN, Account, Bank, corres_Account, BIK, Contact_Person, Phone,
                                              Mail, Note, No_Nds, Full_Name)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            paremetrs = (self.le_name.text(), self.le_legal_address.text(), self.le_actual_address.text(), self.le_inn.text(), self.le_kpp.text(), self.le_ogrn.text(),
                         self.le_rs.text(), self.le_bank.text(), self.le_ks.text(), self.le_bik.text(), self.le_fio.text(), self.le_phone.text(),
                         self.le_mail.text(), self.le_note.toPlainText(), no_nds, self.le_full_name.text())
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
                       BIK = %s, Contact_Person = %s, Phone = %s, Mail = %s, Note = %s, No_Nds = %s, Full_Name = %s WHERE Id = %s"""
            paremetrs = (self.le_name.text(), self.le_legal_address.text(), self.le_actual_address.text(), self.le_inn.text(), self.le_kpp.text(), self.le_ogrn.text(),
                         self.le_rs.text(), self.le_bank.text(), self.le_ks.text(), self.le_bik.text(), self.le_fio.text(), self.le_phone.text(),
                         self.le_mail.text(), self.le_note.toPlainText(), no_nds, self.le_full_name.text(), self.select_id)
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

            for row in range(self.tw_vendor_number.rowCount()):
                item = self.tw_vendor_number.item(row, 0)
                if item.data(-2) is not None:
                    if item.data(-2) == "new":
                        query = "INSERT INTO clients_vendor_number (Client_Id, Number, Contract, Data_From) VALUES (%s, %s, %s, %s)"
                        data = datetime.strptime(self.tw_vendor_number.item(row, 2).text(), "%d.%m.%Y")
                        paremetrs = (self.select_id, self.tw_vendor_number.item(row, 0).text(), self.tw_vendor_number.item(row, 1).text(), data)
                        info_sql = my_sql.sql_change(query, paremetrs)
                        if "mysql.connector.errors" in str(type(info_sql)):
                            QMessageBox.critical(self, "Ошибка sql добавления номера", info_sql.msg, QMessageBox.Ok)
                    elif item.data(-2) == "update":
                        query = "UPDATE clients_vendor_number SET Number = %s, Contract = %s, Data_From = %s WHERE Id = %s"
                        data = datetime.strptime(self.tw_vendor_number.item(row, 2).text(), "%d.%m.%Y")
                        paremetrs = (self.tw_vendor_number.item(row, 0).text(), self.tw_vendor_number.item(row, 1).text(), data, item.data(-1))
                        info_sql = my_sql.sql_change(query, paremetrs)
                        if "mysql.connector.errors" in str(type(info_sql)):
                            QMessageBox.critical(self, "Ошибка sql изменение номера", info_sql.msg, QMessageBox.Ok)

            for del_id in self.delete_numbers:
                query = 'DELETE FROM clients_vendor_number WHERE Id = %s'
                info_sql = my_sql.sql_change(query, (del_id, ))
                if "mysql.connector.errors" in str(type(info_sql)):
                    QMessageBox.critical(self, "Ошибка sql удаление номера", info_sql.msg, QMessageBox.Ok)

        self.m.sql_set_list()
        self.close()
        self.destroy()

    def can(self):
        self.close()
        self.destroy()

    def set_info(self):
        self.tw_adres.horizontalHeader().resizeSection(0, 120)
        self.tw_adres.horizontalHeader().resizeSection(1, 300)
        self.tw_adres.horizontalHeader().resizeSection(2, 80)

        self.tw_vendor_number.horizontalHeader().resizeSection(0, 120)
        self.tw_vendor_number.horizontalHeader().resizeSection(1, 120)
        self.tw_vendor_number.horizontalHeader().resizeSection(2, 120)

        if self.select_id == "new":
            self.pb_add_file.setEnabled(False)
            self.pb_open_file.setEnabled(False)
        else:
            query = """SELECT Name, Legal_Address, Actual_Address, INN, KPP, OGRN, Account, Bank, corres_Account,
                                        BIK, Contact_Person, Phone, Mail, Note, No_Nds, Full_Name FROM clients WHERE Id = %s"""
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

            self.le_full_name.setText(info_client[0][15])

            query = """SELECT Id, Name, Adres, KPP FROM clients_actual_address WHERE Client_Id = %s"""
            info_client = my_sql.sql_select(query, (self.select_id, ))
            if "mysql.connector.errors" in str(type(info_client)):
                    QMessageBox.critical(self, "Ошибка sql вывод адресов клиента", info_client.msg, QMessageBox.Ok)
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

            query = """SELECT Id, Number, Contract, Data_From FROM clients_vendor_number WHERE Client_Id = %s"""
            info_client = my_sql.sql_select(query, (self.select_id, ))
            if "mysql.connector.errors" in str(type(info_client)):
                    QMessageBox.critical(self, "Ошибка sql вывод адресов клиента", info_client.msg, QMessageBox.Ok)
                    return False

            row = 0
            for item in info_client:
                self.tw_vendor_number.insertRow(self.tw_vendor_number.rowCount())
                table_item = QTableWidgetItem(item[1])
                table_item.setData(-1, item[0])
                self.tw_vendor_number.setItem(row, 0, table_item)
                table_item = QTableWidgetItem(item[2])
                self.tw_vendor_number.setItem(row, 1, table_item)
                table_item = QTableWidgetItem(item[3].strftime("%d.%m.%Y"))
                self.tw_vendor_number.setItem(row, 2, table_item)
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
        sql_status = "update" if (self.tw_adres.item(row, 0).data(-2) != "new") else "new"
        table_item = QTableWidgetItem(adress.le_name.text())
        table_item.setData(-1, select_adres[0])
        table_item.setData(-2, sql_status)
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

    def add_number(self):
        number = ClientNumber()
        number.de_date_from.setDate(QDate.currentDate())
        if number.exec() == 0:
            return False
        row = self.tw_vendor_number.rowCount()
        self.tw_vendor_number.insertRow(row)
        table_item = QTableWidgetItem(number.le_vendor.text())
        table_item.setData(-2, "new")
        self.tw_vendor_number.setItem(row, 0, table_item)
        table_item = QTableWidgetItem(number.le_contract.text())
        self.tw_vendor_number.setItem(row, 1, table_item)
        table_item = QTableWidgetItem(number.de_date_from.date().toString("dd.MM.yyyy"))
        self.tw_vendor_number.setItem(row, 2, table_item)

    def double_click_number(self, select_items):
        row = select_items
        select_adres = (self.tw_vendor_number.item(row, 0).data(-1), self.tw_vendor_number.item(row, 0).text(), self.tw_vendor_number.item(row, 1).text(),
                        self.tw_vendor_number.item(row, 2).text())
        number = ClientNumber()
        number.le_vendor.setText(select_adres[1])
        number.le_contract.setText(select_adres[2])
        data = datetime.strptime(select_adres[3], "%d.%m.%Y")
        number.de_date_from.setDate(data)
        if number.exec() == 0:
            return False
        sql_status = "update" if (self.tw_vendor_number.item(row, 0).data(-2) != "new") else "new"
        table_item = QTableWidgetItem(number.le_vendor.text())
        table_item.setData(-1, select_adres[0])
        table_item.setData(-2, sql_status)
        self.tw_vendor_number.setItem(row, 0, table_item)
        table_item = QTableWidgetItem(number.le_contract.text())
        self.tw_vendor_number.setItem(row, 1, table_item)
        table_item = QTableWidgetItem(number.de_date_from.date().toString("dd.MM.yyyy"))
        self.tw_vendor_number.setItem(row, 2, table_item)

    def dell_number(self):
        try:
            row = self.tw_vendor_number.selectedItems()[0].row()
            id = self.tw_vendor_number.selectedItems()[0].data(-1)
            if id is not None:
                self.delete_numbers.append(id)
            self.tw_vendor_number.removeRow(row)
        except:
            pass


class ClientAdress(QDialog, client_adress_class):
    def __init__(self):
        super(ClientAdress, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))


class ClientNumber(QDialog, client_number_class):
    def __init__(self):
        super(ClientNumber, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
