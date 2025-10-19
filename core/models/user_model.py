
class UserModel:
    version = 1

    def __init__(self, username, bio, verify_key, addr):
        self.username = username
        self.bio = bio
        self.verify_key = verify_key
        self.addr = addr

    @classmethod
    def deserialize(cls, file_content):
        return cls(
            username=file_content.get('username'),
            bio=file_content.get('bio'),
            verify_key=file_content.get('verify_key'),
            addr=file_content.get('addr')
        )

    def serialize(self):
        return {
            "version": self.version,
            "username": self.username,
            "bio": self.bio,
            "verify_key": self.verify_key,
            "addr": self.addr
        }
