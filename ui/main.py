import sys

from PySide6.QtWidgets import QApplication

from core.node import Node
from ui.chat import ChatWindow


class GuiNode(Node):
    def __init__(self, get_trusted_token_input):
        super().__init__(get_trusted_token_input)

        self.app = QApplication(sys.argv)

        self.chat_window = ChatWindow()
        self.chat_window.show()

        self.app.exec()


GuiNode(input)