import socket
import threading
import time
from core.networking.discovery_manager import DiscoveryManager
from core.networking.network_manager import NetworkManager
from core.storage.credentials_manager import CredentialsManager
from core.storage.storage_manager import StorageManager
from core.storage.user_manager import UserManager
from core.debug.debugging import log
from core.globals import running


class PeerNode:
    def __init__(self, storage_location=None):
        if storage_location:
            self.storage = StorageManager(storage_location)
        else:
            self.storage = StorageManager()

        self.user_manager = UserManager(self.storage)
        self.credentials = CredentialsManager(self.storage)

        self.discovery_port = 33311
        self.ip = socket.gethostbyname(socket.gethostname())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, 0))
        self.port = self.sock.getsockname()[1]
        self.sock.close()

        print(f"[INIT] Local IP: {self.ip}:{self.port}")

        self.network = NetworkManager(self.ip, self.port, self.credentials, self.user_manager, input)
        self.discovery = DiscoveryManager(
            ip=self.ip,
            port=self.port,
            broadcast_port=self.discovery_port,
            verify_key=self.credentials.get_signing_key().verify_key,
            user_manager=self.user_manager,
            max_broadcast_number=3
        )

        self.message_received_listeners = []

        self.discovery.start_listening()
        self.discovery.start_broadcast()
        print("[DISCOVERY] Started listening and broadcasting...")

    def connect(self, peer_index):
        peers = self.user_manager.discovered
        if not peers or len(peers) < peer_index:
            print("[CONNECT] No peers discovered or not in range(?howisthatpossible)")
            return

        target = peers[peer_index]

        peer = self.network.connect_to_peer(target)
        if not peer:
            print("[CONNECT] Failed to connect.")
            return

        print(f"[CONNECTED] Messaging session started with {target}.")

        chat_active = True

        def display_messages():
            while running and chat_active:
                while not peer.peer_events.messages.empty():
                    addr, message = peer.peer_events.messages.get()
                    print(f"\n[{addr[0]}]: {message['message']}")
                    print("> ", end="", flush=True)
                time.sleep(0.1)

        msg_thread = threading.Thread(target=display_messages, daemon=True)
        msg_thread.start()

        while running:
            msg = input("> ")
            if msg == "|exit|":
                print("[CHAT] Ending session...")
                chat_active = False
                peer.disconnect()
                break
            elif msg.strip():
                peer.peer_connection.send_message(msg)

    def _on_receive_message(self):
        pass

    def _on_peer_discovered(self):
        return self.user_manager.discovered

    def discover(self):
        self.discovery.start_broadcast()
