from fastapi.testclient import TestClient
from tienda.main import app

cliente = TestClient(app)

def test_pedir_perfil_sin_cabecera_authorization_responde_401():
    respuesta = cliente.get("/perfil")
    assert respuesta.status_code == 401

def test_pedir_perfil_con_cabecera_con_basura_responde_401():
    respuesta = cliente.get("/perfil", headers={"Authorization": "Bearer abc"})
    assert respuesta.status_code == 401