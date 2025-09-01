from typing import List
from models.domain import AirQualityMeasurement
from modules.singleton import singleton
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timezone, timedelta
import os

@singleton
class PollutionMeasurementsRepository:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
        self.collection = MongoClient(mongo_uri)["air_quality_db"]["measurements"]

        # TTL index: scadenza basata su "expireAt"
        self.collection.create_index(
            [("expireAt", ASCENDING)],
            expireAfterSeconds=0
        )

    def find_all_measurements(self) -> List[AirQualityMeasurement]:
        results = self.collection.find()
        return [AirQualityMeasurement.from_dict(doc) for doc in results]

    def save(self, measurement: AirQualityMeasurement):
        doc = measurement.to_dict()
        doc["expireAt"] = datetime.now(timezone.utc) + timedelta(minutes=50)
        self.collection.insert_one(doc)
    
    def save_all(self, measurements: List[AirQualityMeasurement]):
        dicts = [m.to_dict() for m in measurements]
        expire_at = datetime.now(timezone.utc) + timedelta(minutes=50)
        for d in dicts:
            d["expireAt"] = expire_at
        self.collection.insert_many(dicts)

    def find_latest_measurement(self) -> AirQualityMeasurement | None:
        doc = self.collection.find_one(
            sort=[("misuration_date", -1)]
        )
        return AirQualityMeasurement.from_dict(doc) if doc else None

    def find_by_exact_date(self, date: str) -> List[AirQualityMeasurement]:
        results = self.collection.find({
            "misuration_date": datetime.fromisoformat(date).replace(tzinfo=timezone.utc) if isinstance(date, str) else date
        })
        return [AirQualityMeasurement.from_dict(doc) for doc in results]

    def find_between_dates(self, start_date: str, end_date: str) -> List[AirQualityMeasurement]:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        results = self.collection.find({
            "misuration_date": {
                "$gte": start,
                "$lte": end
            }
        }).sort("misuration_date", ASCENDING)
        return [AirQualityMeasurement.from_dict(doc) for doc in results]
