from dataclasses import dataclass
from typing import Optional, List
from models.dto import AirQualityMeasurementDTO


@dataclass
class MeasurementsMessageDTO:
    measurements: Optional[AirQualityMeasurementDTO] = None
    
    def to_dict(self)->dict:
        return{
            "measurements": self.measurements if self.measurements else None
        }
        
    @staticmethod
    def from_dict(data: dict) -> "MeasurementsMessageDTO":
        measurements_data = data.get("measurements", [])
        measurements = [
            AirQualityMeasurementDTO(m) for m in measurements_data
        ] if isinstance(measurements_data, list) else []

        return MeasurementsMessageDTO(measurements=measurements)

    @staticmethod
    def from_measurements(measurements: List) -> "MeasurementsMessageDTO":
        """
        Costruisce un DTO a partire da una lista di oggetti AirQualityMeasurement.
        """
        dto_measurements = [
            AirQualityMeasurementDTO.from_domain(m) for m in measurements
        ]
        return MeasurementsMessageDTO(measurements=dto_measurements)

