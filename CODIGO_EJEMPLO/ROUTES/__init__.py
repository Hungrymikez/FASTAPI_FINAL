# Importar modelos para que SQLAlchemy los registre
from app.models.proyecto import Proyecto
from app.models.archivo import Archivo
from app.models.archivo_modificado import ArchivoModificado
from app.models.usuario import Usuario
from app.models.rol import Rol

__all__ = [
    "Proyecto",
    "Archivo",
    "ArchivoModificado",
    "Usuario",
    "Rol",
]

