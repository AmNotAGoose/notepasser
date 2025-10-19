import json
import socket
import threading
import time

from core.credentials_manager import CredentialsManager
from core.globals import running
from core.peer import Peer
from core.storage_manager import StorageManager
from core.user_manager import UserManager


class NetworkManager:
    def __init__(self, my_ip, my_port, credentials_manager: CredentialsManager):
        self.MY_IP = my_ip
        self.MY_PORT = my_port
        self.credentials_manager = credentials_manager
        self.peers = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.MY_IP, self.MY_PORT))
        self.sock.listen(5)

        threading.Thread(target=self.listen_for_peers, daemon=True).start()

    def listen_for_peers(self):
        while running:
            conn, addr = self.sock.accept()
            self.peers[addr] = Peer(conn, addr, self.credentials_manager.get_signing_key())

    def connect_to_peer(self, peer_ip, peer_port):
        if (peer_ip, peer_port) in self.peers:
            return

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((peer_ip, peer_port))

            self.peers[(peer_ip, peer_port)] = Peer(conn, (peer_ip, peer_port), self.credentials_manager.get_signing_key())
            print("connected")
        except Exception as e:
            print(e)
