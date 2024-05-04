from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView

import consts
from client.about import AboutWindow
from repositories.employee import employee_repo_impl, EmployeeModel
from repositories.dev_group import dev_group_repo_impl


class AllEmployeesWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('global_reports/base_report.ui', self)
        self.setStyleSheet(consts.STYLESHEET)

        self.label.setText('Все сотрудники фирмы')

        self.tw.setColumnCount(5)
        self.tw.setHorizontalHeaderItem(0, QTableWidgetItem('ФИО'))
        self.tw.setHorizontalHeaderItem(1, QTableWidgetItem('Дата рождения'))
        self.tw.setHorizontalHeaderItem(2, QTableWidgetItem('Заработная плата'))
        self.tw.setHorizontalHeaderItem(3, QTableWidgetItem('Группа разработки'))
        self.tw.setHorizontalHeaderItem(4, QTableWidgetItem('Дата найма'))
        self.tw.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        table_data: list[EmployeeModel] = employee_repo_impl.get_all()
        self.tw.setRowCount(len(table_data))
        for index, data in enumerate(table_data):
            id_item = QTableWidgetItem(str(data.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.tw.setItem(index, 0, id_item)
            self.tw.setItem(index, 1, QTableWidgetItem(data.birth_date.toString(consts.DATE_FORMAT)))
            self.tw.setItem(index, 2, QTableWidgetItem(str(data.salary)))
            self.tw.setItem(index, 3, QTableWidgetItem(dev_group_repo_impl.get_name(data.dev_group_id)))
            self.tw.setItem(index, 4, QTableWidgetItem(data.hire_date.toString(consts.DATE_FORMAT)))
        self.summary_label.setText('Всего сотрудников: ' + str(len(table_data)))

        self.setMinimumSize(1000, 800)


    @pyqtSlot()
    def on_back_btn_clicked(self):
        self.on_show_authwindow.emit()
        self.close()

    @pyqtSlot()
    def on_close_btn_clicked(self):
        self.close()
