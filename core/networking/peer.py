import json
import queue
import threading
import time
from json import JSONDecodeError
from socket import socket, timeout

from nacl.exceptions import BadSignatureError
from nacl.public import PrivateKey, Box, PublicKey
from nacl.signing import SigningKey, VerifyKey

from core.globals import running
from core.networking.peer_connection import PeerConnection
from core.networking.peer_crypto import PeerCrypto
from core.networking.peer_events import PeerEvents
from core.networking.peer_state import PeerState
from core.storage.user_manager import UserManager
from core.debug.debugging import log


class Peer:
    def __init__(self, network_manager, user_manager: UserManager, conn, addr, my_sign: SigningKey, get_trusted_token):
        self.network_manager = network_manager
        self.user_manager = user_manager
        self.conn = conn
        self.addr = addr

        self.peer_state = PeerState(user_manager, my_sign.verify_key)
        self.peer_crypto = PeerCrypto(self.peer_state, get_trusted_token)
        self.peer_connection = PeerConnection(self.conn, self.peer_crypto)
        self.peer_events = PeerEvents(self.disconnect)

        self.start()

    def start(self):
        threading.Thread(target=self.listen_for_connection_information, daemon=True).start()

        self.conn.sendall(self._get_connection_string())

    def _get_connection_string(self):
        payload = {
            "type": "connection".encode().hex(),
            "encryption_key": bytes(self.peer_crypto.my_pk).hex(),
            "signature": self.peer_crypto.my_signing_key.sign(bytes(self.peer_crypto.my_pk)).signature.hex(),
            "verify_key": bytes(self.peer_crypto.my_verify_key).hex(),
            "trusted_token_exists": bool(self.peer_state.my_information.get("trusted_token"))
        }

        return json.dumps(payload).encode()

    def listen_for_connection_information(self):
        while running:
            try:
                data = json.loads(self.conn.recv(4096).decode("utf-8"))

                peer_encryption_key = bytes.fromhex(data["encryption_key"])
                peer_signature = bytes.fromhex(data["signature"])
                peer_verify_key = VerifyKey(bytes.fromhex(data["verify_key"]))
                peer_trusted_token_exists = bool(data["trusted_token_exists"])

                peer_verify_key.verify(peer_encryption_key, peer_signature)

                peer_pk = PublicKey(peer_encryption_key)
                self.peer_crypto.set_my_box(peer_pk)
                self.peer_state.update_peer(peer_verify_key, peer_pk, peer_trusted_token_exists)

                self.peer_state.connected = True

                self.peer_state.reload_user_information()
                self.peer_state.resolve_trusted_state()
            except:
                self.disconnect()

        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def listen_for_messages(self):
        while running:
            try:
                encrypted_message = self.conn.recv(4096)
                if not encrypted_message:
                    log(f"{self.addr} disconnected")
                    break

                event = self.peer_crypto.decrypt_json(encrypted_message)
                self.peer_events.on_event_received(event)
            except Exception as e:
                log(e)
                self.disconnect()

    def disconnect(self):
        self.peer_connection.send_disconnect()
        self.conn.close()
