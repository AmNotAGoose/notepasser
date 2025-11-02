from core.networking.discovery_manager import DiscoveryManager
from core.networking.network_manager import NetworkManager
from core.storage.storage_manager import StorageManager
from core.storage.user_manager import UserManager


class Node:
    def __init__(self):
        self.storage_manager = StorageManager()
        self.user_manager = UserManager(self.storage_manager)

        self.discovery_manager = DiscoveryManager()
        self.network_manager = NetworkManager()