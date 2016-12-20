from PyQt5.QtWidgets import QApplication
import sys
import form.main_window

try:
    app = QApplication(sys.argv)
    main = form.main_window.MainWindow()
    sys.exit(app.exec_())
except:
    print("123")
