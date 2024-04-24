from os import getenv
from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient

class Database:
    """Database class for handling connections and operations with MongoDB."""

    load_dotenv()
    client = MongoClient(getenv("DB_URL"), tlsCAFile=where())
    db = client["Ticket1"]
    collection = db["Monsters"]

    def seed(self, amount):
        """Inserts the specified number of random monsters into the collection."""
        monsters = [Monster().to_dict() for _ in range(amount)]
        self.collection.insert_many(monsters)

    def reset(self):
        """Deletes all documents from the collection."""
        self.collection.delete_many({})

    def count(self) -> int:
        """Returns the number of documents in the collection."""
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        """Returns a DataFrame containing all documents in the collection."""
        documents = list(self.collection.find({}, {'_id': 0}))
        # Convert ObjectId to string
        return DataFrame(documents)

    def html_table(self) -> str:
        """Returns an HTML table of the DataFrame, or None if the collection is empty."""
        df = self.dataframe()
        return df.to_html() if not df.empty else None
