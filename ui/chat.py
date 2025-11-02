from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QListView, QWidget, QVBoxLayout, QStackedLayout, \
    QStackedWidget

from ui.utils import loadUiWidget


class ChatWindow(QWidget):
    send_message_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.window = loadUiWidget("windows/chat_window")

        layout = QVBoxLayout(self)
        layout.addWidget(self.window)
        self.setLayout(layout)

        self.chat_stack = self.window.findChild(QStackedWidget, "chatStackedWidget")
        self.chat_stack.setCurrentIndex(1)

        self.send_button = self.window.findChild(QPushButton, "sendMessageButton")
        self.message_line_edit = self.window.findChild(QLineEdit, "messageLineEdit")
        self.message_list_view = self.window.findChild(QListView, "messageListView")

        self.send_button.clicked.connect(self._on_send_button_clicked)

    def _on_send_button_clicked(self):
        message = self.message_line_edit.text()
        if message:
            self.send_message_signal.emit(message)
            self.message_line_edit.clear()
