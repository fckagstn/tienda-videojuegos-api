def test_pedir_perfil_sin_cabecera_authorization_responde_401(cliente):
    respuesta = cliente.get("/perfil")
    assert respuesta.status_code == 401

def test_pedir_perfil_con_cabecera_con_basura_responde_401(cliente):
    respuesta = cliente.get("/perfil", headers={"Authorization": "Bearer abc"})
    assert respuesta.status_code == 401