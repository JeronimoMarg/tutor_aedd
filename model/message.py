
class Message(object):
    def __init__(self, role, text):
        self.role = role
        self.text = text
    
    def to_dict(self):
        return {
            "role": self.role,
            "text": self.text
        }

    @staticmethod
    def from_dict(dict):
        return Message(dict["role"], dict["text"])