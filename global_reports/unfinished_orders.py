from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView

import consts
from repositories.client import client_repository_impl

from client.about import AboutWindow
from client.client_orders import ClientOrdersWindow
from repositories.order import OrderModel
from repositories.program import program_repo_impl, ProgramModel
from repositories.order import order_repo_impl, UnfinishedOrderInfoModel
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QPieSeries


class UnfinishedOrdersWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('global_reports/base_report.ui', self)
        self.setStyleSheet(consts.STYLESHEET)

        self.label.setText('Выполненные заказы')

        self.tw.setColumnCount(9)
        self.tw.setHorizontalHeaderItem(0, QTableWidgetItem('ID Заказа'))
        self.tw.setHorizontalHeaderItem(1, QTableWidgetItem('Стоимость'))
        self.tw.setHorizontalHeaderItem(2, QTableWidgetItem('Дедлайн'))
        self.tw.setHorizontalHeaderItem(3, QTableWidgetItem('Клиент'))
        self.tw.setHorizontalHeaderItem(4, QTableWidgetItem('Дата создания'))
        self.tw.setHorizontalHeaderItem(5, QTableWidgetItem('Ссылка на репозиторий'))
        self.tw.setHorizontalHeaderItem(6, QTableWidgetItem('Название программы'))
        self.tw.setHorizontalHeaderItem(7, QTableWidgetItem('Технологический стек'))
        self.tw.setHorizontalHeaderItem(8, QTableWidgetItem('Группа разработки'))
        self.tw.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.summary_label.hide()

        table_data: list[UnfinishedOrderInfoModel] = order_repo_impl.get_unfinished_orders()
        self.tw.setRowCount(len(table_data))
        for index, data in enumerate(table_data):
            id_item = QTableWidgetItem(str(data.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.tw.setItem(index, 0, id_item)
            self.tw.setItem(index, 1, QTableWidgetItem(str(data.price)))
            self.tw.setItem(index, 2, QTableWidgetItem(data.deadline.toString(consts.DATE_FORMAT)))
            self.tw.setItem(index, 3, QTableWidgetItem(data.client_name))
            self.tw.setItem(index, 4, QTableWidgetItem(data.creation_date.toString(consts.DATE_FORMAT)))
            self.tw.setItem(index, 5, QTableWidgetItem(data.repo))
            self.tw.setItem(index, 6, QTableWidgetItem(data.program_name))
            self.tw.setItem(index, 7, QTableWidgetItem(data.stack))
            self.tw.setItem(index, 8, QTableWidgetItem(data.dev_group_name))
        self.setMinimumSize(1000, 800)

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
