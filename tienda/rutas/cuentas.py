from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from tienda.dependencias import obtener_usuario, obtener_sesion
from tienda.modelos_mapeados import Usuario
from tienda.esquemas import UsuarioEntrada, UsuarioSalida, LoginEntrada
from sqlalchemy.exc import IntegrityError
from psycopg.errors import UniqueViolation
from tienda.seguridad import hashear_contrasena, verificar_contrasena, crear_token, dummy_hash

router = APIRouter()

@router.post("/usuarios", status_code=201, response_model=UsuarioSalida)
def crear_usuario_nuevo(usuario:UsuarioEntrada, session = Depends(obtener_sesion)):
    contrasena = usuario.contrasena
    contrasena_hashed = hashear_contrasena(contrasena)

    usuario_nuevo = Usuario(nombre=usuario.nombre, apellidos=usuario.apellidos, correo=usuario.correo, contrasena_hashed=contrasena_hashed)

    try:
        session.add(usuario_nuevo)
        session.commit()
    
    except IntegrityError as e:
        session.rollback()
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=409, detail="El correo no se encuentra disponible para su uso")
        raise

    return usuario_nuevo
    
@router.post("/login")
def autenticar_login(datos_login: LoginEntrada, session = Depends(obtener_sesion)):
    consulta = select(Usuario).where(Usuario.correo == datos_login.correo)
    objeto_usuario = session.scalars(consulta).first()

    if objeto_usuario is None:
        validacion_senuelo = verificar_contrasena(datos_login.contrasena, dummy_hash)
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    validacion = verificar_contrasena(datos_login.contrasena, objeto_usuario.contrasena_hashed)

    if validacion:
        token = crear_token(objeto_usuario.id)

        datos = {
            "access_token": token,
            "token_type": "bearer"
        }
        return datos
    
    else:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.get("/perfil", response_model=UsuarioSalida)
def leer_perfil(usuario = Depends(obtener_usuario)):
    return usuario