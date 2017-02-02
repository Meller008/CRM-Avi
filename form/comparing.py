from form.templates import list


class ComparingName(list.ListItems):
    def set_settings(self):
        self.setWindowTitle("Прочие расходы")  # Имя окна
        self.toolBar.setStyleSheet("background-color: rgb(170, 255, 127);")  # Цвет бара
        self.title_new_window = "Расход"  # Имя вызываемых окон

        self.sql_list = "SELECT comparing_name.Id, comparing_name.Name FROM comparing_name ORDER BY comparing_name.Name"
        self.sql_add = "INSERT INTO comparing_name (Name, Information) VALUES (%s, %s)"
        self.sql_change_select = "SELECT comparing_name.Name, comparing_name.Information FROM comparing_name WHERE  Name = %s"
        self.sql_update_select = 'UPDATE comparing_name SET comparing_name.Name = %s, comparing_name.Information = %s WHERE comparing_name.Name = %s'
        self.sql_dell = "DELETE FROM comparing_name WHERE comparing_name.Name = %s"

        self.set_new_win = {"WinTitle": "Расход",
                            "WinColor": "(170, 255, 127)",
                            "lb_name": "Название",
                            "lb_note": "Информация"}

    def ui_double_click_item(self, select_prov):
        if not self.dc_select:
            self.ui_change_item(select_prov.data(3))
        else:
            item = (select_prov.data(3), select_prov.text())
            self.m_class.of_list_reason_comparing_material(item)
            self.close()
            self.destroy()
