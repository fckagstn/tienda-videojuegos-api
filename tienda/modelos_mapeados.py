from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, String
from tienda.configuracion import db_user, db_password, db_port

# Creamos el engine que contendrá nuestra conexión a PosgreSQL
engine = create_engine(f"postgresql+psycopg://{db_user}:{db_password}@localhost:{db_port}/tienda", echo=True)

class Base(DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
    precio_centavos: Mapped[int]
    categoria: Mapped[str | None]

    def __repr__(self):
        return f"Producto {self.id}: {self.nombre}, {self.precio_centavos / 100.0} Pesos"

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    apellidos: Mapped[str]
    correo: Mapped[str] = mapped_column(unique=True)
    contrasena_hashed: Mapped[str] = mapped_column(String(255))

if __name__ == "__main__":
    Base.metadata.create_all(engine)
