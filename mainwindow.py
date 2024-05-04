from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from adminwindow import AdminWindow
from client.client_window import ClientWindow
from repositories.account import account_repo_impl, AccountModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_startup_ui()

    def init_startup_ui(self):
        uic.loadUi('mainwindow.ui', self)

        self.auth_btn.clicked.connect(self.init_auth_ui)
        self.about_btn.clicked.connect(self.on_show_info_btn_clicked)
        self.close_btn.clicked.connect(self.on_close_btn_clicked)

    def init_auth_ui(self):
        uic.loadUi('authwindow.ui', self)

        self.back_btn.clicked.connect(self.init_startup_ui)
        self.signin_btn.clicked.connect(self.sign_in)

        self.admin_window = AdminWindow()
        self.admin_window.on_show_authwindow.connect(self.erase_fields_and_show_auth_menu)

    def on_show_info_btn_clicked(self):
        msg_box = QMessageBox(parent=self,
                              text='АИС IT Фирмы\nПрактическую работу выполнил студент ИУ5-45Б Расулов Арсен')
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle('Информация о разработчике')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def on_close_btn_clicked(self):
        self.close()

    def sign_in(self):
        login = self.le_login.text()
        password = self.le_password.text()

        user = account_repo_impl.get(login, password)
        if user is None:
            msg_box = QMessageBox(parent=self, text='Ошибка! Неверный логин или пароль')

            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle('Ошибка')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return

        if user.type == AccountModel.Type.ADMIN:
            self.admin_window.show()
            self.hide()
        elif user.type == AccountModel.Type.USER:
            self.client_window = ClientWindow(user.client_id)
            self.client_window.on_show_authwindow.connect(self.erase_fields_and_show_auth_menu)
            self.client_window.show()
            self.hide()


    def erase_fields_and_show_auth_menu(self):
        self.le_login.setText('')
        self.le_password.setText('')
        self.show()