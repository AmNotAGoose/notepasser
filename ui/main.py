import sys

from PySide6.QtWidgets import QApplication

from core.node import Node
from ui.chat import ChatWindow


node = Node()

app = QApplication(sys.argv)

window = ChatWindow()
window.show()

app.exec()
