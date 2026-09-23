import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from tienda.configuracion import llave

ALGORITMO = "HS256"

texto_senuelo = "hola"

def hashear_contrasena(contrasena):
    contrasena_byte = contrasena.encode()
    sal = bcrypt.gensalt(rounds=10)
    contrasena_hashed = bcrypt.hashpw(contrasena_byte, sal)
    return contrasena_hashed.decode()

hash_senuelo = hashear_contrasena(texto_senuelo)

def verificar_contrasena(contrasena, hash_guardado):
    contrasena_byte = contrasena.encode()
    
    validacion = bcrypt.checkpw(contrasena_byte, hash_guardado.encode())
    return validacion

def crear_token(id_usuario):
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=30)
    datos = {
        "sub": str(id_usuario),
        "exp": expiracion
    }

    token = jwt.encode(datos, llave, algorithm=ALGORITMO)

    return token

def leer_token(token):
    token_decode = jwt.decode(token, llave, algorithms=[ALGORITMO])
    sub = int(token_decode["sub"])
    return sub