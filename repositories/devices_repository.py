from typing import List
from models.domain import Device
from modules.singleton import singleton
from pymongo import MongoClient
from typing import Optional
import os

@singleton
class DeviceRepository:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
        self.collection = MongoClient(mongo_uri)["air_quality_db"]["registered_devices"]

    def find_all(self) -> List[Device]:
        results = self.collection.find()
        return [Device.from_dict(doc) for doc in results]

    def find_by_device_id(self, device_id: str) -> Optional[Device]:
        doc = self.collection.find_one({"device_id": device_id})
        return Device.from_dict(doc) if doc else None

    def delete_by_id(self, device_id):
        self.collection.delete_one({"device_id": device_id})

    def save(self, device: Device):
        self.collection.insert_one(device.to_dict())

    def saveWithOverwrite(self, device: Device):
        self.collection.replace_one({"_id": device.to_dict()["_id"]}, device.to_dict(), upsert=True)
