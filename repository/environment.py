import os
from dotenv import load_dotenv

class Environment(object):
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("GROQ_API_KEY")
        self.MODEL = os.getenv("MODEL")
        self.CPP_VERSION = os.getenv("CPP_VERSION")
        self.MONGO_URI = os.getenv("MONGO_URI")
        self.MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")