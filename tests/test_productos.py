from fastapi.testclient import TestClient
from tienda.main import app
from tienda.configuracion import correo, contrasena

cliente = TestClient(app)

def test_pedir_productos_responde_200():
    respuesta = cliente.get("/productos")
    assert respuesta.status_code == 200

def test_respuesta_de_pedir_productos_es_una_lista():
    respuesta = cliente.get("/productos")
    datos = respuesta.json()
    assert isinstance(datos, list)

def test_pedir_producto_por_id_responde_200():
    respuesta = cliente.get("/productos/1")
    assert respuesta.status_code == 200

def test_pedir_producto_por_id_inexistente_responde_404():
    respuesta = cliente.get("/productos/9999")
    assert respuesta.status_code == 404

def test_pedir_producto_por_id_negativo_responde_422():
    respuesta = cliente.get("/productos/-1")
    assert respuesta.status_code == 422

def test_pedir_producto_por_id_cero_responde_422():
    respuesta = cliente.get("/productos/0")
    assert respuesta.status_code == 422

def test_pedir_producto_por_id_str_responde_422():
    respuesta = cliente.get("/productos/hola")
    assert respuesta.status_code == 422

def test_agregar_producto_nuevo_responde_201():
    respuesta_login = cliente.post("/login", json={"correo": correo, "contrasena": contrasena})
    datos_respuesta = respuesta_login.json()
    token = datos_respuesta["access_token"]

    respuesta_post = cliente.post("/productos", headers={"Authorization": f"Bearer {token}"}, json={"nombre": "Consola N64", "precio_centavos": 9000, "categoria": "Accesorio"})
    assert respuesta_post.status_code == 201