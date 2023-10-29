from fastapi import Header, Depends, HTTPException
import jwt
from pydantic import BaseModel
from typing import Dict
import os

_JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "DATA")
_ALGORITHM = "HS256"

class TokenData(BaseModel):
    person_id: str
    user: str
    role : str


def get_token_data(authorization: str = Header(None)):
    
    if authorization is None or len(authorization.split(" "))<1 or authorization.split(" ")[1] is None:
        raise HTTPException(status_code=401)
    
    try:
        payload = jwt.decode(authorization.split(" ")[1], _JWT_SECRET_KEY, algorithms=[_ALGORITHM])
        return TokenData(person_id=payload.get("person_id"), user = payload.get("user"), role = payload.get("role"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token inválidos")