from core.networking.discovery_manager import DiscoveryManager
from core.networking.network_manager import NetworkManager
from core.storage.credentials_manager import CredentialsManager
from core.storage.storage_manager import StorageManager
from core.storage.user_manager import UserManager


class Node:
    def __init__(self):
        self.storage_manager = StorageManager()
        self.user_manager = UserManager(self.storage_manager)
        self.credentials_manager = CredentialsManager(self.storage_manager)

        self.discovery_manager = DiscoveryManager(self.credentials_manager, self.user_manager, 3)
        self.network_manager = NetworkManager()
