# Notas Pytest

* **Tests que requieren autenticación:**
  Si un test necesita hacer un `POST` como un usuario autenticado, primero se deben obtener las credenciales del usuario y verificar que sean válidas contra la base de datos. Después se puede realizar la petición autenticada.

* **Un test correcto no significa que el código sea correcto:**
  Que un test pase únicamente significa que se cumple la **propiedad que definí en el test**. Es posible obtener el resultado esperado siguiendo un camino incorrecto.

  > Un test verifica lo que le pedí que verificara, no necesariamente que toda la implementación sea correcta.

* **TestClient en FastAPI:**
  Para realizar tests de endpoints de una aplicación FastAPI se utiliza `TestClient`, importándolo desde `fastapi.testclient`.
