import os
from PyQt5.QtWidgets import QApplication
import sys, traceback, time
from datetime import datetime

try:
    import form.main_window
except:
    print(1)
    os.system("install_pack.py")
    print(0)
    import form.main_window


def ex(t, v, tb):
    print(traceback.print_exception(t, v, tb))
    with open("ERR.txt", "a") as file:
        file.write("\n---===Error===---\n")
        file.write("Time = %s" % datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        traceback.print_exception(t, v, tb, file=file)
    while 1:
        time.sleep(5)

sys.excepthook = ex

if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = form.main_window.MainWindow(sys.argv)
    sys.exit(app.exec_())

