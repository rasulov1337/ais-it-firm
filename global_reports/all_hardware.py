from PyQt6 import uic
from PyQt6.QtCore import  pyqtSlot, Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView

import consts

from repositories.hardware import hardware_repo_impl, HardwareModel


class AllHardwareWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('global_reports/base_report.ui', self)
        self.setStyleSheet(consts.STYLESHEET)

        self.label.setText('Техническое оборудование фирмы')

        self.tw.setColumnCount(5)
        self.tw.setHorizontalHeaderItem(0, QTableWidgetItem('ID оборудования'))
        self.tw.setHorizontalHeaderItem(1, QTableWidgetItem('Скорость интернета'))
        self.tw.setHorizontalHeaderItem(2, QTableWidgetItem('Модель видеокарты'))
        self.tw.setHorizontalHeaderItem(3, QTableWidgetItem('Процессор'))
        self.tw.setHorizontalHeaderItem(4, QTableWidgetItem('ОЗУ'))
        self.tw.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.summary_label.hide()

        table_data: list[HardwareModel] = hardware_repo_impl.get_all()
        self.tw.setRowCount(len(table_data))
        for index, data in enumerate(table_data):
            id_item = QTableWidgetItem(str(data.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.tw.setItem(index, 0, id_item)
            self.tw.setItem(index, 1, QTableWidgetItem(str(data.internet_speed)))
            self.tw.setItem(index, 2, QTableWidgetItem(data.gpu))
            self.tw.setItem(index, 3, QTableWidgetItem(data.cpu))
            self.tw.setItem(index, 4, QTableWidgetItem(str(data.ram)))
        self.setMinimumSize(1000, 800)


    @pyqtSlot()
    def on_close_btn_clicked(self):
        self.close()
