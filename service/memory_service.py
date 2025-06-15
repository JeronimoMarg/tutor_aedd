
from repository.user_repository import UserRepository

class MemoryService(object):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def find_user(self, username):
        return self.user_repository.find(username)

    def save_user(self, user):
        return self.user_repository.save(user)