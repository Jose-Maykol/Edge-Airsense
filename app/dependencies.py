from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para verificar el token de Firebase
def verify_token(id_token: str):
    try:
        # Verifica el idToken con Firebase
        decoded_token = auth.verify_id_token(id_token)
        user_uid = decoded_token.get('uid')
        return user_uid
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid ID token")
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Expired ID token")
    except auth.RevokedIdTokenError:
        raise HTTPException(status_code=401, detail="Revoked ID token")
    except auth.AuthError as e:
        raise HTTPException(status_code=401, detail=f"Firebase auth error: {e}")

# Dependencia para inyectar el usuario verificado
async def get_current_user(id_token: str = Depends(oauth2_scheme)):
    user_uid = verify_token(id_token)
    return user_uid
