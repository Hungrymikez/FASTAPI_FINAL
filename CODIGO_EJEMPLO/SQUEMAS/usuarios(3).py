from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UsuarioBase(BaseModel):
    nombre_completo: str = Field(..., min_length=3, max_length=80)
    id_rol: int
    correo: EmailStr
    num_documento: str = Field(..., min_length=3, max_length=12)
    estado: bool = True


class UsuarioCreate(UsuarioBase):
    contra_encript: str = Field(..., min_length=8)


class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = Field(default=None, min_length=3, max_length=80)
    correo: Optional[EmailStr] = None
    num_documento: Optional[str] = Field(default=None, min_length=3, max_length=12)
    id_rol: Optional[int] = None
    estado: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: int
    nombre_rol: Optional[str] = None

    class Config:
        from_attributes = True


class UsuarioPasswordUpdate(BaseModel):
    id_usuario: int
    contra_anterior: str = Field(..., min_length=8)
    contra_nueva: str = Field(..., min_length=8)


# Mantener compatibilidad con código existente
CrearUsuario = UsuarioCreate
RetornoUsuario = UsuarioResponse
Editar_usuario = UsuarioUpdate
EditarPass = UsuarioPasswordUpdate
