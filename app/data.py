from os import getenv
from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient
from bson import ObjectId  # Make sure to import ObjectId

class Database:
    """Database class for handling connections and operations with MongoDB."""

    load_dotenv()
    client = MongoClient(getenv("DB_URL"), tlsCAFile=where())
    db = client["Ticket1"]
    collection = db["Monsters"]

    def seed(self, amount):
        monsters = [Monster().to_dict() for _ in range(amount)]
        self.collection.insert_many(monsters)

    def reset(self):
        self.collection.delete_many({})

    def count(self) -> int:
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        documents = list(self.collection.find({}))
        # Convert ObjectId to string
        for document in documents:
            document['_id'] = str(document['_id'])
        return DataFrame(documents)

    def html_table(self) -> str:
        df = self.dataframe()
        return df.to_html() if not df.empty else None
