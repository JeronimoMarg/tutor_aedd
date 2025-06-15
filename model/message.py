
class Message(object):
    def __init__(self, role, text, sec):
        self.role = role
        self.text = text
        self.sec = sec
    
    def to_dict(self):
        return {
            "role": self.role,
            "text": self.text,
            "sec": self.sec
        }

    @staticmethod
    def from_dict(dict):
        return Message(dict["role"], dict["text"], dict["sec"])

    def __str__(self):
        return self.role + ":\n" + self.text