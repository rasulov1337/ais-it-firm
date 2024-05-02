from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QLineEdit, QFormLayout

import consts


class AboutWindow(QWidget):
    on_show_authwindow = pyqtSignal()

    def __init__(self, client_info):
        super().__init__()
        self.setStyleSheet(consts.stylesheet)


        le_name = QLineEdit(client_info.fullname)
        le_telephone = QLineEdit(client_info.telephone)
        le_address = QLineEdit(client_info.address)
        le_email = QLineEdit(client_info.email)

        le_name.setDisabled(True)
        le_telephone.setDisabled(True)
        le_address.setDisabled(True)
        le_email.setDisabled(True)

        layout = QFormLayout()
        layout.addRow('ФИО/Название', le_name)
        layout.addRow('Телефон', le_telephone)
        layout.addRow('Адрес', le_address)
        layout.addRow('Почта', le_email)

        self.setLayout(layout)

    @pyqtSlot()
    def on_back_btn_clicked(self):
        self.on_show_authwindow.emit()
        self.close()
