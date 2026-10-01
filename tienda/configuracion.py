import os
from dotenv import load_dotenv

load_dotenv()

db_port = os.getenv("DB_PORT", "5432")

correo = os.getenv("CORREO")
contrasena = os.getenv("CONTRASENA")

variables_obligatorias = {
    "DB_USER": os.getenv("DB_USER"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    "LLAVE": os.getenv("LLAVE"),
}

lista = [variable for variable, valor in variables_obligatorias.items() if not valor]
if lista:
    raise RuntimeError(f"Falta la variable de entorno obligatoria: {', '.join(lista)}")

db_user = variables_obligatorias["DB_USER"]
db_password = variables_obligatorias["DB_PASSWORD"]
llave = variables_obligatorias["LLAVE"]