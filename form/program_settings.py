from os import getcwd
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from function import my_sql


settings_path_class, settings_path_base_class = loadUiType(getcwd() + '/ui/program_settings_path.ui')


class SettingsPath(QDialog, settings_path_class):
    def __init__(self):
        super(SettingsPath, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.set_info()

    def set_info(self):
        query = 'SELECT Name, program_settings_path.Values FROM program_settings_path'
        sql_ret = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_ret)):
            QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)
            return False

        for path in sql_ret:
            if path[0] == "Путь шаблон рабочие":
                self.le_work_templates_path.setText(path[1])
            if path[0] == "Путь корень рабочие":
                self.le_work_path.setText(path[1])

    def work_path(self):
        self.le_work_path.setText(QFileDialog.getExistingDirectory(self))

    def work_templates_path(self):
        self.le_work_templates_path.setText(QFileDialog.getExistingDirectory(self))

    def ok(self):
        query = "UPDATE program_settings_path SET `Values` = %s WHERE Name = %s"
        parametrs = ((self.le_work_templates_path.text(), "Путь шаблон рабочие"), (self.le_work_path.text(), "Путь корень рабочие"))
        sql_ret = my_sql.sql_many(query, parametrs)
        if "mysql.connector.errors" in str(type(sql_ret)):
            QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)
            return False


