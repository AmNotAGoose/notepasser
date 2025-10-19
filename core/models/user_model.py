
class UserModelV1:
    version = 1

    def __init__(self, username, public_key, private_key):
        self.username = username
        self.public_key = public_key
        self.private_key = private_key

    @classmethod
    def deserialize(cls, file_content):
        cls.username = file_content.get('username')
        cls.public_key = file_content.get('public_key')
        cls.private_key = file_content.get('private_key')

    def serialize(self):
        return {
            "version": self.version,
            "username": self.username,
            "public_key": self.public_key,
            "private_key": self.private_key
        }
