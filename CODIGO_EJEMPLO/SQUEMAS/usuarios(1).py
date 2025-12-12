from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.router.dependencies import get_current_user
from app.schemas.usuarios import (
    CrearUsuario, Editar_usuario, EditarPass, RetornoUsuario,
    UsuarioCreate, UsuarioUpdate, UsuarioPasswordUpdate
)
from core.database import get_db
from app.services.usuario_service import UsuarioService
from typing import List

router = APIRouter(prefix="/usuario", tags=["Usuarios (Legacy)"])


@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def create_user(
    user: CrearUsuario,
    db: Session = Depends(get_db),
    user_token: dict = Depends(get_current_user)
):
    """Endpoint legacy: Crear usuario - Usa /api/v1/usuarios/ para nueva API"""
    try:
        if user_token.get("id_rol") != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso")
        
        UsuarioService.create(db, UsuarioCreate(**user.model_dump()))
        return {"message": "Usuario creado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/obtener-por-id/{id_usuario}", status_code=status.HTTP_200_OK, response_model=RetornoUsuario)
def get_by_id(
    id_usuario: int,
    db: Session = Depends(get_db),
    user_token: dict = Depends(get_current_user)
):
    """Endpoint legacy: Obtener usuario por ID - Usa /api/v1/usuarios/{id} para nueva API"""
    try:
        user = UsuarioService.get_by_id(db, id_usuario)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return RetornoUsuario(**user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/obtener-por-email/{email}", status_code=status.HTTP_200_OK, response_model=RetornoUsuario)
def get_by_email(
    email: str,
    db: Session = Depends(get_db),
    user_token: dict = Depends(get_current_user)
):
    """Endpoint legacy: Obtener usuario por email - Usa /api/v1/usuarios/email/{email} para nueva API"""
    try:
        user = UsuarioService.get_by_email(db, email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return RetornoUsuario(**user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/editar/{user_id}")
def update_user(
    user_id: int,
    user: Editar_usuario,
    db: Session = Depends(get_db),
    user_token: dict = Depends(get_current_user)
):
    """Endpoint legacy: Editar usuario - Usa /api/v1/usuarios/{id} para nueva API"""
    try:
        if user_token.get("id_rol") != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso")
        
        usuario_actualizado = UsuarioService.update(db, user_id, UsuarioUpdate(**user.model_dump()))
        if not usuario_actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return {"message": "Usuario actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/eliminar/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id_usuario: int,
    db: Session = Depends(get_db),
    user_token: dict = Depends(get_current_user)
):
    """Endpoint legacy: Eliminar usuario - Usa DELETE /api/v1/usuarios/{id} para nueva API"""
    try:
        if user_token.get("id_rol") != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso")
        
        success = UsuarioService.delete(db, id_usuario)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/editar-contrasena")
def update_password(
    user: EditarPass,
    db: Session = Depends(get_db),
    user_token: dict = Depends(get_current_user)
):
    """Endpoint legacy: Editar contraseña - Usa PUT /api/v1/usuarios/cambiar-contrasena para nueva API"""
    try:
        if user_token.get("id_rol") != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso")
        
        UsuarioService.update_password(db, UsuarioPasswordUpdate(**user.model_dump()))
        return {"message": "Contraseña actualizada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/obtener-todos", status_code=status.HTTP_200_OK, response_model=List[RetornoUsuario])
def get_all(db: Session = Depends(get_db)):
    """Endpoint legacy: Obtener todos los usuarios - Usa GET /api/v1/usuarios/ para nueva API"""
    try:
        users = UsuarioService.get_all(db)
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuarios no encontrados")
        return [RetornoUsuario(**u) for u in users]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/obtener-todos-secure", status_code=status.HTTP_200_OK, response_model=List[RetornoUsuario])
def get_all_s(
    db: Session = Depends(get_db),
    user_token: dict = Depends(get_current_user)
):
    """Endpoint legacy: Obtener todos los usuarios (seguro) - Usa GET /api/v1/usuarios/seguros para nueva API"""
    try:
        if user_token.get("id_rol") != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para ver usuarios"
            )
        
        users = UsuarioService.get_all(db)
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuarios no encontrados")
        return [RetornoUsuario(**u) for u in users]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
