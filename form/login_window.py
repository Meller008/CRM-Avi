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

            query = 'SELECT  COUNT(*) FROM login WHERE Login.Login = %s AND Login.Password = %s'
            login = self.le_login.text()
            password = self.le_password.text()
            par = (login.lower(), password.lower())
            sql_result = my_sql.sql_select(query, par)

            if sql_result[0][0] == 1:
                self.main.login_access()
                self.close()
                self.destroy()
            else:
                QMessageBox.information(self, "Что то не так", "Не верный логин или пароль")