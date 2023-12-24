from fastapi import APIRouter, Depends, HTTPException
from ..schemas.schemas import DeviceRequest
from ..firestore_config import db
from ..dependencies import get_current_user
import uuid0

router = APIRouter()

@router.post("/add-device")
async def add_device(request: DeviceRequest, user_uid: str = Depends(get_current_user)):
    devices_ref = db.collection('devices')
    query = devices_ref.where('mac', '==', request.mac).get()

    if query:
        # Verificar si el dispositivo pertenece a otro usuario
        for doc in query:
            if doc.to_dict().get('userID') != user_uid:
                raise HTTPException(status_code=400, detail="Dispositivo ya registrado por otro usuario.")
        
        # Si el dispositivo ya está registrado por el mismo usuario
        return {"message": "Dispositivo ya registrado por este usuario."}

    # Si el dispositivo no está registrado, proceder a agregarlo
    device_id = str(uuid0.generate().base62) 
    new_device_data = {
        "userID": user_uid,
        "deviceID": device_id,
        "mac": request.mac,
        "certRef": '/etc/mosquitto/certs/',
        "type": request.deviceType
    }
    devices_ref.document(device_id).set(new_device_data)
    return {"message": "Dispositivo agregado con éxito."}