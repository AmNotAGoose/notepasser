import socket
import time

from core.networking.discovery_manager import DiscoveryManager
from core.networking.network_manager import NetworkManager
from core.storage.credentials_manager import CredentialsManager
from core.storage.storage_manager import StorageManager
from core.storage.user_manager import UserManager

# storage
storage_manager = StorageManager()
user_manager = UserManager(storage_manager)
credentials_manager = CredentialsManager(storage_manager)

# network
discovery_port = 33311
ip = socket.gethostbyname(socket.gethostname())
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip, 0))
port = sock.getsockname()[1]
sock.close()

print("port ", port)

network_manager = NetworkManager(ip, port, credentials_manager, user_manager)
discovery_manager = DiscoveryManager(ip, port, discovery_port, credentials_manager.get_signing_key().verify_key, user_manager, 3)

# start
discovery_manager.start_listening()
discovery_manager.start_broadcast()

while True:
    mode = input()

    match mode:
        case "connect":
            print("which index to connect to: " + str(user_manager.discovered))
            idx = input()
            network_manager.connect_to_peer(user_manager.discovered[int(idx)])
