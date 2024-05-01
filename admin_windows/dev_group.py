from PyQt6.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox

from repositories.dev_group import dev_group_repo_impl, DevGroupModel
from repositories.employee import employee_repo_impl
from repositories.tech_stack import tech_stack_repo_impl

from admin_windows.base_window import BaseInfoWindow


class DevGroupInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__(DevGroupModel, dev_group_repo_impl)

    def init_gui(self):
        self.le_name = QLineEdit()
        self.cb_tech_stack = QComboBox()

        for i in tech_stack_repo_impl.get_all():
            self.cb_tech_stack.addItem(i.tech_stack)

        self.tw_employees = QTableWidget()
        self.tw_employees.setStyleSheet("""
QHeaderView::section {
	background-color: black;
	color: white;
}""")

        self.tw_employees.setColumnCount(4)
        self.tw_employees.setHorizontalHeaderItem(0, QTableWidgetItem('ФИО'))
        self.tw_employees.setHorizontalHeaderItem(1, QTableWidgetItem('Дата рождения'))
        self.tw_employees.setHorizontalHeaderItem(2, QTableWidgetItem('Дата найма'))
        self.tw_employees.setHorizontalHeaderItem(3, QTableWidgetItem('Зарплата'))
        self.tw_employees.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.form_layout.addRow('Название', self.le_name)
        self.form_layout.addRow('Технологический стек', self.cb_tech_stack)
        self.form_layout.addRow(self.tw_employees)

    def gather_data_from_gui_into_object(self):
        return DevGroupModel(self.data[self.current_index].id,
                             self.le_name.text(),
                             self.cb_tech_stack.currentText())

    def show_at_curr_index(self):
        curr_data: DevGroupModel = self.data[self.current_index]
        self.le_name.setText(curr_data.name)

        # In order not to make additional requests to the db let's not get employees for id = 0
        if curr_data.id == 0:
            return

        self.cb_tech_stack.setCurrentText(curr_data.tech_stack)

        table_data = employee_repo_impl.get_employees_by_dev_group_id(curr_data.id)
        self.tw_employees.setRowCount(len(table_data))
        for index, row in enumerate(table_data):
            self.tw_employees.setItem(index, 0, QTableWidgetItem(row.fullname))
            self.tw_employees.setItem(index, 1, QTableWidgetItem(row.birth_date.toString('yyyy-MM-dd')))
            self.tw_employees.setItem(index, 2, QTableWidgetItem(row.hire_date.toString('yyyy-MM-dd')))
            self.tw_employees.setItem(index, 3, QTableWidgetItem(row.salary))
