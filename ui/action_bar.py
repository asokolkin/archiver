from PyQt6 import QtWidgets


def create_and_add_CreateButton(layout):
    create_button = QtWidgets.QPushButton()
    create_button.setText('Создать архив')
    layout.addWidget(create_button)


def create_and_add_UnpackButton(layout):
    unpack_button = QtWidgets.QPushButton()
    unpack_button.setText('Распаковать архив')
    layout.addWidget(unpack_button)


def create_and_add_DeleteFileButton(layout):
    delete_button = QtWidgets.QPushButton()
    delete_button.setText('Удалить файл')
    layout.addWidget(delete_button)
