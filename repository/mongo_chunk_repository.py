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

    def save(self, chunk: Chunk):
        self.collection.insert_one(chunk.to_dict())
        return chunk.id

    def save(self, chunk_list: list[Chunk]):
        self.collection.insert_many([c.to_dict() for c in chunk_list])
        return [c.id for c in chunk_list]

    def find(self, ids):
        chunks = []
        for doc in self.collection.find({"_id": {"$in": ids}}):
            chunks.append(Chunk.from_dict(doc))
        return chunks

    def findAll(self):
        chunks = []
        for doc in self.collection.find():
            chunks.append(Chunk.from_dict(doc))
        return chunks

    def get_id(self):
        doc = self.collection.find_one(sort=[("_id", -1)])
        
        if doc is None:
            return -1  
        return doc["_id"]