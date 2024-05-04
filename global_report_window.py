from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget


from global_reports.all_hardware import AllHardwareWindow
from global_reports.all_orders import AllOrdersWindow
from global_reports.finished_orders import FinishedOrdersWindow
from global_reports.unfinished_orders import UnfinishedOrdersWindow
from global_reports.all_employees import AllEmployeesWindow


class GlobalReportWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('global_report_window.ui', self)

    @pyqtSlot()
    def on_back_btn_clicked(self):
        self.close()

    @pyqtSlot()
    def on_all_orders_btn_clicked(self):
        self.all_orders_window = AllOrdersWindow()
        self.all_orders_window.show()

    @pyqtSlot()
    def on_finished_orders_btn_clicked(self):
        self.finished_orders_window = FinishedOrdersWindow()
        self.finished_orders_window.show()

    @pyqtSlot()
    def on_unfinished_orders_btn_clicked(self):
        self.unfinished_orders_window = UnfinishedOrdersWindow()
        self.unfinished_orders_window.show()

    @pyqtSlot()
    def on_employees_btn_clicked(self):
        self.all_employees_window = AllEmployeesWindow()
        self.all_employees_window.show()

    @pyqtSlot()
    def on_hardware_btn_clicked(self):
        self.all_hardware_window = AllHardwareWindow()
        self.all_hardware_window.show()