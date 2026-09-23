from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from tienda.dependencias import obtener_usuario, obtener_sesion
from tienda.modelos_mapeados import Producto
from tienda.esquemas import ProductoSalida, ProductoEntrada, ProductoParche
from sqlalchemy.exc import IntegrityError
from psycopg.errors import UniqueViolation, ForeignKeyViolation

router = APIRouter(prefix="/productos")

@router.get("", response_model=list[ProductoSalida])
def devolver_productos(session = Depends(obtener_sesion)):
    objetos = session.scalars(select(Producto))
    resultados = objetos.all()
    return resultados

@router.get("/{id}", response_model=ProductoSalida)
def devolver_producto(id: int, session = Depends(obtener_sesion)):
    objeto = session.get(Producto, id)
    if objeto is None:
        raise HTTPException(status_code=404, detail="No existe el producto que buscas")
    return objeto

@router.post("", status_code=201, response_model=ProductoSalida)
def agregar_producto_nuevo(producto: ProductoEntrada, usuario = Depends(obtener_usuario), session = Depends(obtener_sesion)):
    objeto = producto.model_dump()
    producto_nuevo = Producto(**objeto)
    session.add(producto_nuevo)
    try:
        session.commit()

    except IntegrityError as e:
        session.rollback()
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=409, detail="Ya existe un producto con ese nombre")
        raise
   
    return producto_nuevo
    
@router.put("/{id}", response_model=ProductoSalida)
def actualizar_producto(id: int, producto: ProductoEntrada, usuario = Depends(obtener_usuario), session = Depends(obtener_sesion)):
    objeto = session.get(Producto, id)
    if objeto is None:
        raise HTTPException(status_code=404, detail="No existe el producto que buscas")
    
    datos = producto.model_dump()
    for clave, valor in datos.items():
        setattr(objeto, clave, valor)

    try:    
        session.commit()

    except IntegrityError as e:
        session.rollback()
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=409, detail="Ya existe un producto con ese nombre")
        raise

    return objeto 
    
@router.patch("/{id}", response_model=ProductoSalida)
def actualizar_elemento_especifico_producto(producto: ProductoParche, id: int, usuario = Depends(obtener_usuario), session = Depends(obtener_sesion)):
    objeto = session.get(Producto, id)
    if objeto is None:
        raise HTTPException(status_code=404, detail="No existe el producto que buscas")
    
    datos = producto.model_dump(exclude_unset=True)
    if not datos:
        raise HTTPException(status_code=422, detail="No hay datos")
    
    for clave, valor in datos.items():
        setattr(objeto, clave, valor)

    try:
        session.commit()

    except IntegrityError as e:
        session.rollback()
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=409, detail="Ya existe un producto con ese nombre")
        raise

    return objeto

@router.delete("/{id}", status_code=204)
def borrar_producto(id: int, usuario = Depends(obtener_usuario),session = Depends(obtener_sesion)):
    
    objeto = session.get(Producto, id)
    if objeto is None:
        raise HTTPException(status_code=404, detail="No existe el id que intentas eliminar")
        
    session.delete(objeto)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        if isinstance(e.orig, ForeignKeyViolation):
            raise HTTPException(status_code=409, detail="No se puede eliminar un producto con ventas registradas")
        raise