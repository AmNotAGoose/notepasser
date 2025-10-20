import socket
import threading

from core.storage.credentials_manager import CredentialsManager
from core.globals import running
from core.networking.peer import Peer
from core.storage.user_manager import UserManager


class NetworkManager:
    def __init__(self, ip, port, credentials_manager: CredentialsManager, user_manager: UserManager):
        self.credentials_manager = credentials_manager
        self.user_manager = user_manager
        self.peers = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(5)

        threading.Thread(target=self.listen_for_peers, daemon=True).start()

    def listen_for_peers(self):
        while running:
            conn, addr = self.sock.accept()
            print("accepted peer " + str(addr))
            self.peers[addr] = Peer(conn, addr, self.credentials_manager.get_signing_key())

    def connect_to_peer(self, verify_key):
        user = self.user_manager.get_user(verify_key)
        peer_ip, peer_port = user.addr
        if (peer_ip, peer_port) in self.peers: return
        print("trying to connect to " + str(user.addr))
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((peer_ip, peer_port))

            self.peers[verify_key] = Peer(conn, (peer_ip, peer_port), self.credentials_manager.get_signing_key())
            print("connected to " + str((peer_ip, peer_port)))
            return self.peers[verify_key]
        except Exception as e:
            print(e)
