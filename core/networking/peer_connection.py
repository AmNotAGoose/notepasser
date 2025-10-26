import json
import threading

from nacl.public import PublicKey, Box
from nacl.signing import VerifyKey

import core.globals
from core.networking.peer_crypto import PeerCrypto


class PeerConnection:
    def __init__(self, crypto: PeerCrypto, conn):
        self.crypto = crypto
        self.conn = conn

    def send(self, message: dict, encrypt=True):
        data = json.dumps(message).encode()
        if encrypt and self.crypto.box:
            data = self.crypto.box.encrypt(data)
        self.conn.sendall(data)

    def receive(self, decrypt=True, buffer=4096):
        data = self.conn.recv(buffer)
        if not data:
            return None
        if decrypt and self.crypto.box:
            data = self.crypto.box.decrypt(data)
        return json.loads(data.decode())

    def send_disconnect(self):
        if self.crypto.box:
            payload = {"type": "disconnect"}
            self.conn.sendall(self.crypto.box.encrypt(json.dumps(payload).encode()))

        core.globals.running = False