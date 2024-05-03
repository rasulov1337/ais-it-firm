from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QLineEdit, QFormLayout

import consts
from repositories.client import ClientModel


class AboutWindow(QWidget):
    on_show_authwindow = pyqtSignal()

    def __init__(self, client_info: ClientModel):
        super().__init__()
        uic.loadUi('client/client_about.ui', self)
        self.setStyleSheet(consts.STYLESHEET)

        self.le_name.setDisabled(True)
        self.le_telephone.setDisabled(True)
        self.le_address.setDisabled(True)
        self.le_email.setDisabled(True)
        self.rb_jur.setDisabled(True)
        self.rb_phys.setDisabled(True)

        self.le_name.setText(client_info.fullname)
        self.le_telephone.setText(client_info.telephone)
        self.le_address.setText(client_info.address)
        self.le_email.setText(client_info.email)
        if client_info.is_company:
            self.rb_jur.setChecked(True)
        else:
            self.rb_phys.setChecked(True)

    @pyqtSlot()
    def on_back_btn_clicked(self):
        self.on_show_authwindow.emit()
        self.close()
