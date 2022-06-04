from PyQt6 import QtCore, QtWidgets


class TextEdit(QtWidgets.QTextEdit):
    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
            return
        super().keyPressEvent(event)


class TreeView(QtWidgets.QTreeView):
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Control:
            self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Control:
            self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        super().keyReleaseEvent(event)
