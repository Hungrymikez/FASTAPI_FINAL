from sqlalchemy import Column, BigInteger, Integer, String, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Archivo(Base):
    __tablename__ = "archivos"

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    id_proyecto = Column(Integer, ForeignKey("proyectos.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_almacenamiento = Column(String(255), nullable=False)
    fecha_carga = Column(Date, nullable=False)
    fecha_informe = Column(Date, nullable=False)
    responsable = Column(String(255), nullable=False)
    progreso = Column(Integer, nullable=False)
    observacion = Column(Text(255), nullable=True)
    tamano_archivo = Column(String(50), nullable=False)
    version = Column(String(50), nullable=False)
    categoria = Column(String(100), nullable=False)
    codigo_sgps = Column(String(100), nullable=True)
    nombre_centro = Column(String(255), nullable=True)
    regional = Column(String(100), nullable=True)
    responsables_proyecto = Column(Text(255), nullable=True)
    es_modificado = Column(Boolean, default=False, nullable=False)

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="archivos")
    archivos_modificados = relationship("ArchivoModificado", back_populates="archivo_original", foreign_keys="ArchivoModificado.id_archivo_original")

    def __repr__(self):
        return f"<Archivo(id={self.id}, nombre_archivo='{self.nombre_archivo}', id_proyecto={self.id_proyecto})>"

