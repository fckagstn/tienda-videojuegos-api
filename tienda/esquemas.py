from pydantic import BaseModel, ConfigDict, Field

class ProductoEntrada(BaseModel):
    nombre: str = Field(min_length=1)
    precio_centavos: int = Field(ge=1)
    categoria: str

class ProductoParche(BaseModel):
    nombre: str = Field(default=None, min_length=1)
    precio_centavos: int = Field(default=None, ge=1)
    categoria: str | None = None

class ProductoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    precio_centavos: int
    categoria: str | None

class UsuarioEntrada(BaseModel):
    nombre: str
    apellidos: str
    correo: str
    contrasena: str

class UsuarioSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    apellidos: str
    correo: str

class LoginEntrada(BaseModel):
    correo: str
    contrasena: str