import sys

from PySide6.QtWidgets import QApplication

from ui.utils import loadUiWidget


app = QApplication(sys.argv)

window = loadUiWidget("main_window")

window.show()

app.exec()
