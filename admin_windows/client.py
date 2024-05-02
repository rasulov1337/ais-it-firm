from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QMessageBox

from repositories.client import client_repository_impl, ClientModel


class ClientInfoWindow(QWidget):
    on_show_authwindow = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('admin_windows/client_info_window.ui', self)
        self.back_btn.clicked.connect(self.go_back)

        self.current_index = 0
        self.update_gui_data()

        self.prev_btn.clicked.connect(self.show_prev)
        self.next_btn.clicked.connect(self.show_next)
        self.save_btn.clicked.connect(self.update_client)
        self.del_btn.clicked.connect(self.delete_client)
        self.le_search.returnPressed.connect(self.search)

    def update_gui_data(self):
        client_name = self.le_search.text()
        if len(client_name) == 0:
            self.data = client_repository_impl.get_all() + [ClientModel()]
        else:
            self.data = client_repository_impl.find_by_name(client_name) + [ClientModel()]

        self.show_at_curr_index()

    def go_back(self):
        self.close()

    def show_at_curr_index(self):
        client_data = self.data[self.current_index]

        self.le_fullname.setText(client_data.fullname)
        self.le_telephone.setText(client_data.telephone)
        self.le_address.setText(client_data.address)
        self.le_email.setText(client_data.email)

        if client_data.is_company:
            self.rb_jur.setChecked(True)
        else:
            self.rb_phys.setChecked(True)

    def show_prev(self):
        if self.current_index < 1:
            self.create_msg_box('Невозможно перейти к предыдущей странице')
            return
        self.current_index -= 1
        self.show_at_curr_index()

    def show_next(self):
        if self.current_index == len(self.data) - 1:
            self.create_msg_box('Невозможно перейти к следующей странице')
            return
        self.current_index += 1
        self.show_at_curr_index()

    def create_msg_box(self, text):
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setWindowTitle('Ошибка')
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.exec()

    def update_client(self):
        client_info = ClientModel(self.data[self.current_index].id,
                                  self.le_fullname.text(),
                                  self.le_telephone.text(),
                                  self.le_address.text(),
                                  self.le_email.text(),
                                  self.rb_jur.isChecked())

        if client_info.id == 0:
            client_repository_impl.create(client_info)
        else:
            client_repository_impl.update(client_info)
        self.update_gui_data()

    def delete_client(self):
        client_id = self.data[self.current_index].id
        if client_id == 0:
            return

        if client_repository_impl.delete(client_id):
            self.data.pop(self.current_index)
            self.show_at_curr_index()
        else:
            self.create_msg_box('Could not delete client')

    def search(self):
        self.current_index = 0
        self.update_gui_data()
