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
ip = socket.gethostbyname(socket.gethostname())
port = 32132

network_manager = NetworkManager(ip, port, credentials_manager)
discovery_manager = DiscoveryManager(ip, port, credentials_manager.get_signing_key().verify_key, user_manager, 3)

# start
discovery_manager.start_listening()
discovery_manager.start_broadcast()

while True:
    time.sleep(0.01)