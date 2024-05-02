from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget

import consts
from repositories.client import client_repository_impl

from client.about import AboutWindow
from client.client_orders import ClientOrdersWindow


class ClientWindow(QWidget):
    on_show_authwindow = pyqtSignal()

    def __init__(self, id):
        super().__init__()
        self.data = client_repository_impl.get(id)
        uic.loadUi('client/client_main.ui', self)
        self.setStyleSheet(consts.stylesheet)

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
