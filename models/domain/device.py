from dataclasses import dataclass

@dataclass
class Device:

    _id:str
    device_id:str
    #todo da criptare
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
            "_id":self.device_id,
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
    def from_dict(cls, data: dict) -> "Device":
        return cls(
            _id=data.get("device_id", ""),
            device_id=data.get("device_id", ""),
            ipv4=data.get("ipv4", ""),
            latitude=data.get("latitude", 0.0),
            longitude=data.get("longitude", 0.0),
            status=data.get("status", False),
            denomination=data.get("denomination", ""),  
            municipality=data.get("municipality", ""),
            province=data.get("province", ""),
            street=data.get("street", "")
        )