from PyQt5.QtWidgets import QTableWidget, QApplication
from PyQt5.QtCore import Qt, QPoint, QMimeData
from PyQt5.QtGui import QDrag


class TableWidgetDAD(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        self.start_mouse_drag = event.pos()
        QTableWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if not event.buttons() and Qt.LeftButton:
            return
        distance = (event.pos() - self.start_mouse_drag).manhattanLength()
        if distance < QApplication.startDragDistance():
            return
        item = self.selectedItems()[0]
        text = "<row>" + str(item.row()) + "<row>" + "<col>" + str(item.column()) + "<col>" + "<text>" + str(item.text()) + "<text>"
        print(text)
        drag = QDrag(self)
        mim_data = QMimeData()
        mim_data.setText(text)
        drag.setMimeData(mim_data)
        dropAction = drag.exec_(Qt.MoveAction)
