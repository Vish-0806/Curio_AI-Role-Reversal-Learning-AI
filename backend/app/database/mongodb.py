import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

import certifi
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

ROOT_ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
BACKEND_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"

# Load root .env first, then backend/.env so backend values can override when present.
load_dotenv(ROOT_ENV_PATH, override=False)
load_dotenv(BACKEND_ENV_PATH, override=True)


class InsertOneResult:
	def __init__(self, inserted_id: ObjectId):
		self.inserted_id = inserted_id


class InMemoryCollection:
	"""Small subset of Mongo collection APIs used by the app."""

	def __init__(self):
		self._store: Dict[str, Dict[str, Any]] = {}

	def insert_one(self, document: Dict[str, Any]) -> InsertOneResult:
		inserted_id = ObjectId()
		doc_copy = dict(document)
		doc_copy["_id"] = inserted_id
		self._store[str(inserted_id)] = doc_copy
		return InsertOneResult(inserted_id)

	def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> None:
		doc = self.find_one(query)
		if not doc:
			return

		doc_id = str(doc["_id"])
		if "$set" in update:
			doc.update(update["$set"])
		if "$push" in update:
			for key, value in update["$push"].items():
				existing = doc.get(key)
				if not isinstance(existing, list):
					existing = []
				existing.append(value)
				doc[key] = existing
		self._store[doc_id] = doc

	def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		if "_id" in query:
			key = str(query["_id"])
			doc = self._store.get(key)
			return dict(doc) if doc else None

		for doc in self._store.values():
			if all(doc.get(k) == v for k, v in query.items()):
				return dict(doc)
		return None

	def delete_one(self, query: Dict[str, Any]) -> None:
		if "_id" in query:
			self._store.pop(str(query["_id"]), None)
			return

		doc = self.find_one(query)
		if doc:
			self._store.pop(str(doc["_id"]), None)

	def count_documents(self, _query: Dict[str, Any]) -> int:
		return len(self._store)


def _create_mongo_collections() -> tuple[Any, Any, bool, Optional[str]]:
	mongo_uri = os.getenv("MONGO_URI")
	if not mongo_uri:
		return InMemoryCollection(), InMemoryCollection(), False, "MONGO_URI is not configured"

	mongo_db_name = os.getenv("MONGO_DB_NAME", "").strip() or "curio_db"
	allow_invalid_certs = os.getenv("MONGO_TLS_ALLOW_INVALID_CERTS", "false").lower() == "true"

	last_error: Optional[str] = None
	for _ in range(3):
		try:
			client = MongoClient(
				mongo_uri,
				tlsCAFile=certifi.where(),
				tlsAllowInvalidCertificates=allow_invalid_certs,
				serverSelectionTimeoutMS=15000,
				connectTimeoutMS=15000,
				socketTimeoutMS=15000,
				retryWrites=True,
			)
			client.admin.command("ping")

			db = client.get_default_database()
			if db is None:
				db = client[mongo_db_name]

			return db["sessions"], db["reports"], True, None
		except PyMongoError as exc:
			last_error = str(exc)
			time.sleep(1)

	return InMemoryCollection(), InMemoryCollection(), False, last_error


sessions, reports, mongo_connected, mongo_error = _create_mongo_collections()
