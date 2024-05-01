from PyQt6.QtWidgets import QLineEdit

from repositories.tech_stack import tech_stack_repo_impl, TechStackModel
from admin_windows.base_window import BaseInfoWindow


class TechStackInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__(TechStackModel, tech_stack_repo_impl)

    def init_gui(self):
        self.le_stack_name = QLineEdit()

        self.form_layout.addRow('Технологический стек', self.le_stack_name)

    def gather_data_from_gui_into_object(self):
        return TechStackModel(self.data[self.current_index].id,
                              self.le_stack_name.text())

    def show_at_curr_index(self):
        self.le_stack_name.setText(self.data[self.current_index].tech_stack)
