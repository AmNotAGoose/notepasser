import json
import socket
import threading

from core.peer import Peer
from core.user_manager import UserManager

running = True

class NetworkManager:
    def __init__(self, my_ip, my_port, on_receive):
        global running
        self.MY_IP = my_ip
        self.MY_PORT = my_port
        self.on_receive = on_receive
        self.peers = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.MY_IP, self.MY_PORT))
        self.sock.listen(10)

        peer_listener_thread = threading.Thread(target=self.listen_for_peers, daemon=True)
        peer_listener_thread.start()

        messages_listener_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        messages_listener_thread.start()

    def send(self, message: str, conn):
        conn.sendall(message.encode("uft-8"))

    def listen_for_peers(self):
        while running:
            conn, addr = self.sock.accept()
            self.peers[addr] = Peer(conn, addr)


    def listen_for_messages(self, conn):
        try:
            while running:
                data = json.dumps(conn.recv(4096).decode("utf-8"))
                self.on_receive(data)
        finally:
            conn.close()


