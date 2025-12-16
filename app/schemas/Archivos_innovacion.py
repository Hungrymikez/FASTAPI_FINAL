from typing import Optional, List
from pydantic import BaseModel, Field

class ProyectoSimple(BaseModel):
    id: int
    nombre: str


class ArchivoBase(BaseModel):
    nombre_proyecto: Optional[str] = None
    id_proyecto: int
    fecha_informe: Optional[str] = None  # "YYYY-MM-DD"
    responsable: Optional[str] = None
    progreso: Optional[int] = None
    observacion: Optional[str] = None
    tamano_archivo: Optional[str] = None
    version: Optional[str] = None
    categoria: Optional[str] = None
    codigo_sgps: Optional[str] = None
    nombre_centro: Optional[str] = None
    regional: Optional[str] = None
    responsables_proyecto: Optional[str] = None


class ArchivoCreate(ArchivoBase):
    nombre_archivo: str


class ArchivoModificadoCreate(ArchivoCreate):
    id_archivo_original: int
    razon_modificado: Optional[str] = None


class ArchivoMetaResponse(ArchivoBase):
    id: int
    nombre_archivo: str
    ruta_almacenamiento: Optional[str] = None
    # Usaremos fecha_carga para originales y fecha_subido para modificados
    # Si es original, este es fecha_carga. Si es modificado, este es fecha_subido.
    fecha_carga: Optional[str] = None 
    # Añadir fecha_subido para modificados, aunque Pydantic lo acepta si viene.
    fecha_subido: Optional[str] = None 


class ArchivoResponse(ArchivoMetaResponse):
    nombre_proyecto: Optional[str] = None
    archivo_tipo: Optional[str] = None  # 'original' | 'modificado'
    id_archivo_original: Optional[int] = None
    razon_modificado: Optional[str] = None


class ListaArchivosResponse(BaseModel):
    archivos: List[ArchivoResponse]