from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView

import consts
from repositories.client import client_repository_impl

from client.about import AboutWindow
from client.client_orders import ClientOrdersWindow
from repositories.order import OrderModel
from repositories.program import program_repo_impl, ProgramModel


class ReportWindow(QWidget):
    on_show_authwindow = pyqtSignal()

    def __init__(self, id):
        super().__init__()
        self.data = client_repository_impl.get(id)
        uic.loadUi('client/client_report.ui', self)
        self.setStyleSheet(consts.STYLESHEET)

        self.label.setText('Заказы клиента ' + self.data.fullname)

        self.tw.setColumnCount(8)
        self.tw.setHorizontalHeaderItem(0, QTableWidgetItem('Стоимость заказа'))
        self.tw.setHorizontalHeaderItem(1, QTableWidgetItem('Дедлайн'))
        self.tw.setHorizontalHeaderItem(2, QTableWidgetItem('Дата создания'))
        self.tw.setHorizontalHeaderItem(3, QTableWidgetItem('Выполнен?'))
        self.tw.setHorizontalHeaderItem(4, QTableWidgetItem('Название'))
        self.tw.setHorizontalHeaderItem(5, QTableWidgetItem('Репозиторий'))
        self.tw.setHorizontalHeaderItem(6, QTableWidgetItem('Технологический стек'))
        self.tw.setHorizontalHeaderItem(7, QTableWidgetItem('Группа разработки'))
        self.tw.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # table_data: list[ProgramModel] = program_repo_impl.get_programs_by_order_id(curr_data.id)
        table_data: list[ProgramModel, OrderModel, str] = program_repo_impl.get_programs_and_their_orders(self.data.id)
        self.tw.setRowCount(len(table_data))
        overall_price = 0
        for index, (program_data, order_data, group_name) in enumerate(table_data):
            # dev_group_name = dev_group_repo_impl.get(row.dev_group_id).name
            self.tw.setItem(index, 0, QTableWidgetItem(str(order_data.price)))
            self.tw.setItem(index, 1, QTableWidgetItem(order_data.deadline.toString(consts.DATE_FORMAT)))
            self.tw.setItem(index, 2, QTableWidgetItem(order_data.creation_date.toString(consts.DATE_FORMAT)))
            self.tw.setItem(index, 3, QTableWidgetItem('+' if order_data.done else '-'))
            self.tw.setItem(index, 4, QTableWidgetItem(program_data.name))
            self.tw.setItem(index, 5, QTableWidgetItem(program_data.repo))
            self.tw.setItem(index, 6, QTableWidgetItem(program_data.tech_stack))
            self.tw.setItem(index, 7, QTableWidgetItem(group_name))
            overall_price += order_data.price
        self.summary_label.setText('Итого: ' + str(overall_price))

    @pyqtSlot()
    def on_back_btn_clicked(self):
        self.on_show_authwindow.emit()
        self.close()

    @pyqtSlot()
    def on_about_btn_clicked(self):
        self.about_window = AboutWindow(self.data)
        self.about_window.show()

    @pyqtSlot()
    def on_open_orders_btn_clicked(self):
        self.client_orders_window = ClientOrdersWindow(self.data.id)
        self.client_orders_window.show()

    @pyqtSlot()
    def on_close_btn_clicked(self):
        self.close()
