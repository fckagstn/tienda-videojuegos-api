import pytest
import uuid
from fastapi.testclient import TestClient
from tienda.main import app
from sqlalchemy.orm import Session
from tienda.dependencias import obtener_sesion
from sqlalchemy import create_engine
from tienda.configuracion import db_password, db_port, db_user
from tienda.modelos_mapeados import Base, Producto

@pytest.fixture
def cliente():
    return TestClient(app)

@pytest.fixture
def token(cliente, usuario_temporal):
    resultado_login = cliente.post("/login", json={
        "correo": usuario_temporal["correo"], 
        "contrasena": usuario_temporal["contrasena"]
    })

    datos_login = resultado_login.json()
    token = datos_login["access_token"]
    return token

@pytest.fixture
def usuario_temporal(cliente):
    str_nombre = str(uuid.uuid4())
    str_apellidos = str(uuid.uuid4())
    str_correo = f"{uuid.uuid4()}@dominio.com"
    str_contrasena = str(uuid.uuid4())

    cliente.post("/usuarios", json={
        "nombre": str_nombre, 
        "apellidos": str_apellidos, 
        "correo": str_correo, 
        "contrasena": str_contrasena
    })

    datos = {
        "correo": str_correo,
        "contrasena": str_contrasena
    }
    yield datos

engine_test = create_engine(f"postgresql+psycopg://{db_user}:{db_password}@localhost:{db_port}/tienda_test", echo=False)

def obtener_sesion_test():
    with Session(engine_test) as session:
        yield session


@pytest.fixture(autouse=True)
def crear_db_test_y_registrar_session():
    Base.metadata.create_all(engine_test)
    app.dependency_overrides[obtener_sesion] = obtener_sesion_test
    yield
    Base.metadata.drop_all(engine_test)
    app.dependency_overrides.clear()

@pytest.fixture
def producto_creado():
    nombre_prod = "Test"
    precio_prod = 9000
    categoria_prod = "Test"

    with Session(engine_test) as session:
        producto = Producto(nombre = nombre_prod, precio_centavos = precio_prod, categoria = categoria_prod)

        session.add(producto)
        session.commit()
        
        return producto.id