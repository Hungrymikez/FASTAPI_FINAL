from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date


class ProyectoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255, description="Nombre del proyecto")


class ProyectoCreate(ProyectoBase):
    pass


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)


class ProyectoResponse(ProyectoBase):
    id: int

    class Config:
        from_attributes = True


class ProyectoWithArchivos(ProyectoResponse):
    archivos: List["ArchivoResponse"] = []

    class Config:
        from_attributes = True


# Forward references
from app.schemas.archivo import ArchivoResponse
ProyectoWithArchivos.model_rebuild()

