from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
from sqlalchemy.orm import Session
from io import BytesIO
from app.crud.cargar_archivo_pepeganga import insertar_datos_en_bd
from core.database import get_db

router = APIRouter()

@router.post("/upload-excel-innovacion/")
async def upload_excel_innovacion(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    
    # Leer Hoja1 del Excel
    df = pd.read_excel(
        BytesIO(contents),
        sheet_name="Hoja1",
        engine="openpyxl",
        header=0  # Primera fila como encabezado
    )

    # Renombrar columnas a snake_case (coinciden con los campos del modelo)
    df.columns = [
        "codigo_centro", "centro_formacion", "vigencia_proyecto", "sgps_proyecto_investigacion",
        "nombre_completo_proyecto", "instructor_lider_proyecto", "tipo_vinculacion_instructor",
        "programas_formacion_impacta", "grupo_investigacion_coinvestigador",
        "enlace_inventario_equipos", "enlace_documentacion_proyecto", "lineas_tecnologicas",
        "presupuesto", "titulo_producto", "descripcion_producto", "anio_publicacion_producto",
        "autores_producto", "correos_autores", "telefonos_autores", "programas_impacto_producto",
        "uso_producto", "tipologia_producto", "area_conocimiento", "enlace_repositorio",
        "grupo_investigacion", "codigo_grupo_investigacion", "instructor_lider_grupo",
        "semillero_proyecto", "instructor_lider_semillero", "programas_impacta_semillero",
        "linea_investigacion_semillero", "tematicas_semillero", "lineas_tecnologicas_semillero"
    ]

    # Eliminar filas completamente vacías
    df.dropna(how="all", inplace=True)

    # Asegurarte de que los tipos coincidan (presupuesto como float, etc.)
    if "presupuesto" in df.columns:
        df["presupuesto"] = pd.to_numeric(df["presupuesto"].astype(str).str.replace(r"[^\d.-]", "", regex=True), errors="coerce")

    # Llamar al CRUD
    resultado = insertar_datos_en_bd(db, df)

    return resultado