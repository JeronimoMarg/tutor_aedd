from model.conversation import Conversation
from model.user import User
from model.message import Message
from repository.user_repository import UserRepository

class MemoryService(object):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def find_user(self, username: str) -> User:
        return self.user_repository.find(username)

    def save_user(self, user: User) -> str:
        return self.user_repository.save(user)

    def create_conversation(self, user: User) -> Conversation:
        ids = [conv.id for conv in user.conversations]
        ids.sort()
        if ids and len(ids) > 0:
            new_id = ids[-1] + 1
        else:
            new_id = 1
        conv = Conversation(new_id, [])
        user.conversations.append(conv)
        return conv

    def add_message(self, conv: Conversation, message: Message) -> int:
        secs = [m.sec for m in conv.memory]
        secs.sort()
        if secs and len(secs) > 0:
            new_sec = secs[-1] + 1
        else:
            new_sec = 1
        message.sec = new_sec
        conv.memory.append(message)

        return new_sec