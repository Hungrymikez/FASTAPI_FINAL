# routes/cargar_archivo.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from io import BytesIO
from app.crud.cargar_archivo_pepeganga import insertar_datos_en_bd  # Ajusta si el archivo se llama distinto
from app.router.dependencies import get_current_user
from app.schemas.usuarios import RetornoUsuario
from core.database import get_db

router = APIRouter()

@router.post("/upload-excel-innovacion/", status_code=status.HTTP_201_CREATED)
async def upload_excel_innovacion(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    # 🔐 Validación de permisos (igual que en consultar_por_gmail)
    if user_token.id_rol != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos Excel (.xlsx)")

    contents = await file.read()
    df = pd.read_excel(BytesIO(contents), sheet_name="Hoja1", engine="openpyxl", header=0)

    expected_columns = [
        "Código Centro", "Centro de Formación ", "Vigencia proyecto", "SGPS Proyecto de investigación",
        "Nombre Completo del proyecto", "Instructor líder del Proyecto",
        "Tipo de vinculación Instructor líder del Proyecto",
        "Programas de Formación que impacta el proyecto",
        "Grupo de Investigación o Empresa Aliada del proyecto como coinvestigador",
        "Enlace a inventario de equipos del proyecto",
        "Enlace de Documentación del proyecto",
        "Relacione las líneas tecnológicas a la que se asocia el proyecto desde la linea de investigación  (linea de diseño de productos,Linea de producción y transformación del campo,linea de materiales y biotecnologia, linea de TICS e inteligencia artificial ,li",
        "Presupuesto",
        "Título completo del producto - resultado de Investigación, Desarrollo Tecnológico e innovación (I+D+i)",
        "Descripción del producto - resultado de Investigación, Desarrollo Tecnológico e innovación (I+D+i) ",
        "Año de publicación del producto resultado de Investigación, Desarrollo Tecnológico e innovación (I+D+i)",
        "Autores del producto resultado de Investigación, Desarrollo Tecnológico e innovación (I+D+i)  (separar con punto y coma (;) si son varios autores)",
        "Correos electrónicos de los autores del producto resultado de Investigación, Desarrollo Tecnológico e innovación (I+D+i)  (separar con punto y coma (;) y digitar en el orden en el cual se registraron los autores)",
        "Números telefónicos de contacto de los autores del producto resultado de Investigación, Desarrollo Tecnológico e innovación (I+D+i) (separar con punto y coma (;) y digitar en el orden en el cual se registraron los autores)",
        "Nombre completo y nivel del PROGRAMA DE FORMACIÓN al cual puede impactar el producto de investigación (relacione si aplica más de uno)",
        "El producto desarrollado está siendo utilizado en procesos formativos, sector productivo, empresa, otros). En caso afirmativo realice una breve explicación del uso",
        "Tipología del producto relacionado",
        "Área del conocimiento",
        "Si el producto se cargo a un repositorio del Sistema de Bibliotecas, copiar el enlace de consulta ",
        "Grupo de Investigación al que pertenece el proyecto",
        "Código del grupo de investigación (Este código debe coincidir con lo registrado en el aplicativo GrupLAC de Minciencias. Ejemplo: COLXXXXXX)",
        "Instructor lider Grupo de Investigación",
        "Semillero al que pertenece el proyecto",
        "Instructor Líder del Semillero",
        "Relacione los programas de formación a los que impacta el semillero de investigación",
        "Línea de investigación a la que pertenece el semillero (Debe coincidir con las líneas de investigación registradas en el GrupLAC)",
        "Temáticas sobre las que trabaja el semillero de investigación ",
        "Relacione las líneas tecnológicas a la que se asocia el semillero desde la linea de investigación"
    ]

    if list(df.columns) != expected_columns:
        raise HTTPException(status_code=400, detail="El formato del Excel no coincide con la plantilla esperada")

    # Renombrar a snake_case
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

    # Limpieza básica
    df = df.dropna(how="all")
    if "presupuesto" in df.columns:
        df["presupuesto"] = pd.to_numeric(
            df["presupuesto"].astype(str).str.replace(r"[^\d.-]", "", regex=True),
            errors="coerce"
        )

    # # Vaciar tabla antes de insertar (opcional pero recomendado para recargas completas)
    # from sqlalchemy import text
    # try:
    #     #db.execute(text("TRUNCATE TABLE proyectos_innovacion"))
    #     except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error al vaciar la tabla: {str(e)}")

    # Insertar datos
    try:
        resultado = insertar_datos_en_bd(db, df)
        return resultado
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {str(e)}")