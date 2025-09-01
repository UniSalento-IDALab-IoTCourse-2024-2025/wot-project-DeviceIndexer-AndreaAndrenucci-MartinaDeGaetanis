from dataclasses import dataclass
from typing import Optional, List
from models.dto import DeviceDto

@dataclass
class DeviceResponseDto:
    response:int
    message:str
    payload:Optional[List[DeviceDto]] = None

    def to_dict(self):
        return {
            "response": self.response,
            "message": self.message,
            "payload": [d.to_dict() for d in self.payload] if self.payload else []
        }
