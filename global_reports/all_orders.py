from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView

import consts
from repositories.client import client_repository_impl

from client.about import AboutWindow
from client.client_orders import ClientOrdersWindow
from repositories.order import OrderModel
from repositories.program import program_repo_impl, ProgramModel
from repositories.order import order_repo_impl, OrderOverallInfoModel
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QPieSeries


class AllOrdersWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('global_reports/base_report.ui', self)
        self.setStyleSheet(consts.STYLESHEET)

        self.label.setText('Заказы')

        self.tw.setColumnCount(5)
        self.tw.setHorizontalHeaderItem(0, QTableWidgetItem('Клиент'))
        self.tw.setHorizontalHeaderItem(1, QTableWidgetItem('Стоимость заказа'))
        self.tw.setHorizontalHeaderItem(2, QTableWidgetItem('Дедлайн'))
        self.tw.setHorizontalHeaderItem(3, QTableWidgetItem('Дата создания'))
        self.tw.setHorizontalHeaderItem(4, QTableWidgetItem('Выполнен?'))
        self.tw.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        table_data: list[OrderOverallInfoModel] = order_repo_impl.get_orders_overall_info()
        self.tw.setRowCount(len(table_data))
        overall_price = 0
        client_price_sum = {}
        for index, data in enumerate(table_data):
            self.tw.setItem(index, 0, QTableWidgetItem(data.fullname))
            self.tw.setItem(index, 1, QTableWidgetItem(str(data.price)))
            self.tw.setItem(index, 2, QTableWidgetItem(data.deadline.toString(consts.DATE_FORMAT)))
            self.tw.setItem(index, 3, QTableWidgetItem(data.creation_date.toString(consts.DATE_FORMAT)))
            self.tw.setItem(index, 4, QTableWidgetItem('+' if data.done else '-'))
            overall_price += data.price
            client_price_sum[data.fullname] = client_price_sum.get(data.fullname, 0) + data.price
        self.summary_label.setText('Стоимость всех заказов: ' + str(overall_price))

        # Chart
        series = QPieSeries()

        for key, value in client_price_sum.items():
            series.append(key, value)

        diagram = QChart()
        diagram.setTheme(QChart.ChartTheme.ChartThemeDark)
        diagram.addSeries(series)

        chart_view = QChartView(diagram)
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
