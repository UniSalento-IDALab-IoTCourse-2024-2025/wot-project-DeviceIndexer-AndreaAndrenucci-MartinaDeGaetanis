from dataclasses import dataclass
from models.domain import Device

@dataclass
class DeviceDto:
    device_id:str
    ipv4:str
    latitude:float
    longitude:float
    status:bool
    denomination: str = ""
    municipality: str = ""
    province: str = ""
    street: str = ""
    
    def to_dict(self)->dict:
        return{
            "device_id":self.device_id,
            "ipv4":self.ipv4,
            "latitude":self.latitude,
            "longitude":self.longitude,
            "status":self.status,
            "denomination":self.denomination,
            "municipality":self.municipality,
            "province":self.province,
            "street":self.street
        }

    @classmethod
    def from_dict(cls, data: dict)->"DeviceDto":
        return{
            cls(
                device_id=data["device_id"],
                ipv4=data["ipv4"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                status=data["status"],
                denomination=data["denomination"],
                municipality=data["municipality"],
                province=data["province"],
                street=data["street"]
            )
        }
        
    @classmethod
    def from_domain(cls, device: "Device") -> "DeviceDto":
        return cls(
            device_id=device.device_id,
            ipv4=device.ipv4,
            latitude=device.latitude,
            longitude=device.longitude,
            status=device.status,
            denomination=device.denomination,
            municipality=device.municipality,
            province=device.province,
            street=device.street
        )

    def to_domain(self) -> "Device":
        return Device(
            device_id=self.device_id,
            ipv4=self.ipv4,
            latitude=self.latitude,
            longitude=self.longitude,
            status=self.status,
            denomination=self.denomination,
            municipality=self.municipality,
            province=self.province,
            street=self.street
        )