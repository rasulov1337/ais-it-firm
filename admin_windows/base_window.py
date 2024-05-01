from abc import abstractmethod, ABC
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QMessageBox


def create_msg_box(text):
    msg_box = QMessageBox()
    msg_box.setText(text)
    msg_box.setWindowTitle('Ошибка')
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.exec()


class BaseInfoWindow(QWidget):
    on_show_authwindow = pyqtSignal()

    def __init__(self, model_class, repo_impl, ui='admin_windows/base_window.ui'):
        super().__init__()
        uic.loadUi(ui, self)

        self.model_class = model_class
        self.repo_impl = repo_impl

        self.form_layout = self.formLayout

        self.init_gui()

        self.prev_btn.clicked.connect(self.show_prev)
        self.next_btn.clicked.connect(self.show_next)
        self.save_btn.clicked.connect(self.update)
        self.del_btn.clicked.connect(self.delete)
        self.back_btn.clicked.connect(self.go_back)
        self.le_search.returnPressed.connect(self.search)

        self.current_index = 0
        self.update_gui_data()

    def update_gui_data(self):
        client_name = self.le_search.text()
        if len(client_name) == 0:
            self.data = self.repo_impl.get_all() + [self.model_class()]
        else:
            self.data = self.repo_impl.find_by_name(client_name) + [self.model_class()]

        self.show_at_curr_index()

    def go_back(self):
        self.close()

    @abstractmethod
    def show_at_curr_index(self):
        pass

    def show_prev(self):
        if self.current_index < 1:
            create_msg_box('Невозможно перейти к предыдущей странице')
            return
        self.current_index -= 1
        self.show_at_curr_index()

    def show_next(self):
        if self.current_index == len(self.data) - 1:
            create_msg_box('Невозможно перейти к следующей странице')
            return
        self.current_index += 1
        self.show_at_curr_index()

    @abstractmethod
    def gather_data_from_gui_into_object(self):
        pass

    @abstractmethod
    def init_gui(self):
        pass

    def update(self):
        row_data = self.gather_data_from_gui_into_object()

        res = 0
        if row_data.id == 0:
            res = self.repo_impl.create(row_data)
        else:
            res = self.repo_impl.update(row_data)
        if not res:
            create_msg_box('Error! Could not create/update data')
        self.update_gui_data()

    def delete(self):
        id = self.data[self.current_index].id
        if id == 0:
            return

        if self.repo_impl.delete(id):
            self.data.pop(self.current_index)
            self.show_at_curr_index()
        else:
            create_msg_box('Could not delete client')

    def search(self):
        self.current_index = 0
        self.update_gui_data()
