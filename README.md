# Tienda de Videojuegos API

Este proyecto es una API de una tienda de videojuegos que responde a peticiones HTTP. Cuenta con registro de usuarios, login y autenticación con token, y maneja los errores siempre en formato JSON con status codes coherentes con los errores que ocurren. Además cuenta con pruebas hechas con pytest.

Por ejemplo, la API responde:

- **401** si no mandas el token, si es inválido o ya expiró, o si el correo o la contraseña son incorrectos.
- **404** si el producto que buscas no existe.
- **409** si el correo o el nombre del producto ya están en uso.
- **422** si mandas datos inválidos, como un precio en 0 o un id que no es número.
- **500** si algo falla dentro del servidor. La respuesta trae un `id_error`, que también queda en el log para poder encontrar qué pasó.

## Stack

- **Python**
- **FastAPI** como framework web
- **SQLAlchemy** como ORM
- **PostgreSQL** como base de datos
- **pytest** como herramienta de pruebas
- **bcrypt** y **PyJWT** como librerías de autenticación (bcrypt para proteger las contraseñas y PyJWT para los tokens)
- **Uvicorn** como servidor

## Endpoints

| Método | Ruta | Qué hace | Requiere token |
|--------|------|----------|----------------|
| POST | `/usuarios` | Registra un usuario nuevo | No |
| POST | `/login` | Inicia sesión y te devuelve un token | No |
| GET | `/perfil` | Muestra los datos de tu cuenta | Sí |
| GET | `/productos` | Lista todos los productos | No |
| GET | `/productos/{id}` | Muestra un producto por su id | No |
| POST | `/productos` | Agrega un producto nuevo | Sí |
| PUT | `/productos/{id}` | Reemplaza todos los datos de un producto | Sí |
| PATCH | `/productos/{id}` | Cambia solo los datos que le mandes de un producto | Sí |
| DELETE | `/productos/{id}` | Elimina un producto | Sí |

Para las rutas que piden token, primero haz login y manda el `access_token` que te devuelve en la cabecera `Authorization: Bearer <token>`. El token dura 30 minutos.

Los precios se manejan en centavos: `9000` son $90.00.

## Requisitos previos

- Python 3.10 o superior
- PostgreSQL instalado y corriendo en tu computadora

## Instalación

1. Clona el repositorio y entra a la carpeta:

   ```bash
   git clone https://github.com/fckagstn/tienda-videojuegos-api.git
   cd tienda-videojuegos-api
   ```

2. Crea un entorno virtual:

   ```bash
   python -m venv venv
   ```

   Y actívalo: en Windows con `venv\Scripts\activate` y en Linux o Mac con `source venv/bin/activate`.

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno: copia el archivo `.env.example`, renómbralo a `.env` y llénalo con tus datos.

   - `DB_USER` y `DB_PASSWORD`: tu usuario y contraseña de PostgreSQL.
   - `DB_PORT`: el puerto donde corre PostgreSQL. Si no lo pones, usa el 5432.
   - `LLAVE`: una cadena larga y aleatoria que se usa para firmar los tokens. Puedes generar una con `python -c "import secrets; print(secrets.token_hex(32))"`.
   - `CORREO` y `CONTRASENA`: no son obligatorias, el programa funciona sin ellas.

   Si falta `DB_USER`, `DB_PASSWORD` o `LLAVE`, el programa no arranca y te avisa cuál falta.

5. En PostgreSQL crea dos bases de datos, `tienda` para la API y `tienda_test` para las pruebas. Puedes hacerlo desde pgAdmin o con psql:

   ```sql
   CREATE DATABASE tienda;
   CREATE DATABASE tienda_test;
   ```
   Nota: `tienda_test` la crearan solo las pruebas

6. Crea las tablas de la base `tienda`:

   ```bash
   python -m tienda.modelos_mapeados
   ```

## Cómo levantarlo

Desde la carpeta del proyecto y con el entorno virtual activado, ejecuta:

```bash
uvicorn tienda.main:app --reload
```

La API queda corriendo en http://127.0.0.1:8000. Si entras a http://127.0.0.1:8000/docs puedes ver todos los endpoints y probar desde el navegador los que no piden token. Para los que sí lo piden usa Postman, Thunder Client o algo parecido, porque esa página no manda la cabecera `Authorization`.

## Cómo correr las pruebas

Con el entorno virtual activado y PostgreSQL corriendo, ejecuta desde la carpeta del proyecto:

```bash
pytest -v
```

Las pruebas revisan, por ejemplo, que no te deje ver tu perfil sin token, que un producto que no existe responda 404 y que los ids inválidos respondan 422. Usan la base `tienda_test`: crean las tablas antes de cada prueba y las borran al terminar, así que no tocan los datos de la base `tienda`.
