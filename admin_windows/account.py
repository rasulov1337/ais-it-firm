from PyQt6.QtWidgets import QLineEdit, QComboBox

from repositories.account import account_repo_impl, AccountModel
from repositories.client import client_repository_impl, ClientModel
from admin_windows.base_window import BaseInfoWindow


class AccountInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__(AccountModel, account_repo_impl)

    def init_gui(self):
        self.cb_client = QComboBox()
        self.le_login = QLineEdit()
        self.le_password = QLineEdit()
        self.cb_type = QComboBox()

        self.le_login.setMaxLength(16)
        self.le_password.setMaxLength(16)

        self.cb_type.addItems([AccountModel.Type.USER, AccountModel.Type.ADMIN])
        self.clients = [ClientModel(fullname='-')] + client_repository_impl.get_names_and_ids()
        for i in self.clients:
            self.cb_client.addItem(i.fullname, userData=i.id)

        self.form_layout.addRow('Клиент', self.cb_client)
        self.form_layout.addRow('Логин', self.le_login)
        self.form_layout.addRow('Пароль', self.le_password)
        self.form_layout.addRow('Тип', self.cb_type)

    def gather_data_from_gui_into_object(self):
        return AccountModel(self.data[self.current_index].id,
                            self.cb_client.currentData(),
                            self.le_login.text(),
                            self.le_password.text(),
                            self.cb_type.currentText())

    def show_at_curr_index(self):
        curr_data = self.data[self.current_index]
        self.le_login.setText(curr_data.login)
        self.le_password.setText(curr_data.password)
        if curr_data.client_id == 0:
            self.cb_client.setCurrentText('-')
        else:
            for i in self.clients:
                if i.id == curr_data.client_id:
                    self.cb_client.setCurrentText(i.fullname)
        self.cb_type.setCurrentText(curr_data.type)
