from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from form import pack


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

        self.pack = pack.PackBrows(pack_id=id)
        self.pack.setModal(True)
        self.pack.show()

    def keyPressEvent(self, event):
        if event.key() == 16777221 or event.key() == 16777220:
            self.ui_acc_id()
        event.accept()