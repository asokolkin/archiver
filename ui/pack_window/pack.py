from PyQt6 import QtCore, QtGui, QtWidgets
import re
import ui.error_window.error_window as error_window
import ui.event_filter as event_filters
from archive_methods import compression
from ui.event_filter import TextEdit


class PackWindow:
    def __init__(self, filename_list, folders_list, number_of_files):
        self.window = QtWidgets.QDialog()
        self.window.setObjectName("PUW")
        self.window.setWindowTitle('Создать архив')
        self.window.setWindowIcon(QtGui.QIcon('icons/main.png'))

        self.filename_list = filename_list
        self.folders_list = folders_list
        self.number_of_files = number_of_files

        self.main_layout = QtWidgets.QVBoxLayout()

        self.directory_layout = QtWidgets.QHBoxLayout()

        self.directory_text_layout = QtWidgets.QHBoxLayout()

        self.dir_text = QtWidgets.QLabel()
        self.dir_text.setText('Создать архив в:')

        self.dir_input = TextEdit()
        self.dir_input.setFixedHeight(26)
        self.directory_text_layout.addWidget(self.dir_text)
        self.directory_text_layout.addWidget(self.dir_input)

        self.archive_name_layout = QtWidgets.QHBoxLayout()

        self.archive_name_text = QtWidgets.QLabel()
        self.archive_name_text.setText('Имя архива:')

        self.archive_name_input = TextEdit()
        self.archive_name_input.setFixedHeight(26)
        self.archive_name_layout.addWidget(self.archive_name_text)
        self.archive_name_layout.addWidget(self.archive_name_input)

        self.directory_button = QtWidgets.QPushButton()
        self.directory_button.setText('...')
        self.directory_button.clicked.connect(lambda: self.get_folder_and_display_it())

        self.directory_layout.addLayout(self.directory_text_layout)
        self.directory_layout.addWidget(self.directory_button)

        self.dialog_button_layout = QtWidgets.QHBoxLayout()

        self.ok_button = QtWidgets.QPushButton()
        self.ok_button.setText('Ок')
        self.ok_button.clicked.connect(self.start_compressing)

        self.no_button = QtWidgets.QPushButton()
        self.no_button.setText('Отменить')
        self.no_button.clicked.connect(self.window.close)

        self.dialog_button_layout.addWidget(self.ok_button)
        self.dialog_button_layout.addWidget(self.no_button)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setVisible(False)

        self.main_layout.addLayout(self.directory_layout)
        self.main_layout.addLayout(self.archive_name_layout)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addLayout(self.dialog_button_layout)

        self.window.setLayout(self.main_layout)

    def show(self):
        self.window.show()

    def exec(self):
        self.window.exec()

    def start_compressing(self):
        if self.check_validity():
            self.main_layout.itemAt(2).widget().setVisible(True)
            compression.compress_files_and_folders(str(self.dir_input.toPlainText()),
                                                   str(self.archive_name_input.toPlainText())+'.zip',
                                                   self.filename_list,
                                                   self.folders_list, self.number_of_files,
                                                   self.main_layout.itemAt(2).widget())
        else:
            error_message = error_window.ErrorMessage('Введите директорию')
            error_message.show()

    def check_validity(self):
        directory = str(self.dir_input.toPlainText())
        if re.search('[A-Z]:/', directory):
            return True
        else:
            return False

    def get_folder_and_display_it(self):
        file_path = QtWidgets.QFileDialog.getExistingDirectory(
            self.directory_button, 'Выберите папку')
        self.dir_input.setText(str(file_path))
