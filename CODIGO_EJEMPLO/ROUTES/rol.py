from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import relationship
from core.database import Base


class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(SmallInteger, primary_key=True, autoincrement=True)
    nombre_rol = Column(String(20), nullable=False)

    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")

    def __repr__(self):
        return f"<Rol(id_rol={self.id_rol}, nombre_rol='{self.nombre_rol}')>"

