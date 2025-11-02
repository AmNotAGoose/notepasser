import sys

from PySide6.QtWidgets import QApplication

from ui.chat import ChatWindow
from ui.utils import loadUiWidget


app = QApplication(sys.argv)

window = ChatWindow()
window.show()

app.exec()
