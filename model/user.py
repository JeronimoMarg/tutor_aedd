from model.conversation import Conversation

class User(object):
    def __init__(self, username, conversations):
        self.username = username
        self.conversations = conversations

    def to_dict(self):
        return {
            "username": self.username,
            "conversations": [c.to_dict() for c in self.conversations]
        }

    @staticmethod
    def from_dict(dict):
        return User(dict["username"], [Conversation.from_dict(cd) for cd in dict["conversations"]])