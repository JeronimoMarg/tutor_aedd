from pymongo import MongoClient

from repository.environment import Environment
from model.user import User
from repository.user_repository import UserRepository

class MongoUserRepository(UserRepository):
    def __init__(self, env: Environment):
        super().__init__()
        self.client = MongoClient(env.MONGO_URI)
        self.db = self.client[env.MONGO_DB_NAME]
        self.collection = self.db["user"]
        self.collection.create_index("username", unique=True) # Username as id

    def save(self, user):
        self.collection.replace_one(
            {"username": user.username},
            user.to_dict(),
            upsert=True # Insert/Update
        )
        return user.username

    def find(self, username):
        doc = self.collection.find_one({"username": username})
        if doc:
            return User.from_dict(doc)
        return None