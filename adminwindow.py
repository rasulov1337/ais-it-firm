from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget
from admin_windows.client import ClientInfoWindow
from admin_windows.employee import EmployeeInfoWindow
from admin_windows.dev_group import DevGroupInfoWindow
from admin_windows.account import AccountInfoWindow
from admin_windows.order import OrderInfoWindow
from admin_windows.program import ProgramInfoWindow
from admin_windows.hardware import HardwareInfoWindow
from admin_windows.tech_stack import TechStackInfoWindow
from global_report_window import GlobalReportWindow


class AdminWindow(QWidget):
    on_show_authwindow = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('adminwindow.ui', self)

    @pyqtSlot()
    def on_back_btn_clicked(self):
        self.on_show_authwindow.emit()
        self.close()

    @pyqtSlot()
    def on_clients_btn_clicked(self):
        self.client_info_window = ClientInfoWindow()
        self.client_info_window.show()

    @pyqtSlot()
    def on_dev_groups_btn_clicked(self):
        self.dev_group_info_window = DevGroupInfoWindow()
        self.dev_group_info_window.show()

    @pyqtSlot()
    def on_employees_btn_clicked(self):
        self.employee_info_window = EmployeeInfoWindow()
        self.employee_info_window.show()

    @pyqtSlot()
    def on_orders_btn_clicked(self):
        self.order_info_window = OrderInfoWindow()
        self.order_info_window.show()

    @pyqtSlot()
    def on_programs_btn_clicked(self):
        self.program_info_window = ProgramInfoWindow()
        self.program_info_window.show()

    @pyqtSlot()
    def on_tech_eqs_btn_clicked(self):
        self.tech_eq_info_window = HardwareInfoWindow()
        self.tech_eq_info_window.show()

    @pyqtSlot()
    def on_tech_stacks_btn_clicked(self):
        self.tech_stack_info_window = TechStackInfoWindow()
        self.tech_stack_info_window.show()

    @pyqtSlot()
    def on_accounts_btn_clicked(self):
        self.account_info_window = AccountInfoWindow()
        self.account_info_window.show()

    @pyqtSlot()
    def on_reports_btn_clicked(self):
        self.global_report_window = GlobalReportWindow()
        self.global_report_window.show()
