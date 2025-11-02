from PySide6.QtCore import Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem, Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QListView, QWidget, QVBoxLayout, QStackedLayout, \
    QStackedWidget
from ui.utils import loadUiWidget


class ChatWindow(QWidget):
    send_message_signal = Signal(str)
    user_selected_signal = Signal(str)

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

        self.messages_list_view = self.window.findChild(QListView, "messagesListView")
        self.messages_list_model = QStandardItemModel()
        self.messages_list_view.setModel(self.messages_list_model)

        self.users_list_view = self.window.findChild(QListView, "usersListView")
        self.users_list_model = QStandardItemModel()
        self.users_list_view.setModel(self.users_list_model)

        self.send_button.clicked.connect(self._on_send_button_clicked)

    def load_users_list(self, users_info):
        if not users_info:
            self.users_list_model.clear()

        for user in users_info["users"]:
            self.users_list_model.appendRow(user)

    def load_chat(self, chat_info):
        if not chat_info:
            self.chat_stack.setCurrentIndex(1)
            return

        self.chat_stack.setCurrentIndex(0)
        for message in chat_info["messages"]:
            item = QStandardItem(message)
            self.messages_list_model.appendRow(item)

    def _on_user_selected(self):
        selected_indexes = self.users_list_view.selectedIndexes()[0]
        user = self.users_list_model.data(selected_indexes[0], Qt.DisplayRole) if selected_indexes else None
        self.user_selected_signal.emit(user)

    def _on_send_button_clicked(self):
        message = self.message_line_edit.text()
        if message:
            self.send_message_signal.emit(message)
            self.message_line_edit.clear()
