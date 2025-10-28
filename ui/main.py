from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sys
import socket
import threading
import time
from core.networking.discovery_manager import DiscoveryManager
from core.networking.network_manager import NetworkManager
from core.storage.credentials_manager import CredentialsManager
from core.storage.storage_manager import StorageManager
from core.storage.user_manager import UserManager
from core.debug.debugging import log
from core.globals import running


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Sidebar"))
        self.list_widget = QListWidget()
        self.list_widget.addItems(["General Info", "Chat with Friend"])
        layout.addWidget(self.list_widget)
        self.setLayout(layout)


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message...")
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)

        layout.addWidget(QLabel("Chat Window"))
        layout.addWidget(self.chat_display)
        layout.addLayout(input_layout)
        self.setLayout(layout)

    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            self.chat_display.append(f"You: {message}")
            self.message_input.clear()
            self.chat_display.append(f"Friend: Echo -> {message}")


class MainInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Info"))
        layout.addWidget(QLabel("Welcome to notepasser!"))
        self.setLayout(layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("notepasser")
        self.setGeometry(100, 100, 900, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Top bar
        top_bar = QHBoxLayout()
        top_label = QLabel("Top Bar")
        top_button = QPushButton("Discover")
        top_bar.addWidget(top_label)
        top_bar.addStretch()
        top_bar.addWidget(top_button)
        main_layout.addLayout(top_bar)

        content_layout = QHBoxLayout()

        # Sidebar
        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar, 1)

        self.stack = QStackedWidget()
        self.info_widget = MainInfoWidget()
        self.chat_widget = ChatWidget()
        self.stack.addWidget(self.info_widget)
        self.stack.addWidget(self.chat_widget)
        content_layout.addWidget(self.stack, 2)

        main_layout.addLayout(content_layout)

        self.sidebar.list_widget.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.sidebar.list_widget.setCurrentRow(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())