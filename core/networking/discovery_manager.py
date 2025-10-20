import socket
import threading
import time

from core.globals import VERSION
from core.storage.credentials_manager import CredentialsManager


class DiscoveryManager:
    def __init__(self, ip, port, verify_key, user_manager, max_broadcast_number):
        self.ip = ip
        self.port = port
        self.verify_key = bytes(verify_key).hex()
        self.user_manager = user_manager
        self.max_broadcast_number = max_broadcast_number
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("0.0.0.0", self.port))

    def start_broadcast(self):
        def broadcast():
            print("discovery broadcast started")
            self.user_manager.discovered = []
            for i in range(0, self.max_broadcast_number):
                message = f"NOTEPASSER|{VERSION}|{self.verify_key}"
                print("sending discovery packet " + message)
                self.sock.sendto(message.encode("utf-8"), (self.ip, self.port))
                time.sleep(1.5)

        threading.Thread(target=broadcast, daemon=True).start()

    def start_listening(self):
        def listen():
             print("discovery listen started")
             while True:
                 try:
                     data, addr = self.sock.recvfrom(4096)
                     text = data.decode("utf-8", errors="replace").split("|")
                     if len(text) != 3:
                         print("discovered invalid user")
                         continue
                     prefix, version, peer_verify_key = text
                     if prefix != "NOTEPASSER" or version != VERSION or peer_verify_key == self.verify_key:
                         print("discovered self or different version or irrelevant packet")
                         continue
                     print("discovered user " + peer_verify_key + " with address " + str(addr))
                     self.user_manager.on_user_discovered(peer_verify_key, addr)
                     self.respond_to_discovery_request(addr)
                 except socket.timeout:
                     continue

        threading.Thread(target=listen, daemon=True).start()

    def respond_to_discovery_request(self, addr):
        self.sock.sendto(f"NOTEPASSER|{VERSION}|{self.verify_key}".encode("utf-8"), addr) # this should really have some kind of limiter
