from PyQt6 import QtCore, QtGui, QtWidgets

import file_managment_methods.delete
import ui.action_bar as action_bar
import os
import ui.event_filter as event_filter_elements
import ui.pack_window.pack as pack_window_container
import ui.unpack_window.unpack as unpack_window_container
import ui.error_window.error_window as error_window

MW = 0


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global MW
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowIcon(QtGui.QIcon('icons/main.png'))

        self.mw = MainWindow

        self.verticalLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 110, 771, 481))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.adjustSize()

        self.file_manager = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.file_manager.setContentsMargins(0, 0, 0, 0)
        self.file_manager.setObjectName("file_manager")

        self.path_field = QtWidgets.QHBoxLayout(self.verticalLayoutWidget)
        self.path_field.setContentsMargins(100, 0, 100, 0)

        self.button_bar = QtWidgets.QHBoxLayout()
        self.button_bar.setContentsMargins(100, 0, 100, 0)
        self.button_bar.setObjectName("button_bar")

        self.add_buttons_to_bar(self.button_bar)
        self.add_path_field_and_text(self.path_field)
        self.file_manager.addLayout(self.button_bar)
        self.file_manager.addLayout(self.path_field)
        self.add_file_manager(self.file_manager)
        self.add_on_click_listeners(self.button_bar)

        MainWindow.setCentralWidget(self.verticalLayoutWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MW = MainWindow

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Архиватор"))

    def add_file_manager(self, layout):
        file_manager = event_filter_elements.TreeView()
        model = QtGui.QFileSystemModel()
        model.setRootPath(QtCore.QDir().path())
        file_manager.setModel(model)
        file_manager.selectionModel().selectionChanged.connect(self.text_updater)
        layout.addWidget(file_manager)

    def add_buttons_to_bar(self, layout):
        action_bar.create_and_add_CreateButton(layout)
        action_bar.create_and_add_UnpackButton(layout)
        action_bar.create_and_add_DeleteFileButton(layout)

    def add_path_field_and_text(self, layout):
        pathtext = QtWidgets.QLabel()
        pathtext.setText('Путь')
        pathfield = QtWidgets.QTextEdit()
        pathfield.setFixedHeight(25)
        pathfield.setReadOnly(True)
        layout.addWidget(pathtext)
        layout.addWidget(pathfield)

    def update_path_in_pathfield(self, text):
        path_layout = self.path_field
        pathfield = path_layout.itemAt(1).widget()
        pathfield.setText(text)

    def text_updater(self):
        self.update_path_in_pathfield(self.get_file_path())

    def get_file_path(self):
        file_manager = self.file_manager.itemAt(2).widget()
        model = file_manager.model()
        if len(file_manager.selectedIndexes()) > 0:
            index = file_manager.selectedIndexes()[0]
            path = str(model.filePath(index))
            path = path.rpartition('/')
            path = path[0:len(path) - 1]
            path = ''.join(path)
            return path

    def get_filenames_list_and_number_of_files(self):
        file_manager = self.file_manager.itemAt(2).widget()
        filename_list = []
        if len(file_manager.selectedIndexes()) > 0:
            for i in range(len(file_manager.selectedIndexes())):
                index = file_manager.selectedIndexes()[i]
                if index.model().type(index) != 'File Folder':
                    filename_list.append(str(index.model().filePath(index)))
            filename_list = list(set(filename_list))
            return filename_list, len(filename_list)
        else:
            return [], 0

    def get_folders_list(self):
        file_manager = self.file_manager.itemAt(2).widget()
        folders_list = []
        if len(file_manager.selectedIndexes()) > 0:
            for i in range(len(file_manager.selectedIndexes())):
                index = file_manager.selectedIndexes()[i]
                if index.model().type(index) == 'File Folder':
                    folders_list.append(str(index.model().filePath(index)))
            return list(set(folders_list))

    def add_on_click_listeners(self, layout):
        create_button = layout.itemAt(0).widget()
        create_button.clicked.connect(lambda: self.check_validity(True))
        unpack_button = layout.itemAt(1).widget()
        unpack_button.clicked.connect(lambda: self.check_validity(False))
        delete_file_button = layout.itemAt(2).widget()
        delete_file_button.clicked.connect(
            lambda: file_managment_methods.delete.delete_file(self.get_filenames_list_and_number_of_files(),
                                                              self.get_folders_list()))

    def call_pack_window(self):
        subfolders, number_of_files_in_subfolders = find_subfolders_and_number_of_files(self.get_folders_list())
        filename_list, number_of_files = self.get_filenames_list_and_number_of_files()
        total_number = number_of_files + number_of_files_in_subfolders
        pack_window = pack_window_container.PackWindow(filename_list, subfolders, total_number)
        pack_window.exec()

    def call_unpack_window(self):
        filename_list, number_of_files = self.get_filenames_list_and_number_of_files()
        needed_archive = filename_list[0]
        unpack_window = unpack_window_container.UnPackWindow(needed_archive)
        unpack_window.show()

    def check_validity(self, flag):
        subfolders, number_of_files_in_subfolders = find_subfolders_and_number_of_files(self.get_folders_list())
        filename_list, number_of_files = self.get_filenames_list_and_number_of_files()
        filename_list = filename_list if len(filename_list) != 0 else ['aaaa']
        if number_of_files_in_subfolders or number_of_files != 0:
            if flag:
                self.call_pack_window()
            else:
                if number_of_files > 1 or filename_list[0][len(filename_list[0]) - 3:len(filename_list[0])] != 'zip':
                    error_window_t = error_window.ErrorMessage('Выберите zip архив')
                    error_window_t.show()
                else:
                    self.call_unpack_window()
        else:
            if flag:
                error_window_n = error_window.ErrorMessage('Выберите файлы для архивации')
                error_window_n.show()
            else:
                error_window_t = error_window.ErrorMessage('Выберите zip архив')
                error_window_t.show()


def init():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    set_app_icon(app)
    MainWindow = QtWidgets.QMainWindow()
    ui_a = Ui_MainWindow()
    ui_a.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())


def find_subfolders_and_number_of_files(folder_name_list):
    folder_name_list = folder_name_list if folder_name_list is not None else []
    all_subfolders = []
    number_of_files = 0
    for folder in folder_name_list:
        for kit in os.walk(folder, topdown=True):
            all_subfolders.append(kit)
            number_of_files += len(kit[2])
    return all_subfolders, number_of_files


def set_app_icon(app):
    app_icon = QtGui.QIcon()
    app_icon.addFile('icons/main.png', QtCore.QSize(16, 16))
    app_icon.addFile('icons/main.png', QtCore.QSize(24, 24))
    app_icon.addFile('icons/main.png', QtCore.QSize(32, 32))
    app_icon.addFile('icons/main.png', QtCore.QSize(48, 48))
    app_icon.addFile('icons/main.png', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
