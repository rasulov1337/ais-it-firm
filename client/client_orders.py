from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QDateEdit, QCheckBox, QMessageBox, QTableWidgetItem, \
    QHeaderView, QLabel

import consts
from consts import DATE_FORMAT
from repositories.dev_group import dev_group_repo_impl
from repositories.order import order_repo_impl, OrderModel

from client.about import AboutWindow
from repositories.program import ProgramModel, program_repo_impl


def create_msg_box(text):
    msg_box = QMessageBox()
    msg_box.setText(text)
    msg_box.setWindowTitle('Ошибка')
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.exec()


class ClientOrdersWindow(QWidget):
    on_show_authwindow = pyqtSignal()

    def __init__(self, id):
        super().__init__()
        uic.loadUi('client/client_orders.ui', self)
        self.setStyleSheet(consts.STYLESHEET)

        self.le_order_id.setDisabled(True)
        self.le_price.setDisabled(True)
        self.deadline.setDisabled(True)
        self.created_at.setDisabled(True)
        self.cb_is_done.setDisabled(True)

        self.tw_programs.setColumnCount(4)
        self.tw_programs.setHorizontalHeaderItem(0, QTableWidgetItem('Название'))
        self.tw_programs.setHorizontalHeaderItem(1, QTableWidgetItem('Репозиторий'))
        self.tw_programs.setHorizontalHeaderItem(2, QTableWidgetItem('Технологический стек'))
        self.tw_programs.setHorizontalHeaderItem(3, QTableWidgetItem('Группа разработки'))
        self.tw_programs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.current_index = 0
        self.data = order_repo_impl.get_orders_by_client_id(id)
        self.show_at_curr_index()

    @pyqtSlot()
    def on_go_back_btn_clicked(self):
        self.close()

    @pyqtSlot()
    def on_prev_btn_clicked(self):
        if self.current_index < 1:
            create_msg_box('Невозможно перейти к предыдущей странице')
            return
        self.current_index -= 1
        self.show_at_curr_index()

    @pyqtSlot()
    def on_next_btn_clicked(self):
        if self.current_index == len(self.data) - 1:
            create_msg_box('Невозможно перейти к следующей странице')
            return
        self.current_index += 1
        self.show_at_curr_index()

    @pyqtSlot()
    def on_back_btn_clicked(self):
        self.on_show_authwindow.emit()
        self.close()

    @pyqtSlot()
    def on_about_btn_clicked(self):
        self.about_window = AboutWindow(self.data)
        self.about_window.show()

    def show_at_curr_index(self):
        curr_data: OrderModel = self.data[self.current_index]

        self.le_order_id.setText(str(curr_data.id))
        self.le_price.setText(curr_data.price)
        self.deadline.setDate(curr_data.deadline)
        self.created_at.setDate(curr_data.creation_date)
        self.cb_is_done.setChecked(curr_data.done)

        table_data: list[ProgramModel] = program_repo_impl.get_programs_by_order_id(curr_data.id)
        self.tw_programs.setRowCount(len(table_data))
        for index, row in enumerate(table_data):
            dev_group_name = dev_group_repo_impl.get(row.dev_group_id).name
            print(dev_group_name)
            self.tw_programs.setItem(index, 0, QTableWidgetItem(row.name))
            self.tw_programs.setCellWidget(index, 1, QLabel('<a href={0}>{1}</a>'.format(row.repo, row.repo)))
            self.tw_programs.setItem(index, 2, QTableWidgetItem(row.tech_stack))
            self.tw_programs.setItem(index, 3, QTableWidgetItem(dev_group_name))
