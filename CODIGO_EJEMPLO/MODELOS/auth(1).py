from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.router.dependencies import authenticate_user
from app.schemas.auth import ResponseLoggin
from app.schemas.usuarios import UsuarioResponse
from app.services.usuario_service import UsuarioService
from core.security import create_access_token
from core.database import get_db
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/access", tags=["Autenticación (Legacy)"])

@router.post("/token", response_model=ResponseLoggin)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """Endpoint legacy de autenticación - Usa /api/v1/auth/token para nueva API"""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Datos Incorrectos en email o password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener información completa del usuario
    user_info = UsuarioService.get_by_id(db, user.id_usuario)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id_usuario), "rol": user.id_rol}
    )
    
    return ResponseLoggin(
        user=UsuarioResponse(**user_info),
        access_token=access_token
    )