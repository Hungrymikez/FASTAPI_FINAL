from sqlalchemy import Column, BigInteger, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class ArchivoModificado(Base):
    __tablename__ = "archivos_modificados"

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    id_archivo_original = Column(BigInteger, ForeignKey("archivos.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    id_proyecto = Column(Integer, ForeignKey("proyectos.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_almacenamiento = Column(String(255), nullable=False)
    fecha_subido = Column(Date, nullable=False)
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
    razon_modificado = Column(Text(255), nullable=True)

    # Relaciones
    archivo_original = relationship("Archivo", back_populates="archivos_modificados", foreign_keys=[id_archivo_original])
    proyecto = relationship("Proyecto", back_populates="archivos_modificados")

    def __repr__(self):
        return f"<ArchivoModificado(id={self.id}, nombre_archivo='{self.nombre_archivo}', id_archivo_original={self.id_archivo_original})>"

