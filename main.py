from PyQt5.QtWidgets import QApplication
import sys, traceback
import form.main_window
from datetime import datetime


def ex(t, v, tb):
    with open("ERR.txt", "a") as file:
        file.write("\n---===Error===---\n")
        file.write("Time = %s" % datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        traceback.print_exception(t, v, tb, file=file)

sys.excepthook = ex

app = QApplication(sys.argv)
main = form.main_window.MainWindow()
sys.exit(app.exec_())

