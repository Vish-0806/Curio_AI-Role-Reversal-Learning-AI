from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["curio_db"]

sessions = db["sessions"]
reports = db["reports"]

print("Connected:", client.list_database_names())