from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


class ArchivoModificadoBase(BaseModel):
    id_archivo_original: int = Field(..., description="ID del archivo original")
    id_proyecto: int = Field(..., description="ID del proyecto")
    nombre_archivo: str = Field(..., min_length=1, max_length=255)
    ruta_almacenamiento: str = Field(..., min_length=1, max_length=255)
    fecha_subido: date
    fecha_informe: date
    responsable: str = Field(..., min_length=1, max_length=255)
    progreso: int = Field(..., ge=0, le=100, description="Progreso del archivo (0-100)")
    observacion: Optional[str] = Field(None, max_length=255)
    tamano_archivo: str = Field(..., min_length=1, max_length=50)
    version: str = Field(..., min_length=1, max_length=50)
    categoria: str = Field(..., min_length=1, max_length=100)
    codigo_sgps: Optional[str] = Field(None, max_length=100)
    nombre_centro: Optional[str] = Field(None, max_length=255)
    regional: Optional[str] = Field(None, max_length=100)
    responsables_proyecto: Optional[str] = Field(None, max_length=255)
    razon_modificado: Optional[str] = Field(None, max_length=255)


class ArchivoModificadoCreate(ArchivoModificadoBase):
    pass


class ArchivoModificadoUpdate(BaseModel):
    id_archivo_original: Optional[int] = None
    id_proyecto: Optional[int] = None
    nombre_archivo: Optional[str] = Field(None, min_length=1, max_length=255)
    ruta_almacenamiento: Optional[str] = Field(None, min_length=1, max_length=255)
    fecha_subido: Optional[date] = None
    fecha_informe: Optional[date] = None
    responsable: Optional[str] = Field(None, min_length=1, max_length=255)
    progreso: Optional[int] = Field(None, ge=0, le=100)
    observacion: Optional[str] = Field(None, max_length=255)
    tamano_archivo: Optional[str] = Field(None, min_length=1, max_length=50)
    version: Optional[str] = Field(None, min_length=1, max_length=50)
    categoria: Optional[str] = Field(None, min_length=1, max_length=100)
    codigo_sgps: Optional[str] = Field(None, max_length=100)
    nombre_centro: Optional[str] = Field(None, max_length=255)
    regional: Optional[str] = Field(None, max_length=100)
    responsables_proyecto: Optional[str] = Field(None, max_length=255)
    razon_modificado: Optional[str] = Field(None, max_length=255)


class ArchivoModificadoResponse(ArchivoModificadoBase):
    id: int

    class Config:
        from_attributes = True


class ArchivoModificadoWithRelations(ArchivoModificadoResponse):
    archivo_original: Optional["ArchivoResponse"] = None
    proyecto: Optional["ProyectoResponse"] = None

    class Config:
        from_attributes = True


# Forward references
from app.schemas.archivo import ArchivoResponse
from app.schemas.proyecto import ProyectoResponse
ArchivoModificadoWithRelations.model_rebuild()

