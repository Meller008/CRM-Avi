from form import material_provider


class AccessoriesName(material_provider.MaterialName):
    def set_sql_query(self):
        self.sql_list = "SELECT accessories_name.Name FROM accessories_name"
        self.sql_add = "INSERT INTO accessories_name (Name, Information) VALUES (%s, %s)"
        self.sql_change_select = "SELECT accessories_name.Name, accessories_name.Information FROM accessories_name WHERE  Name = %s"
        self.sql_update_select = 'UPDATE accessories_name SET accessories_name.Name = %s, accessories_name.Information = %s ' \
                                 'WHERE accessories_name.Name = %s'
        self.sql_dell = "DELETE FROM accessories_name WHERE accessories_name.Name = %s"

    def set_settings(self):
        self.setWindowTitle("Названия фурнитур")
        self.toolBar.setStyleSheet("background-color: rgb(251, 110, 255);")
        self.add_title = "Добавить фурнитуру"
        self.change_title = "Изменить фурнитуру"


class AccessoriesProvider(material_provider.MaterialProvider):
    def set_settings(self):
        self.setWindowTitle("Поставщики фурнитуры")
        self.toolBar.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.add_title = "Добавить поставщика"
        self.change_title = "Изменить поставщика"

    def set_sql_query(self):
        self.sql_list = "SELECT accessories_provider.Name FROM accessories_provider"
        self.sql_add = "INSERT INTO avi_crm.accessories_provider (Name, Information) VALUES (%s, %s)"
        self.sql_change_select = "SELECT accessories_provider.Name, accessories_provider.Information FROM accessories_provider WHERE  Name = %s"
        self.sql_update_select = 'UPDATE accessories_provider SET accessories_provider.Name = %s, accessories_provider.Information = %s ' \
                                 'WHERE accessories_provider.Name = %s'
        self.sql_dell = "DELETE FROM accessories_provider WHERE accessories_provider.Name = %s"

    def double_click_provider(self, select_prov):
        if not self.dc_select:
            self.change_provider = material_provider.ChangeMaterialProvider(self, select_prov.text())
            self.change_provider.show()
        else:
            self.m_class.le_provider.setText(select_prov.text())
            self.close()
            self.destroy()
