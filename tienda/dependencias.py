from fastapi import HTTPException, Header, Depends
import jwt
from sqlalchemy.orm import Session
from tienda.modelos_mapeados import engine, Usuario
from tienda.seguridad import leer_token

def obtener_sesion():
    with Session(engine) as session:
        yield session

def obtener_usuario(authorization: str | None = Header(None), session = Depends(obtener_sesion)):
    if not authorization:
        raise HTTPException(
            status_code=401, 
            detail="Falta la cabecera de autorización", 
            headers={"WWW-Authenticate": "Bearer"}
        )

    partes = authorization.split(" ")

    if len(partes) != 2 or partes[0].lower() != "bearer":
        raise HTTPException(
            status_code=401, 
            detail="Formato de token inválido. Use 'Bearer <token>'", 
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = partes[1]

    try:
        id_usuario = leer_token(token)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, 
            detail="El token ha expirado", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, 
            detail="El token proporcionado es invalido o esta corrupto", 
            headers={"WWW-Authenticate": "Bearer"}
        )

    objeto_usuario = session.get(Usuario, id_usuario)
    if objeto_usuario is None:
        raise HTTPException(
            status_code=401, 
            detail="No fue posible encontrar al usuario", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return objeto_usuario