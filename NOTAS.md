# Notas Pytest

* ****Un test correcto no significa que el código sea correcto:****

  Que un test pase únicamente significa que se cumple la ****propiedad que definí en el test****. Es posible obtener el resultado esperado siguiendo un camino incorrecto.

  > Un test verifica lo que le pedí que verificara, no necesariamente que toda la implementación sea correcta.

* ****Parámetros de ruta y nombres:****

  El nombre definido en la ruta y el nombre del parámetro de la función forman el mismo **contrato**. Si no coinciden, FastAPI no puede encontrar el valor esperado para el parámetro y la petición responde con **422 Unprocessable Entity**.

* ****Comparar un valor con un tipo:****

  `1 != int` compara el valor `1` con el objeto `int` (el tipo), por lo que la comparación da `True`. Si quiero comprobar si un valor pertenece a un tipo, utilizo `isinstance()`.

  ```python
  isinstance(1, int)  # True
  ```

* ****No guardar tokens directamente en el código:****

  Un token no debe quedar pegado en un archivo porque puede **expirar** y, además, si el archivo se sube a GitHub u otro repositorio, el token puede quedar **expuesto públicamente**. Las credenciales y tokens deben manejarse mediante variables de entorno, archivos `.env` (sin subirlos al repositorio) o un gestor de secretos.
