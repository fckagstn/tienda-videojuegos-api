from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import tienda.rutas.productos as productos
import tienda.rutas.cuentas as cuentas

app = FastAPI()

@app.exception_handler(RequestValidationError)
def manejar_validacion(request, exc):
    mi_lista = []
    for error in exc.errors():
        loc = error["loc"]
        msg = error["msg"]
        mi_lista.append({loc[-1]: msg})

    return JSONResponse(status_code=422, content={"detail": mi_lista})

app.include_router(productos.router)
app.include_router(cuentas.router)
