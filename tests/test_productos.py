def test_pedir_productos_responde_200(cliente):
    respuesta = cliente.get("/productos")
    assert respuesta.status_code == 200

def test_respuesta_de_pedir_productos_es_una_lista(cliente):
    respuesta = cliente.get("/productos")
    datos = respuesta.json()
    assert isinstance(datos, list)

def test_pedir_producto_por_id_responde_200(cliente, producto_creado):
    respuesta = cliente.get(f"/productos/{producto_creado}")
    assert respuesta.status_code == 200

def test_pedir_producto_por_id_inexistente_responde_404(cliente):
    respuesta = cliente.get("/productos/9999")
    assert respuesta.status_code == 404

def test_pedir_producto_por_id_negativo_responde_422(cliente):
    respuesta = cliente.get("/productos/-1")
    assert respuesta.status_code == 422

def test_pedir_producto_por_id_cero_responde_422(cliente):
    respuesta = cliente.get("/productos/0")
    assert respuesta.status_code == 422

def test_pedir_producto_por_id_str_responde_422(cliente):
    respuesta = cliente.get("/productos/hola")
    assert respuesta.status_code == 422

def test_agregar_producto_nuevo_responde_201(cliente, token):
    respuesta_post = cliente.post("/productos", headers={"Authorization": f"Bearer {token}"}, json={"nombre": "Consola N64", "precio_centavos": 9000, "categoria": "Accesorio"})
    assert respuesta_post.status_code == 201

def test_actualizar_producto_put_por_id_negativo_responde_422(cliente, token):
    respuesta_put = cliente.put("/productos/-1", headers={"Authorization": f"Bearer {token}"}, json={"nombre": "Consola Gamecube", "precio_centavos": 9000, "categoria": "Accesorio"})
    assert respuesta_put.status_code == 422

def test_actualizar_producto_patch_por_id_negativo_responde_422(cliente, token):
    respuesta_patch = cliente.patch("/productos/-1", headers={"Authorization": f"Bearer {token}"}, json={"nombre": "Consola PS1"})
    assert respuesta_patch.status_code == 422

def test_borrar_producto_por_id_negativo_responde_422(cliente, token):
    respuesta_put = cliente.delete("/productos/-1", headers={"Authorization": f"Bearer {token}"})
    assert respuesta_put.status_code == 422

def test_obtener_producto_por_id_devuelve_cuerpo_id(cliente, producto_creado):
    respuesta = cliente.get(f"/productos/{producto_creado}")
    datos_respuesta = respuesta.json()
    id_producto = datos_respuesta["id"]
    assert id_producto == producto_creado

def test_usuario_logueado_responde_200(cliente, usuario_temporal):
    respuesta = cliente.post("/login", json={"correo": usuario_temporal["correo"], "contrasena": usuario_temporal["contrasena"]})
    assert respuesta.status_code == 200