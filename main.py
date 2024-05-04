import sys
from PyQt6.QtWidgets import QApplication


app = QApplication(sys.argv)
from mainwindow import MainWindow

window = MainWindow()
window.show()


app.exec()
