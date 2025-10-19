
class UserModel:
    version = 1

    def __init__(self, username, bio, verify_key):
        self.username = username
        self.bio = bio
        self.verify_key = verify_key

    @classmethod
    def deserialize(cls, file_content):
        cls.username = file_content.get('username')
        cls.bio = file_content.get('bio')
        cls.verify_key = file_content.get('verify_key')

    def serialize(self):
        return {
            "version": self.version,
            "username": self.username,
            "bio": self.bio,
            "verify_key": self.verify_key
        }
