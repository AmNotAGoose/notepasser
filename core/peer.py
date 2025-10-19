import json
import threading
from json import JSONDecodeError

import nacl.utils
from nacl.exceptions import BadSignatureError
from nacl.public import PrivateKey, Box, PublicKey
from nacl.signing import SigningKey, VerifyKey

from core.network_manager import running


class Peer:
    def __init__(self, conn, addr, my_sign, my_verify):
        self.conn = conn
        self.addr = addr

        self.peer_information = None

        self.my_sign = my_sign
        self.my_verify = my_verify
        self.my_sk = PrivateKey.generate()
        self.my_pk = self.my_sk.public_key
        self.my_box = None

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
