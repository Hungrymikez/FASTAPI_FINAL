from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    nombre = Column(String(255), nullable=False)

    # Relaciones
    archivos = relationship("Archivo", back_populates="proyecto", cascade="all, delete-orphan")
    archivos_modificados = relationship("ArchivoModificado", back_populates="proyecto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Proyecto(id={self.id}, nombre='{self.nombre}')>"

