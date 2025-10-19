import time

from core.storage.credentials_manager import CredentialsManager
from core.networking.network_manager import NetworkManager
from core.storage.storage_manager import StorageManager


def test_send_and_receive():
    nm1 = NetworkManager("127.0.0.1", 32313, CredentialsManager(StorageManager()))
    nm2 = NetworkManager("127.0.0.1", 32314, CredentialsManager(StorageManager()))

    nm2.connect_to_peer("127.0.0.1", 32313)
    peer = nm2.peers[("127.0.0.1", 32313)]
    while not peer.my_box:
        time.sleep(0.1)

    peer.send_message("hello")
