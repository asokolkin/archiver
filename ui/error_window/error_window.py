from PyQt6.QtWidgets import QMessageBox
from PyQt6 import QtGui


class ErrorMessage:
    def __init__(self, text):
        self.window = QMessageBox()
        self.window.setWindowTitle('Ошибка')
        self.window.setWindowIcon(QtGui.QIcon('icons/error.png'))
        self.window.setIcon(QMessageBox.Icon.Critical)
        self.window.setText(text)

    def show(self):
        self.window.exec()
