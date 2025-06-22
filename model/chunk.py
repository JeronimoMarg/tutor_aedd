import numpy as np

class Chunk(object):
    def __init__(self, id: np.int64, text: str):
        self.id = id
        self.text = text

    def to_dict(self):
        return {
            "_id": self.id,
            "text": self.text
        }
    
    @staticmethod
    def from_dict(dict):
        return Chunk(dict["_id"], dict["text"])