from pydantic import BaseModel

# Modelo para la solicitud
class DeviceRequest(BaseModel):
    mac: str
    deviceType: str

class DeviceQuery(BaseModel):
    deviceID: str
    certRef: str