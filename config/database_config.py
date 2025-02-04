from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    def __init__(self, env_name: str = "mongodb"):
        env_path = f"env/.env.{env_name}"
        load_dotenv(env_path)

        self.MONGO_DB_URI = os.getenv("MONGO_DB_URI")
        self.FILE_PATH = os.getenv("FILE_PATH")
        self.DATABASE_NAME = os.getenv("DATABASE_NAME")
        self.COLLECTION_NAME = os.getenv("COLLECTION_NAME")
