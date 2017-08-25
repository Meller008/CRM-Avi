from os import getcwd, path, mkdir, listdir
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
from function import my_sql
import socket


label_settings = loadUiType(getcwd() + '/ui/print_birk_settings.ui')[0]
label_file = loadUiType(getcwd() + '/ui/print_birk_file.ui')[0]

IP_SERV_LABEL = "192.168.1.3"


class LabelFile(QDialog, label_file):
    def __init__(self, article_parametr_id, path_name, data=None):
        super(LabelFile, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.data = data

        query = """SELECT product_article.Article, product_article_size.Size, product_article_parametrs.Name
                      FROM product_article LEFT JOIN product_article_size ON product_article.Id = product_article_size.Article_Id
                      LEFT JOIN product_article_parametrs ON product_article_size.Id = product_article_parametrs.Product_Article_Size_Id
                      WHERE product_article_parametrs.Id = %s"""
        info_sql = my_sql.sql_select(query, (article_parametr_id, ))
        if "mysql.connector.errors" in str(type(info_sql)):
                QMessageBox.critical(self, "Ошибка sql", info_sql.msg, QMessageBox.Ok)

        dir_name = info_sql[0][0] + " " + info_sql[0][1] + " " + info_sql[0][2]

        self.full_path = self.inspection_files(dir_name, path_name)

    def ui_select_label(self, item):
        path = self.full_path + "/" + item.text()
        self.print = LabelSettings(path, self.data)
        self.print.setModal(True)
        self.print.show()
        if self.print.exec() > 0:
            self.close()
            self.destroy()

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
        dir_name = dir_name.replace("/", "-")
        self.path = self.inspection_path(dir_name, sql_dir_name)
        if self.path:
            self.lw_label.clear()
            files = listdir("%s/%s" % (self.path_wor, dir_name))
            for file in files:
                if "~" not in file:
                    r = path.splitext(file)  # Получаем название и расширение
                    if "xlsx" in r[1][1:] or "xlsm" in r[1] or "xls" in r[1] or "xlt" in r[1]:
                        ico = "xlsx"
                    elif "xml" in r[1][1:] or "docx" in r[1] or "doc" in r[1] or "docm" in r[1]:
                        ico = "xml"
                    elif "png" in r[1].lower() or "jpg" in r[1] or "jpeg" in r[1] or "jpe" in r[1] or "gif" in r[1] or "bmp" in r[1]:
                        ico = "image"
                    elif "pdf" in r[1]:
                        ico = "pdf"
                    elif "btw" in r[1]:
                        ico = "btw"
                    else:
                        ico = "other"

                    list_item = QListWidgetItem(r[0] + r[1])
                    list_item.setIcon(QIcon(getcwd() + "/images/%s.ico" % ico))
                    self.lw_label.addItem(list_item)
            return self.path


class LabelSettings(QDialog, label_settings):
    def __init__(self, path, data=None):
        super(LabelSettings, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.label_data = {"label_path": path.replace("/", '\\'),
                           "label_value": "None",
                           "label_print": "None",
                           "article": "None",
                           "article_size": "None",
                           "article_parametr": "None",
                           "article_barcode": "None",
                           "pack_id": "None",
                           "clients_vendor": "None",
                           "date_order": "None",
                           "number_order": "None",
                           "date_now": QDate.currentDate().toString("MM.yyyy")}

        self.le_label_path.setText(path)

        if data:
            for key, val in data.items():
                if self.label_data.get(key, False) != False:
                    self.label_data[key] = str(val)

    def ui_print_tcp(self):

        self.label_data["label_value"] = self.le_value.value()
        self.label_data["label_print"] = self.cb_printer.currentText()

        conn = socket.socket()
        try:
            conn.connect((IP_SERV_LABEL, 6666))
        except TimeoutError:
            return False

        conn.send(bytes(str(self.label_data), encoding='utf-8'))
        conn.send(b"data_ok")

        self.done(1)

    def ui_can(self):
        self.done(-1)
        self.close()
        self.destroy()