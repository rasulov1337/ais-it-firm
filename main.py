import sys
from PyQt6.QtWidgets import QApplication

from mainwindow import MainWindow

app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

from adminwindow import AdminWindow

w = AdminWindow()
w.show()

app.exec()
