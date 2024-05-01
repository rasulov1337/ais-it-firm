from PyQt6.QtWidgets import QLineEdit, QComboBox

from repositories.order import order_repo_impl, OrderModel
from repositories.program import program_repo_impl, ProgramModel
from repositories.dev_group import dev_group_repo_impl, DevGroupModel
from admin_windows.base_window import BaseInfoWindow
from repositories.tech_stack import tech_stack_repo_impl
from repositories.client import client_repository_impl, ClientModel


class ProgramInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__(ProgramModel, program_repo_impl)

    def init_gui(self):
        self.le_search = QLineEdit()
        self.le_name = QLineEdit()
        self.le_repo = QLineEdit()
        self.le_client = QLineEdit()
        self.cb_tech_stack = QComboBox()
        self.cb_order_id = QComboBox()
        self.cb_dev_group_id = QComboBox()

        self.le_client.setDisabled(True)

        self.le_search.returnPressed.connect(self.on_search_field_edit_finished)

        self.clients: list[ClientModel] = client_repository_impl.get_all()
        self.orders: list[OrderModel] = order_repo_impl.get_all()
        for i in self.orders:
            self.cb_order_id.addItem('Заказ №' + str(i.id), i.id)

        self.dev_groups: list[DevGroupModel] = dev_group_repo_impl.get_all()
        for i in self.dev_groups:
            self.cb_dev_group_id.addItem(i.name, i.id)

        for i in tech_stack_repo_impl.get_all():
            self.cb_tech_stack.addItem(i.tech_stack)

        self.form_layout.addRow('Поиск по названию', self.le_search)
        self.form_layout.addRow('Название', self.le_name)
        self.form_layout.addRow('Репозиторий', self.le_repo)
        self.form_layout.addRow('Технологический стек', self.cb_tech_stack)
        self.form_layout.addRow('Заказ', self.cb_order_id)
        self.form_layout.addRow('Клиент', self.le_client)
        self.form_layout.addRow('Группы разработки', self.cb_dev_group_id)

    def gather_data_from_gui_into_object(self):
        return ProgramModel(self.data[self.current_index].id,
                            self.le_repo.text(),
                            self.le_name.text(),
                            self.cb_tech_stack.currentText(),
                            self.cb_order_id.currentData(),
                            self.cb_dev_group_id.currentData())

    def show_at_curr_index(self):
        curr_data: ProgramModel = self.data[self.current_index]
        self.le_name.setText(curr_data.name)
        self.le_repo.setText(curr_data.repo)
        self.cb_order_id.setCurrentText('Заказ №' + str(curr_data.order_id))
        # In order not to make additional requests to the db let's not get employees for id = 0
        if curr_data.id == 0:
            return

        self.cb_tech_stack.setCurrentText(curr_data.tech_stack)

        for i in self.orders:
            if i.id == curr_data.order_id:
                for j in self.clients:
                    if j.id == i.client_id:
                        self.le_client.setText(j.fullname)

        for i in self.dev_groups:
            if i.id == curr_data.dev_group_id:
                self.cb_dev_group_id.setCurrentText(i.name)

    def on_search_field_edit_finished(self):
        search_query = self.le_search.text()
        if len(search_query) == 0:
            self.search_results = None
        else:
            self.search_results = program_repo_impl.get_programs_by_name(search_query)
        self.current_index = 0
        self.update_gui_data()
