from model.message import Message

class Conversation(object):
    def __init__(self, id, memory):
        self.id = id
        self.memory = memory

    def to_dict(self):
        return {
            "id": self.id,
            "memory": [m.to_dict() for m in self.memory]
        }
    
    @staticmethod
    def from_dict(dict):
        return Conversation(dict["id"], [Message.from_dict(m) for m in dict["memory"]])