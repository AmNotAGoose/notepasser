import sys
import threading
import time

from PySide6.QtWidgets import QApplication

from core.node import Node
from ui.chat import ChatWindow


class GuiNode(Node):
    def __init__(self, get_trusted_token_input):
        super().__init__(get_trusted_token_input)

        self.app = QApplication(sys.argv)

        self.chat_window = ChatWindow(self)
        self.chat_window.show()
        self.chat_window.user_selected_signal.connect(self.chat_selected)

        self.app.exec()

    def chat_selected(self, user_verify_key):
        user_verify_key = bytes.fromhex(user_verify_key)
        peer = self.network_manager.connect_to_peer(user_verify_key)

        if not peer: return

        messages = []
        messages_lock = threading.Lock()

        def display_messages():
            nonlocal messages
            while True:
                while not peer.peer_events.messages.empty():
                    addr, payload = peer.peer_events.messages.get()
                    with messages_lock:
                        messages.append(payload['message'])
                time.sleep(0.1)

        msg_thread = threading.Thread(target=display_messages, daemon=True)
        msg_thread.start()

        self.chat_window.load_chat({
            "messages": messages
        })

GuiNode(input)
