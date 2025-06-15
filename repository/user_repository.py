from model.user import User

class UserRepository(object):
    def __init__(self):
        pass

    def save(self, user: User):
        """
        Guardar documento usuario con todas las conversaciones"""
        pass

    def find(username: str) -> User:
        pass
