# models/proyectos_innovacion.py
from sqlalchemy import Column, Integer, String, Text, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProyectoInnovacion(Base):
    __tablename__ = "proyectos_innovacion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_centro = Column(String(50), nullable=True)
    centro_formacion = Column(String(255), nullable=True)
    vigencia_proyecto = Column(Integer, nullable=True)
    sgps_proyecto_investigacion = Column(String(100), nullable=True)
    nombre_completo_proyecto = Column(Text, nullable=True)
    instructor_lider_proyecto = Column(String(255), nullable=True)
    tipo_vinculacion_instructor = Column(String(100), nullable=True)
    programas_formacion_impacta = Column(Text, nullable=True)
    grupo_investigacion_coinvestigador = Column(String(255), nullable=True)
    enlace_inventario_equipos = Column(Text, nullable=True)
    enlace_documentacion_proyecto = Column(Text, nullable=True)
    lineas_tecnologicas = Column(Text, nullable=True)
    presupuesto = Column(Float, nullable=True)
    titulo_producto = Column(Text, nullable=True)
    descripcion_producto = Column(Text, nullable=True)
    anio_publicacion_producto = Column(Integer, nullable=True)
    autores_producto = Column(Text, nullable=True)
    correos_autores = Column(Text, nullable=True)
    telefonos_autores = Column(Text, nullable=True)
    programas_impacto_producto = Column(Text, nullable=True)
    uso_producto = Column(Text, nullable=True)
    tipologia_producto = Column(String(100), nullable=True)
    area_conocimiento = Column(String(100), nullable=True)
    enlace_repositorio = Column(Text, nullable=True)
    grupo_investigacion = Column(String(100), nullable=True)
    codigo_grupo_investigacion = Column(String(100), nullable=True)
    instructor_lider_grupo = Column(String(255), nullable=True)
    semillero_proyecto = Column(String(255), nullable=True)
    instructor_lider_semillero = Column(String(255), nullable=True)
    programas_impacta_semillero = Column(Text, nullable=True)
    linea_investigacion_semillero = Column(Text, nullable=True)
    tematicas_semillero = Column(Text, nullable=True)
    lineas_tecnologicas_semillero = Column(Text, nullable=True)