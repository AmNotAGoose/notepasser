from core.storage.storage_manager import StorageManager
from core.models.user_model import UserModel


class UserManager:
    def __init__(self, storage_manager: StorageManager):
        self.storage_manager = storage_manager
        self.contacts = None

        self.reload_contacts()

    def reload_contacts(self):
        self.storage_manager.ensure_file_exists('contacts')
        self.contacts = {}
        file_content = self.storage_manager.read_file('contacts')
        for contact in file_content:
            self.contacts[contact.verify_key] = UserModel.serialize(contact)

    def get_user(self, verify_key):
        return self.contacts.get(verify_key)

    def update_user_addr(self, verify_key, new_addr):
        user = self.contacts.get(verify_key)
        user.addr = new_addr
        self.contacts[verify_key] = user
