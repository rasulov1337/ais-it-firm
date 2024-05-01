from PyQt6.QtWidgets import QLineEdit, QComboBox, QSpinBox

from admin_windows.base_window import BaseInfoWindow
from repositories.hardware import hardware_repo_impl, HardwareModel


class HardwareInfoWindow(BaseInfoWindow):
    def __init__(self):
        super().__init__(HardwareModel, hardware_repo_impl)

    def init_gui(self):
        self.le_id = QLineEdit()
        self.le_internet_speed = QLineEdit()
        self.le_gpu = QLineEdit()
        self.le_cpu = QLineEdit()
        self.sb_ram = QSpinBox()

        self.le_id.setDisabled(True)

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

        # # In order not to make additional requests to the db let's not get employees for id = 0
        # if curr_data.id == 0:
        #     return
        #
        # self.cb_tech_stack.setCurrentText(curr_data.tech_stack)
        #
        # for i in self.orders:
        #     if i.id == curr_data.order_id:
        #         for j in self.clients:
        #             if j.id == i.client_id:
        #                 self.le_client.setText(j.fullname)
        #
        # for i in self.dev_groups:
        #     if i.id == curr_data.dev_group_id:
        #         self.cb_dev_group_id.setCurrentText(i.name)
