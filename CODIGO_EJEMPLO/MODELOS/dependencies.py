from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.usuario_service import UsuarioService
from core.security import verify_password, verify_token
from core.database import get_db
from fastapi.security import OAuth2PasswordBearer
from app.schemas.usuarios import UsuarioResponse


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/access/token")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    """Dependencia legacy para obtener usuario actual - Usa app.api.v1.dependencies para nueva API"""
    user_id = verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Invalido")
    
    user_info = UsuarioService.get_by_id(db, user_id)
    if user_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    if not user_info.get("estado", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo. No autorizado")
    
    # Convertir a formato legacy (dict) para compatibilidad
    return user_info


def authenticate_user(username: str, password: str, db: Session):
    """Función legacy de autenticación - Usa app.api.v1.dependencies para nueva API"""
    user = UsuarioService.get_by_email_security(db, username)
    if not user:
        return False
    if not verify_password(password, user.contra_encript):
        return False
    return user