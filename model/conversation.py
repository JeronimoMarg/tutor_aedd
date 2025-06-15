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

    def __str__(self):
        if len(self.memory) > 0:
            self.memory.sort(key=lambda x: x.sec) # Sort messages by sec number
            return "\n".join([m.__str__() for m in self.memory])
        return ""