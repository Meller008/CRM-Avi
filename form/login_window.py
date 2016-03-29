from os import getcwd

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUiType

from function import my_sql

login_class, login_base_class = loadUiType(getcwd() + '/ui/login.ui')


class LoginWindow(QDialog, login_class):
    def __init__(self, main_w, *args):
        self.main = main_w
        super(LoginWindow, self).__init__(*args)
        self.setupUi(self)

    def check_login(self):

            query = 'SELECT COUNT(*) FROM login WHERE Login.Login = %s AND Login.Password = %s'
            par = (self.le_login.text(), self.le_password.text())
            a = my_sql.sql_select(query, par)
            print(a)

            # self.main.login_access()
            # self.close()
            # self.destroy()
