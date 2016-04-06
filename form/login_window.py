from os import getcwd
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUiType
from function import my_sql

login_class, login_base_class = loadUiType(getcwd() + '/ui/login.ui')


class LoginWindow(QDialog, login_class):
    def __init__(self, *args):
        self.main = args[0]
        self.user = args[1]
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.setModal(True)

    def check_login(self):

            query = 'SELECT Login.Id, Login.Login, Login.Privilege FROM login WHERE Login.Login = %s AND Login.Password = %s'
            login = self.le_login.text()
            password = self.le_password.text()
            par = (login.lower(), password.lower())
            sql_result = my_sql.sql_select(query, par)

            if not sql_result:
                QMessageBox.information(self, "Что то не так", "Не верный логин или пароль")
            else:
                self.user.id = sql_result[0][0]
                self.user.login = sql_result[0][1]
                self.user.privilege = sql_result[0][2]
                self.main.login_access()
                self.close()
                self.destroy()
