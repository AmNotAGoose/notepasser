import socket
import threading
import time

from core.globals import VERSION
from core.storage.credentials_manager import CredentialsManager


class DiscoveryManager:
    def __init__(self, ip, port, discovery_port, verify_key, user_manager, max_broadcast_number):
        self.ip = ip
        self.port = port
        self.discovery_port = discovery_port
        self.verify_key = bytes(verify_key).hex()
        self.user_manager = user_manager
        self.max_broadcast_number = max_broadcast_number
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.discovery_port))

    def get_broadcast_string(self):
        return f"NOTEPASSER|{VERSION}|{self.verify_key}|{self.ip}|{self.port}"

    def start_broadcast(self):
        def broadcast():
            print("discovery broadcast started")
            self.user_manager.discovered = []
            for i in range(0, self.max_broadcast_number):
                message = self.get_broadcast_string()
                print("sending discovery packet " + message)
                self.sock.sendto(message.encode("utf-8"), ("255.255.255.255", self.discovery_port))
                time.sleep(1.5)

        threading.Thread(target=broadcast, daemon=True).start()

    def start_listening(self):
        def listen():
             print("discovery listen started")
             while True:
                 try:
                     data, addr = self.sock.recvfrom(4096)
                     text = data.decode("utf-8", errors="replace").split("|")
                     if len(text) != 5:
                         print("discovered invalid user")
                         continue
                     prefix, version, peer_verify_key, ip, port = text
                     peer_addr = (ip, int(port))
                     if prefix != "NOTEPASSER" or version != VERSION:
                         print("different version or irrelevant packet")
                         continue
                     if peer_verify_key == self.verify_key:
                         print("discovered self")
                         continue
                     print("discovered user " + peer_verify_key + " with address " + str(peer_addr))
                     self.user_manager.on_user_discovered(peer_verify_key, peer_addr)
                     self.respond_to_discovery_request(peer_addr)
                 except socket.timeout:
                     continue
                 except ConnectionResetError:
                     print("windows badness")
                     continue

        threading.Thread(target=listen, daemon=True).start()

    def respond_to_discovery_request(self, peer_addr):
        print("sending targeted discovery packet to " + str(peer_addr))
        self.sock.sendto(self.get_broadcast_string().encode("utf-8"), peer_addr) # this should really have some kind of limiter
