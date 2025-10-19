import socket
import threading
import time

from core.globals import VERSION_NUMBER
from core.storage.credentials_manager import CredentialsManager


class DiscoveryManager:
    def __init__(self, ip, port, verify_key, user_manager, max_broadcast_number):
        self.ip = ip
        self.port = port
        self.verify_key = verify_key
        self.user_manager = user_manager
        self.max_broadcast_number = max_broadcast_number
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("0.0.0.0", self.port))

    def start_broadcast(self):
        def broadcast():
            i = 0
            for i in range(0, self.max_broadcast_number):
                message = f"NOTEPASSER|{VERSION_NUMBER}|{self.verify_key}"
                print("sending discovery packet " + message)
                self.sock.sendto(message.encode("utf-8"), (self.ip, self.port))
                time.sleep(1.5)
                i += 1

        threading.Thread(target=broadcast, daemon=True)

    def start_listening(self):
        def listen():
             while True:
                 try:
                     data, addr = self.sock.recvfrom(4096)
                     text = data.decode("utf-8", errors="replace").split("|")
                     if len(text) != 3:
                         continue
                     prefix, version, peer_verify_key = text
                     if prefix != "NOTEPASSER" or version != VERSION_NUMBER or peer_verify_key == self.verify_key:
                         continue

                     if CredentialsManager
                     self.user_manager.update_user_addr(peer_verify_key, addr)
                 except socket.timeout:
                     continue
                 except Exception as e:
                     print(e)

        threading.Thread(target=listen, daemon=True).start()
