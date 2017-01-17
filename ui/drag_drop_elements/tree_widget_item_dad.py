from PyQt5.QtWidgets import QTableWidget, QApplication, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QPoint, QMimeData
from PyQt5.QtGui import QDrag


class TreeWidgetItemDAD(QTreeWidgetItem):
    def __init__(self, parent):
        super().__init__(parent)

    def dragEnterEvent(self, event):
        if event.source() and event.source() != self:
            event.setDropAction(Qt.MoveAction)
            event.accept()

    def dragMoveEvent(self, event):
        if event.source() and event.source() != self:
            event.setDropAction(Qt.MoveAction)
            event.accept()

    def dropEvent(self, event):
        if event.source() and event.source() != self:
            event.setDropAction(Qt.MoveAction)
            event.accept()
            print(self.text())
