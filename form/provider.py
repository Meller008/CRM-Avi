from form.templates import list


class ProviderMaterial(list.ListItems):
    def set_settings(self):
        self.setWindowTitle("Поставщики ткани")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(255, 170, 0);")  # Цвет бара
        self.title_new_window = "Поставщик"  # Имя вызываемых окон

        self.sql_list = "SELECT Id, Name FROM material_provider ORDER BY Name"
        self.sql_add = "INSERT INTO material_provider (Name, Information) VALUES (%s, %s)"
        self.sql_change_select = "SELECT Name, Information FROM material_provider WHERE Id = %s"
        self.sql_update_select = 'UPDATE material_provider SET Name = %s, Information = %s WHERE id = %s'
        self.sql_dell = "DELETE FROM material_provider WHERE Id = %s"

        self.set_new_win = {"WinTitle": "Поставщик",
                            "WinColor": "(255, 170, 0)",
                            "lb_name": "Название",
                            "lb_note": "Информация"}

    def ui_double_click_item(self, select_prov):
        if not self.dc_select:
            self.ui_change_item(select_prov.data(3))
        else:
            item = (select_prov.data(3), select_prov.text())
            self.m_class.of_list_reason_provider_material(item)
            self.close()
            self.destroy()


class ProviderAccessories(list.ListItems):
    def set_settings(self):
        self.setWindowTitle("Поставщики фурнитуры")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(255, 255, 127);")  # Цвет бара
        self.title_new_window = "Поставщик"  # Имя вызываемых окон

        self.sql_list = "SELECT Id, Name FROM accessories_provider ORDER BY Name"
        self.sql_add = "INSERT INTO accessories_provider (Name, Information) VALUES (%s, %s)"
        self.sql_change_select = "SELECT Name, Information FROM accessories_provider WHERE Id = %s"
        self.sql_update_select = 'UPDATE accessories_provider SET Name = %s, Information = %s WHERE id = %s'
        self.sql_dell = "DELETE FROM accessories_provider WHERE Id = %s"

        self.set_new_win = {"WinTitle": "Поставщик",
                            "WinColor": "(255, 255, 127)",
                            "lb_name": "Название",
                            "lb_note": "Информация"}

    def ui_double_click_item(self, select_prov):
        if not self.dc_select:
            self.ui_change_item(select_prov.data(3))
        else:
            item = (select_prov.data(3), select_prov.text())
            self.m_class.of_list_reason_provider_accessories(item)
            self.close()
            self.destroy()