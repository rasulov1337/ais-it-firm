from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QMessageBox, QComboBox

from repositories.employee import employee_repo_impl, EmployeeModel
from repositories.dev_group import dev_group_repo_impl


class EmployeeInfoWindow(QWidget):
    on_show_authwindow = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('admin_windows/employee.ui', self)

        # Let user select date
        self.de_hire.setCalendarPopup(True)
        self.de_birth.setCalendarPopup(True)

        for i in dev_group_repo_impl.get_all():
            self.cb_group.addItem(i.name, i.id)

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
            self.data = employee_repo_impl.get_all() + [EmployeeModel()]
        else:
            self.data = employee_repo_impl.find_by_name(client_name) + [EmployeeModel()]

        self.show_at_curr_index()

    def go_back(self):
        self.close()

    def show_at_curr_index(self):
        curr_data = self.data[self.current_index]

        self.le_fullname.setText(curr_data.fullname)
        self.le_salary.setText(str(curr_data.salary))
        self.de_hire.setDate(curr_data.hire_date)
        self.de_birth.setDate(curr_data.birth_date)
        self.cb_group.setCurrentText(dev_group_repo_impl.get(curr_data.dev_group_id).name)

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

    def update(self):
        row_data = EmployeeModel(self.data[self.current_index].id,
                                 self.le_fullname.text(),
                                 self.de_birth.date().toString('yyyy-MM-dd'),
                                 self.de_hire.date().toString('yyyy-MM-dd'),
                                 self.le_salary.text(),
                                 self.cb_group.currentData())

        if row_data.id == 0:
            res = employee_repo_impl.create(row_data)
        else:
            res = employee_repo_impl.update(row_data)
        if not res:
            self.create_msg_box('Error! Could not create/update data')
        self.update_gui_data()

    def delete(self):
        id = self.data[self.current_index].id
        if id == 0:
            return

        if employee_repo_impl.delete(id):
            self.data.pop(self.current_index)
            self.show_at_curr_index()
        else:
            self.create_msg_box('Could not delete client')

    def search(self):
        self.current_index = 0
        self.update_gui_data()
