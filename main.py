from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.router import usuarios
from app.router import centros
from app.router import auth
from app.router import cargar_archivos
from app.router import programas
from app.router import cargar_archivo_pepeganga
from app.router import cargar_archivo_pepeganga_seguro

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir en el objeto app los routers
app.include_router(usuarios.router, prefix="/usuario", tags=["Servicios usuarios"])
app.include_router(centros.router, prefix="/centro", tags=["Servicios de Centros de Formación"])
app.include_router(auth.router, prefix="/access", tags=["Servicios de login"])
app.include_router(cargar_archivos.router, prefix="/cargar", tags=["Servicios de upload"])
app.include_router(programas.router)


app.include_router(cargar_archivo_pepeganga.router, prefix="/cargar_pepeganga", tags=["PEPEGANGA"])
app.include_router(cargar_archivo_pepeganga_seguro.router, prefix="/cargar_pepeganga_seguro", tags=["PEPEGANGA"])

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen

origins = [
    "http://127.0.0.1:5501",  # Si usas Live Server en VS Code
    "http://localhost:5500",
    "https://fastapifinal-production.up.railway.app", # Si ya está en producción
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

@app.get("/")
def read_root():
    return {
                "message": "ok",
                "autor": "PEPEGANGA"
            }


