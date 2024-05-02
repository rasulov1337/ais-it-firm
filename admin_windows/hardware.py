from PyQt6.QtWidgets import QLineEdit, QSpinBox, QTableWidget, QTableWidgetItem, QHeaderView

from admin_windows.base_window import BaseInfoWindow
from repositories.dev_group import dev_group_repo_impl
from repositories.hardware import hardware_repo_impl, HardwareModel
from repositories.employee import employee_repo_impl, EmployeeModel


class HardwareInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__(HardwareModel, hardware_repo_impl)

    def init_gui(self):
        self.le_id = QLineEdit()
        self.le_internet_speed = QLineEdit()
        self.le_gpu = QLineEdit()
        self.le_cpu = QLineEdit()
        self.sb_ram = QSpinBox()
        self.tw_employees = QTableWidget()  # Employees that use this hardware

        self.le_id.setDisabled(True)

        self.tw_employees.setColumnCount(5)
        self.tw_employees.setHorizontalHeaderItem(0, QTableWidgetItem('ФИО'))
        self.tw_employees.setHorizontalHeaderItem(1, QTableWidgetItem('Дата рождения'))
        self.tw_employees.setHorizontalHeaderItem(2, QTableWidgetItem('Зарплата'))
        self.tw_employees.setHorizontalHeaderItem(3, QTableWidgetItem('Дата найма'))
        self.tw_employees.setHorizontalHeaderItem(4, QTableWidgetItem('Группа разработки'))
        self.tw_employees.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # self.clients: list[ClientModel] = client_repository_impl.get_all()
        # self.orders: list[OrderModel] = order_repo_impl.get_all()
        # for i in self.orders:
        #     self.cb_order_id.addItem('Заказ №' + str(i.id), i.id)
        #
        # self.dev_groups: list[DevGroupModel] = dev_group_repo_impl.get_all()
        # for i in self.dev_groups:
        #     self.cb_dev_group_id.addItem(i.name, i.id)
        #
        # for i in tech_stack_repo_impl.get_all():
        #     self.cb_tech_stack.addItem(i.tech_stack)

        self.form_layout.addRow('ID Оборудования', self.le_id)
        self.form_layout.addRow('Скорость интернета', self.le_internet_speed)
        self.form_layout.addRow('Модель видеокарты', self.le_gpu)
        self.form_layout.addRow('Процессор', self.le_cpu)
        self.form_layout.addRow('ОЗУ', self.sb_ram)
        self.form_layout.addRow(self.tw_employees)

    def gather_data_from_gui_into_object(self):
        curr_id = self.data[self.current_index].id
        return HardwareModel(curr_id,
                             self.le_internet_speed.text(),
                             self.le_gpu.text(),
                             self.le_cpu.text(),
                             self.sb_ram.value())

    def show_at_curr_index(self):
        curr_data: HardwareModel = self.data[self.current_index]
        self.le_id.setText(str(curr_data.id))
        self.le_internet_speed.setText(str(curr_data.internet_speed))
        self.le_gpu.setText(curr_data.gpu)
        self.le_cpu.setText(curr_data.cpu)
        self.sb_ram.setValue(curr_data.ram)

        if curr_data.id == 0:
            return

        table_data: list[EmployeeModel] = employee_repo_impl.get_employees_by_hardware_id(curr_data.id)
        self.tw_employees.setRowCount(len(table_data))
        for index, row in enumerate(table_data):
            dev_group_name = dev_group_repo_impl.get(row.dev_group_id).name
            self.tw_employees.setItem(index, 0, QTableWidgetItem(row.fullname))
            self.tw_employees.setItem(index, 1, QTableWidgetItem(row.birth_date.toString('yyyy-MM-dd')))
            self.tw_employees.setItem(index, 2, QTableWidgetItem(row.salary))
            self.tw_employees.setItem(index, 3, QTableWidgetItem(row.hire_date.toString('yyyy-MM-dd')))
            self.tw_employees.setItem(index, 4, QTableWidgetItem(dev_group_name))
