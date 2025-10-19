import json
import queue
import threading
import time
from json import JSONDecodeError

from nacl.exceptions import BadSignatureError
from nacl.public import PrivateKey, Box, PublicKey
from nacl.signing import SigningKey, VerifyKey

from core.globals import running


class Peer:
    def __init__(self, conn, addr, my_sign: SigningKey):
        self.conn = conn
        self.addr = addr

        self.peer_information = None

        self.my_sign = my_sign
        self.my_verify = my_sign.verify_key
        self.my_sk = PrivateKey.generate()
        self.my_pk = self.my_sk.public_key
        self.my_box = None
        self.message_queue = queue.Queue()

        payload = {
            "encryption_key": bytes(self.my_pk).hex(),
            "signature": self.my_sign.sign(bytes(self.my_pk)).signature.hex(),
            "verify_key": bytes(self.my_verify).hex()
        }

        threading.Thread(target=self.listen_for_connection_information, daemon=True).start()

        conn.sendall(json.dumps(payload).encode())

    def listen_for_connection_information(self):
        while running and not self.peer_information:
            try:
                data = json.loads(self.conn.recv(4096).decode("utf-8"))

                peer_encryption_key = bytes.fromhex(data["encryption_key"])
                peer_signature = bytes.fromhex(data["signature"])
                peer_verify_key = VerifyKey(bytes.fromhex(data["verify_key"]))

                peer_verify_key.verify(peer_encryption_key, peer_signature)

                peer_pk = PublicKey(peer_encryption_key)
                self.my_box = Box(self.my_sk, peer_pk)

                self.peer_information = {
                    "verify_key": peer_verify_key,
                    "public_key": peer_pk,
                    "addr": self.addr
                }
            except BadSignatureError:
                print("you have opps")
            except (JSONDecodeError, KeyError):
                print("packet broken")

        if self.my_box:
            threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def listen_for_messages(self):
        while running:
            if not self.my_box:
                time.sleep(0.01)
                continue
            try:
                encrypted = self.conn.recv(4096)
                if not encrypted:
                    print(f"{self.addr} disconnected")
                    break
                message = self.my_box.decrypt(encrypted).decode()
                self.message_queue.put([self.addr, message])
                print(f"[{self.addr}] {message}")
            except Exception as e:
                print(e)

    def send_message(self, message):
        if not self.my_box:
            print("handshake not complete")
            return
        self.conn.sendall(self.my_box.encrypt(message.encode()))
        self.message_queue.put([self.addr, message])
