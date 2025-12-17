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
from app.router import Archivos_innovacion_donald



from app.router import Archivos_innovacion

app = FastAPI(
    title="BACKEND FAST API V1",
    description="""
    # 🚀 Sistema de Gestión de Proyecto F
    
    ## Descripción
    Esta API permite gestionar las funcionalidades, junto a sus rutas para el modulo innovacion del SENA
    
    ## Funcionalidades
    - Gestión de usuarios
    - Administración de productos
    - Procesos de ventas
    - Reportes y analytics
    
    ## Desarrollo
    DESARROLLADO POR EL EQUIPO DE TRABAJO DE COGRYKEZ LAB STUDIO
    """,
    version="1.0.0",
        contact={
        "name": "HUNGRYMIKEZZ",
        "email": "codemaestablishment@gmail.com",
    }

)


@app.get("/",tags=["OK"])
def read_root():
    return {
                "message": "ok",
                "autor": "PEPEGANGA"
            }




app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir en el objeto app los routers
app.include_router(auth.router, prefix="/access", tags=["Servicios de login"])
app.include_router(usuarios.router, prefix="/usuario", tags=["Servicios usuarios"])
app.include_router(centros.router, prefix="/centro", tags=["Servicios de Centros de Formación"])
app.include_router(cargar_archivos.router, prefix="/cargar", tags=["Servicios de upload"])
app.include_router(programas.router)


app.include_router(cargar_archivo_pepeganga.router, prefix="/cargar_pepeganga", tags=["PEPEGANGA"])
app.include_router(cargar_archivo_pepeganga_seguro.router, prefix="/cargar_pepeganga_seguro", tags=["PEPEGANGA"])

app.include_router(Archivos_innovacion_donald.router, prefix="/innovacion_donald", tags=["SERVICIOS DE INNOVACION DONALD"])


app.include_router(Archivos_innovacion.router, prefix="/innovacion", tags=["SERVICIOS DE INNOVACION"])
# Configuración de CORS para permitir todas las solicitudes desde cualquier origen


origins = [
    "http://127.0.0.1:5501",  # Si usas Live Server en VS Code
    "http://127.0.0.1:5500", 
    "http://localhost:5500",
    "https://fastapifinal-production.up.railway.app", # Si ya está en producción
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)



