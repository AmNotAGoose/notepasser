from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QListView

from ui.utils import loadUiWidget


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = loadUiWidget("main_window")
        self.setCentralWidget(self.window)

        self.message_sent = 

        self.send_button = self.window.findChild(QPushButton, "sendMessageButton")
        self.message_line_edit = self.window.findChild(QLineEdit, "messageLineEdit")
        self.message_list_view = self.window.findChild(QListView, "messageListView")

