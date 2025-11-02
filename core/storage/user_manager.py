from core.storage.storage_manager import StorageManager
from core.models.user_model import UserModel


class UserManager:
    def __init__(self, storage_manager: StorageManager):
        self.storage_manager = storage_manager

        self.contacts = {}

        self.discovered = [] # updated by discovery manager

        self.reload_contacts()

        self.subscribers = {
            "peers_discovered": [],
        }

    def on(self, event_name, callback):
        if event_name not in self.subscribers:
            raise ValueError(f"Unknown event: {event_name}")
        self.subscribers[event_name].append(callback)

    def _emit(self, event_name, *args, **kwargs):
        for callback in self.subscribers.get(event_name, []):
            callback(*args, **kwargs)

    def set_discovered(self, discovered):
        self.discovered = discovered

    def reload_contacts(self):
        self.storage_manager.ensure_file_exists('contacts')
        self.contacts = {}
        file_content = self.storage_manager.read_file('contacts')
        for contact in file_content:
            self.contacts[contact.verify_key] = UserModel.serialize(contact)

    def get_user(self, verify_key):
        self.ensure_user_exists(verify_key)
        return self.contacts.get(verify_key)

    def ensure_user_exists(self, verify_key, addr=None):
        if verify_key in self.contacts.keys(): return
        self.contacts[verify_key] = UserModel(None, None, verify_key, addr)

    def on_user_discovered(self, verify_key, new_addr, disconnect):
        self.ensure_user_exists(verify_key, new_addr)
        user = self.contacts.get(verify_key)
        user.addr = new_addr
        self.contacts[verify_key] = user
        if not verify_key in self.discovered and not disconnect:
            self.discovered.append(verify_key)
        elif verify_key in self.discovered and disconnect:
            self.discovered.remove(verify_key)
        self._emit("peers_discovered", self.discovered)
