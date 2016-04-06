from form import material_provider


class ComparingName(material_provider.MaterialProvider):
    def set_sql_query(self):
        self.sql_list = "SELECT comparing_name.Name FROM comparing_name"
        self.sql_add = "INSERT INTO comparing_name (Name, Information) VALUES (%s, %s)"
        self.sql_change_select = "SELECT comparing_name.Name, comparing_name.Information FROM comparing_name WHERE  Name = %s"
        self.sql_update_select = 'UPDATE comparing_name SET comparing_name.Name = %s, comparing_name.Information = %s ' \
                                 'WHERE comparing_name.Name = %s'
        self.sql_dell = "DELETE FROM comparing_name WHERE comparing_name.Name = %s"

    def set_settings(self):
        self.setWindowTitle("Прочие растраты")
        self.toolBar.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.add_title = "Добавить прочие растр."
        self.change_title = "Изменить прочие растр."
