from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_completo = Column(String(80), nullable=False)
    num_documento = Column(String(12), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contra_encript = Column(String(140), nullable=False)
    id_rol = Column(SmallInteger, ForeignKey("rol.id_rol"), nullable=False)
    estado = Column(Boolean, default=True, nullable=False)

    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")

    def __repr__(self):
        return f"<Usuario(id_usuario={self.id_usuario}, correo='{self.correo}')>"

