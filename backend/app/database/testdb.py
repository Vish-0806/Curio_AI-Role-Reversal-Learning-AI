from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI"),
    tlsCAFile=certifi.where()
)

db = client["curio_db"]

print("Connected to MongoDB")

db.sessions.insert_one({
    "user_id": "user123",
    "topic": "Binary Search",
    "messages": [
        {"role": "user", "text": "Binary search divides array"},
        {"role": "ai", "text": "Why must it be sorted?"}
    ],
    "score": 7,
    "timestamp": datetime.utcnow()
})


db.reports.insert_one({
    "user_id": "user123",
    "topic": "Binary Search",
    "strengths": ["Understands basic idea"],
    "weaknesses": ["Time complexity confusion"],
    "missing_concepts": ["Sorted requirement"],
    "score": 7
})


print("Inserted successfully")