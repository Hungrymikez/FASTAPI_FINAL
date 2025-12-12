from pydantic import BaseModel
from app.schemas.usuarios import UsuarioResponse


class ResponseLoggin(BaseModel):
    user: UsuarioResponse
    access_token: str  