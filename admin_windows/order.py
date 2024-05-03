from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit, QComboBox, QCheckBox, \
    QAbstractItemView

from repositories.dev_group import dev_group_repo_impl
from repositories.order import order_repo_impl, OrderModel
from repositories.client import client_repository_impl
from admin_windows.base_window import BaseInfoWindow
from repositories.program import program_repo_impl, ProgramModel
from consts import DATE_FORMAT


class OrderInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__(OrderModel, order_repo_impl)

    def init_gui(self):
        self.le_order_id = QLineEdit()
        self.le_price = QLineEdit()
        self.de_deadline = QDateEdit(QDate.currentDate())
        self.cb_client = QComboBox()
        self.de_creation_date = QDateEdit(QDate.currentDate())
        self.checkbox_done = QCheckBox()

        self.le_order_id.setDisabled(True)
        self.de_deadline.setCalendarPopup(True)
        self.de_creation_date.setCalendarPopup(True)

        self.clients = client_repository_impl.get_all()
        for i in self.clients:
            self.cb_client.addItem(i.fullname, i.id)

        self.tw_programs = QTableWidget()

        self.tw_programs.setColumnCount(4)
        self.tw_programs.setHorizontalHeaderItem(0, QTableWidgetItem('Название'))
        self.tw_programs.setHorizontalHeaderItem(1, QTableWidgetItem('Репозиторий'))
        self.tw_programs.setHorizontalHeaderItem(2, QTableWidgetItem('Технологический стек'))
        self.tw_programs.setHorizontalHeaderItem(3, QTableWidgetItem('Группа разработки'))
        self.tw_programs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.form_layout.addRow('Номер заказа', self.le_order_id)
        self.form_layout.addRow('Стоимость', self.le_price)
        self.form_layout.addRow('Дедлайн', self.de_deadline)
        self.form_layout.addRow('Клиент', self.cb_client)
        self.form_layout.addRow('Дата создания', self.de_creation_date)
        self.form_layout.addRow('Выполнен?', self.checkbox_done)
        self.form_layout.addRow(self.tw_programs)

    def gather_data_from_gui_into_object(self):
        return OrderModel(self.data[self.current_index].id,
                          self.le_price.text(),
                          self.de_deadline.date().toString(DATE_FORMAT),
                          self.cb_client.currentData(),
                          self.de_creation_date.date().toString(DATE_FORMAT),
                          self.checkbox_done.isChecked())

    def show_at_curr_index(self):
        curr_data = self.data[self.current_index]
        self.le_order_id.setText(str(curr_data.id))
        self.le_price.setText(str(curr_data.price))
        self.de_deadline.setDate(curr_data.deadline)
        self.de_creation_date.setDate(curr_data.creation_date)
        self.checkbox_done.setChecked(curr_data.done)

        # In order not to make additional requests to the db let's not get employees for id = 0
        if curr_data.id == 0:
            return

        for i in self.clients:
            if i.id == curr_data.client_id:
                self.cb_client.setCurrentText(i.fullname)

        table_data: list[ProgramModel] = program_repo_impl.get_programs_by_order_id(curr_data.id)
        self.tw_programs.setRowCount(len(table_data))
        for index, row in enumerate(table_data):
            dev_group_name = dev_group_repo_impl.get(row.dev_group_id).name
            print(dev_group_name)
            self.tw_programs.setItem(index, 0, QTableWidgetItem(row.name))
            self.tw_programs.setItem(index, 1, QTableWidgetItem(row.repo))
            self.tw_programs.setItem(index, 2, QTableWidgetItem(row.tech_stack))
            self.tw_programs.setItem(index, 3, QTableWidgetItem(dev_group_name))
