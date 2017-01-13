from os import getcwd
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUiType
from function import my_sql
from PyQt5.QtGui import QIcon
from classes.my_class import User

login_class, login_base_class = loadUiType(getcwd() + '/ui/login.ui')


class LoginWindow(QDialog, login_class):
    def __init__(self, *args):
        self.main = args[0]
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.setModal(True)
        self.show()

        self.check_login()

    def check_login(self):

            query = """SELECT staff_worker_login.Worker_Info_Id
                      FROM staff_worker_login
                      WHERE staff_worker_login.Login = %s AND BINARY staff_worker_login.Password = %s"""
            login = self.le_login.text()
            password = self.le_password.text()
            sql_result = my_sql.sql_select(query, (login, password))

            if not sql_result:
                QMessageBox.information(self, "Что то не так", "Не верный логин или пароль", QMessageBox.Ok)
            else:
                User().set_id(sql_result[0][0])
                self.main.login_access()
                self.close()
                self.destroy()
