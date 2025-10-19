from core.storage.storage_manager import StorageManager
from core.models.user_model import UserModelV1


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
            self.contacts[contact.public_key] = UserModelV1.serialize(contact)

    def get_user(self, public_key):
        return self.contacts.get(public_key)
