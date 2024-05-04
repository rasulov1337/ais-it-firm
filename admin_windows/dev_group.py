from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QPushButton, \
    QAbstractItemView

from repositories.dev_group import dev_group_repo_impl, DevGroupModel
from repositories.employee import employee_repo_impl, EmployeeModel
from repositories.tech_stack import tech_stack_repo_impl

from admin_windows.base_window import BaseInfoWindow, create_msg_box


class DevGroupInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__(DevGroupModel, dev_group_repo_impl)

    def init_gui(self):
        self.le_name = QLineEdit()
        self.cb_tech_stack = QComboBox()

        for i in tech_stack_repo_impl.get_all():
            self.cb_tech_stack.addItem(i.tech_stack)

        self.tw_employees = QTableWidget()

        self.tw_employees.setColumnCount(5)
        self.tw_employees.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tw_employees.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tw_employees.setHorizontalHeaderItem(0, QTableWidgetItem('ID'))
        self.tw_employees.setHorizontalHeaderItem(1, QTableWidgetItem('ФИО'))
        self.tw_employees.setHorizontalHeaderItem(2, QTableWidgetItem('Дата рождения'))
        self.tw_employees.setHorizontalHeaderItem(3, QTableWidgetItem('Дата найма'))
        self.tw_employees.setHorizontalHeaderItem(4, QTableWidgetItem('Зарплата'))
        self.tw_employees.setColumnHidden(0, True)
        self.tw_employees.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.form_layout.addRow('Название', self.le_name)
        self.form_layout.addRow('Технологический стек', self.cb_tech_stack)
        self.form_layout.addRow(self.tw_employees)

        add_new_row_btn = QPushButton('Добавить новую строку')
        add_new_row_btn.clicked.connect(self.on_add_new_row_btn_clicked)

        del_selected_row_btn = QPushButton('Удалить выбранную строку')
        del_selected_row_btn.clicked.connect(self.on_del_selected_row_btn_clicked)

        self.btns_widget.layout().addWidget(add_new_row_btn)
        self.btns_widget.layout().addWidget(del_selected_row_btn)

        self.resize(1000, 600)

    def update(self):
        row_data = self.gather_data_from_gui_into_object()

        res = 0
        if row_data.id == 0:
            res = self.repo_impl.create(row_data)
        else:
            res = self.repo_impl.update(row_data)
        if not res:
            create_msg_box('Error! Could not create/update data')

        for i in range(self.tw_employees.rowCount()):
            if self.tw_employees.item(i, 0):
                id = self.tw_employees.item(i, 0).text()
            else:
                id = '0'

            fullname = self.tw_employees.item(i, 1).text()
            birth_date = self.tw_employees.item(i, 2).text()
            hire_date = self.tw_employees.item(i, 3).text()
            salary = self.tw_employees.item(i, 4).text()
            dev_group_id = self.data[self.current_index].id

            employee = EmployeeModel(id,
                                     fullname,
                                     birth_date,
                                     hire_date,
                                     salary,
                                     dev_group_id)

            if id == '0':
                res = employee_repo_impl.create(employee)
            else:
                res = employee_repo_impl.update(employee)
            if not res:
                create_msg_box('Не получилось создать разработчика')

        self.update_gui_data()

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
            self.tw_employees.setItem(index, 0, QTableWidgetItem(str(row.id))),
            self.tw_employees.setItem(index, 1, QTableWidgetItem(row.fullname))
            self.tw_employees.setItem(index, 2, QTableWidgetItem(row.birth_date.toString('yyyy-MM-dd')))
            self.tw_employees.setItem(index, 3, QTableWidgetItem(row.hire_date.toString('yyyy-MM-dd')))
            self.tw_employees.setItem(index, 4, QTableWidgetItem(str(row.salary)))

    @pyqtSlot()
    def on_add_new_row_btn_clicked(self):
        self.tw_employees.setRowCount(self.tw_employees.rowCount() + 1)

    @pyqtSlot()
    def on_del_selected_row_btn_clicked(self):
        selected_rows = self.tw_employees.selectionModel().selectedRows()
        if len(selected_rows) == 0:
            create_msg_box('Ни одна строка не выделена!')
            return

        emp_id = selected_rows[0].data()
        if not employee_repo_impl.delete(emp_id):
            create_msg_box('Не получилось удалить разработчика')
            return

        self.update_gui_data()
