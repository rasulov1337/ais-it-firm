from PyQt6.QtWidgets import QMessageBox


def create_msg_box(text):
    msg_box = QMessageBox()
    msg_box.setText(text)
    msg_box.setWindowTitle('Ошибка')
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.exec()