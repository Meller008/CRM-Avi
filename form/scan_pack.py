from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from form import pack
from function import my_sql


scan_pack = loadUiType(getcwd() + '/ui/scan_pack.ui')[0]


class ScanPack(QDialog, scan_pack):
    def __init__(self):
        super(ScanPack, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

    def ui_acc_id(self):
        try:
            id = int(self.le_number.text())
        except:
            return False

        query = """SELECT COUNT(Id) FROM pack WHERE Id = %s"""
        count_id = my_sql.sql_select(query, (id, ))
        if "mysql.connector.errors" in str(type(count_id)):
            QMessageBox.critical(self, "Ошибка sql поиска пачки", count_id.msg, QMessageBox.Ok)
            return False

        if count_id[0][0] != 1:
            QMessageBox.information(self, "Ошибка номера", "Нет пачки с таким номером", QMessageBox.Ok)
            return False

        self.pack = pack.PackBrows(pack_id=id)
        self.pack.setModal(True)
        self.pack.show()

    def keyPressEvent(self, event):
        if event.key() == 16777221 or event.key() == 16777220:
            self.ui_acc_id()
        event.accept()