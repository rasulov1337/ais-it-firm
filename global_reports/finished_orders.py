from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView

import consts
from repositories.client import client_repository_impl

from client.about import AboutWindow
from client.client_orders import ClientOrdersWindow
from repositories.order import OrderModel
from repositories.program import program_repo_impl, ProgramModel
from repositories.order import order_repo_impl, FinishedOrderInfoModel
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QPieSeries, QBarSet, QBarSeries, QBarCategoryAxis


class FinishedOrdersWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('global_reports/base_report.ui', self)
        self.setStyleSheet(consts.STYLESHEET)

        self.label.setText('Выполненные заказы')

        self.tw.setColumnCount(5)
        self.tw.setHorizontalHeaderItem(0, QTableWidgetItem('ID Заказа'))
        self.tw.setHorizontalHeaderItem(1, QTableWidgetItem('Клиент'))
        self.tw.setHorizontalHeaderItem(2, QTableWidgetItem('Стоимость'))
        self.tw.setHorizontalHeaderItem(3, QTableWidgetItem('Дедлайн'))
        self.tw.setHorizontalHeaderItem(4, QTableWidgetItem('Дата создания'))
        self.tw.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tw.setAlternatingRowColors(True)

        table_data: list[FinishedOrderInfoModel] = order_repo_impl.get_finished_orders()
        self.tw.setRowCount(len(table_data))
        overall_price = 0

        client_spent_money = {

        }
        for index, data in enumerate(table_data):
            id_item = QTableWidgetItem(str(data.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.tw.setItem(index, 0, id_item)
            self.tw.setItem(index, 1, QTableWidgetItem(data.client_name))
            self.tw.setItem(index, 2, QTableWidgetItem(str(data.price)))
            self.tw.setItem(index, 3, QTableWidgetItem(data.deadline.toString(consts.DATE_FORMAT)))
            self.tw.setItem(index, 4, QTableWidgetItem(data.creation_date.toString(consts.DATE_FORMAT)))
            overall_price += data.price
            client_spent_money[data.client_name] = client_spent_money.get(data.client_name, 0) + data.price
            
        self.summary_label.setText('Стоимость всех завершенных заказов: ' + str(overall_price))
        
        bar_series = QBarSeries()
        for name, money in client_spent_money.items():
            bar_set = QBarSet(name)
            bar_set.append(money)
            bar_series.append(bar_set)


        chart = QChart()
        chart.addSeries(bar_series)
        chart.createDefaultAxes()

        chart_view = QChartView(chart)
        self.layout().addWidget(chart_view)
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
