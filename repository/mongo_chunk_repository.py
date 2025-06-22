from pymongo import MongoClient

from repository.environment import Environment
from model.chunk import Chunk
from repository.user_repository import UserRepository

class MongoChunkRepository():
    def __init__(self, env: Environment):
        super().__init__()
        self.client = MongoClient(env.MONGO_URI)
        self.db = self.client[env.MONGO_DB_NAME]
        self.collection = self.db["chunk"]

    def save(self, chunk):
        self.collection.insert_one(chunk.to_dict())
        return chunk.id

    def find(self, id):
        doc = self.collection.find_one({"_id": id})
        if doc:
            return Chunk.from_dict(doc)
        return None

    def get_id(self):
        doc = self.collection.find_one(sort=[("_id", -1)])
        
        if doc is None:
            return -1  
        return doc["_id"]