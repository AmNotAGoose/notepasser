import socket
import threading

from core.storage.credentials_manager import CredentialsManager
from core.globals import running
from core.networking.peer import Peer


class NetworkManager:
    def __init__(self, ip, port, credentials_manager: CredentialsManager):
        self.credentials_manager = credentials_manager
        self.peers = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(5)

        threading.Thread(target=self.listen_for_peers, daemon=True).start()

    def listen_for_peers(self):
        while running:
            conn, addr = self.sock.accept()
            self.peers[addr] = Peer(conn, addr, self.credentials_manager.get_signing_key())

    def connect_to_peer(self, addr):
        peer_ip, peer_port = addr
        if (peer_ip, peer_port) in self.peers:
            return
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((peer_ip, peer_port))

            self.peers[(peer_ip, peer_port)] = Peer(conn, (peer_ip, peer_port), self.credentials_manager.get_signing_key())
            print("connected")
        except Exception as e:
            print(e)

    def connect_to_discovered_peer(self, verify_key, addr):pass
