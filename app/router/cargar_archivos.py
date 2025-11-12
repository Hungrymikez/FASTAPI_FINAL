
from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
from sqlalchemy.orm import Session
from io import BytesIO
from app.crud.cargar_archivos import insertar_datos_en_bd
from core.database import get_db

router = APIRouter()

@router.post("/upload-excel-pe04/")
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    df = pd.read_excel(
        BytesIO(contents),
        engine="openpyxl",
        skiprows=4,
        usecols=[
            'CODIGO_REGIONAL', 'NOMBRE_REGIONAL', 'CODIGO_CENTRO', 'NOMBRE_CENTRO',
            'IDENTIFICADOR_FICHA', 'IDENTIFICADOR_UNICO_FICHA', 'ESTADO_CURSO',
            'CODIGO_NIVEL_FORMACION', 'NIVEL_FORMACION', 'CODIGO_JORNADA',
            'NOMBRE_JORNADA', 'FECHA_INICIO_FICHA', 'FECHA_TERMINACION_FICHA',
            'CODIGO_PROGRAMA', 'VERSION_PROGRAMA', 'NOMBRE_PROGRAMA_FORMACION',
            'NOMBRE_PROGRAMA_ESPECIAL', 'CODIGO_MODALIDAD', 'MODALIDAD_FORMACION',
            'ETAPA_FICHA', 'CODIGO_TIPO_OFERTA', 'TIPO_OFERTA', 'CODIGO_PROYECTO',
            'NOMBRE_PROYECTO', 'CODIGO_ESTADO', 'NOMBRE_ESTADO', 'CODIGO_TIPO_FORMACION',
            'TIPO_FORMACION', 'CODIGO_EMPRESA', 'NOMBRE_EMPRESA', 'CODIGO_MUNICIPIO_CURSO',
            'NOMBRE_MUNICIPIO_CURSO', 'CODIGO_DEPARTAMENTO_CURSO',
            'NOMBRE_DEPARTAMENTO_CURSO', 'NOMBRE_RESPONSABLE', 'CORREO_RESPONSABLE',
            'CODIGO_PRESUPUESTO', 'NOMBRE_PRESUPUESTO', 'NOMBRE_TIPO_FORMACION',
            'NOMBRE_NIVEL_FORMACION', 'CODIGO_SECTOR', 'NOMBRE_SECTOR',
            'TOTAL_APRENDICES', 'HORAS_PLANTA', 'HORAS_CONTRATISTAS',
            'HORAS_CONTRATISTAS_EXTERNOS', 'HORAS_MONITORES', 'HORAS_INST_EMPRESA',
            'TOTAL_HORAS', 'TOTAL_APRENDICES_ACTIVOS', 'DURACION_PROGRAMA',
            'NOMBRE_NUEVO_SECTOR'
        ],
        dtype=str 
    )
    print(df.head())  # paréntesis
    print(df.columns)
    print(df.dtypes)

    # Renombrar columnas
    df = df.rename(columns={
        # === Información de centro y regional ===
        "CODIGO_REGIONAL": "cod_regional",
        "NOMBRE_REGIONAL": "nombre_regional",
        "CODIGO_CENTRO": "cod_centro",
        "NOMBRE_CENTRO": "nombre_centro",

        # === Identificadores de ficha / grupo ===
        "IDENTIFICADOR_FICHA": "ficha",                    # → grupos.ficha
        "IDENTIFICADOR_UNICO_FICHA": "identificador_unico", # no está en BD (opcional)
        "ESTADO_CURSO": "estado_curso",                    # → grupos.estado_curso

        # === Nivel y jornada ===
        "CODIGO_NIVEL_FORMACION": "cod_nivel_formacion",
        "NIVEL_FORMACION": "nivel_formacion",              # → programas_formacion.nivel
        "CODIGO_JORNADA": "cod_jornada",
        "NOMBRE_JORNADA": "jornada",                       # → grupos.jornada

        # === Fechas ===
        "FECHA_INICIO_FICHA": "fecha_inicio",              # → grupos.fecha_inicio
        "FECHA_TERMINACION_FICHA": "fecha_fin",            # → grupos.fecha_fin

        # === Programa de formación ===
        "CODIGO_PROGRAMA": "cod_programa",                 # → programas_formacion.cod_programa
        "VERSION_PROGRAMA": "version",                     # → programas_formacion.version
        "NOMBRE_PROGRAMA_FORMACION": "nombre_programa",    # → programas_formacion.nombre
        "NOMBRE_PROGRAMA_ESPECIAL": "nombre_programa_especial",

        # === Modalidad y etapa ===
        "CODIGO_MODALIDAD": "cod_modalidad",
        "MODALIDAD_FORMACION": "modalidad",                # → grupos.modalidad
        "ETAPA_FICHA": "etapa_ficha",                      # → grupos.etapa_ficha

        # === Tipo de oferta / proyecto / estado ===
        "CODIGO_TIPO_OFERTA": "cod_tipo_oferta",
        "TIPO_OFERTA": "tipo_oferta",
        "CODIGO_PROYECTO": "cod_proyecto",
        "NOMBRE_PROYECTO": "nombre_proyecto",
        "CODIGO_ESTADO": "cod_estado",
        "NOMBRE_ESTADO": "nombre_estado",

        # === Tipo de formación / empresa ===
        "CODIGO_TIPO_FORMACION": "cod_tipo_formacion",
        "TIPO_FORMACION": "tipo_formacion",
        "CODIGO_EMPRESA": "cod_empresa",
        "NOMBRE_EMPRESA": "nombre_empresa",                # → grupos.nombre_empresa

        # === Ubicación geográfica ===
        "CODIGO_MUNICIPIO_CURSO": "cod_municipio",         # → grupos.cod_municipio
        "NOMBRE_MUNICIPIO_CURSO": "nombre_municipio",      # → municipios.nombre
        "CODIGO_DEPARTAMENTO_CURSO": "cod_departamento",
        "NOMBRE_DEPARTAMENTO_CURSO": "nombre_departamento",

        # === Responsable ===
        "NOMBRE_RESPONSABLE": "nombre_responsable",        # → grupos.nombre_responsable
        "CORREO_RESPONSABLE": "correo_responsable",

        # === Presupuesto y tipo formación ===
        "CODIGO_PRESUPUESTO": "cod_presupuesto",
        "NOMBRE_PRESUPUESTO": "nombre_presupuesto",
        "NOMBRE_TIPO_FORMACION": "nombre_tipo_formacion",
        "NOMBRE_NIVEL_FORMACION": "nombre_nivel_formacion",

        # === Sector ===
        "CODIGO_SECTOR": "cod_sector",
        "NOMBRE_SECTOR": "nombre_sector",

        # === Indicadores cuantitativos ===
        "TOTAL_APRENDICES": "total_aprendices",
        "HORAS_PLANTA": "horas_planta",
        "HORAS_CONTRATISTAS": "horas_contratistas",
        "HORAS_CONTRATISTAS_EXTERNOS": "horas_contratistas_externos",
        "HORAS_MONITORES": "horas_monitores",
        "HORAS_INST_EMPRESA": "horas_inst_empresa",
        "TOTAL_HORAS": "total_horas",
        "TOTAL_APRENDICES_ACTIVOS": "total_aprendices_activos",
        "DURACION_PROGRAMA": "duracion_programa",          # → programas_formacion.tiempo_duracion
        "NOMBRE_NUEVO_SECTOR": "nombre_nuevo_sector"
    })

    print(df.head())  # paréntesis

    # si quieren que funcione en todos los centros de pais 
    # crear codigo para llenar regionales centros y eliminar la siguiente linea.
    df = df[df["cod_centro"] == '9121']

    print(df.head())

    # Eliminar filas con valores faltantes en campos obligatorios
    required_fields = [ #ESTOS SON CAMPOS IMPORTANTES
        "cod_ficha", "cod_centro", "cod_programa", "la_version", "nombre", 
        "fecha_inicio", "fecha_fin", "etapa", "responsable", "nombre_municipio"
    ]
    df = df.dropna(subset=required_fields)

    # Convertir columnas a tipo numérico
    for col in ["cod_ficha", "cod_programa", "la_version", "cod_centro"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    print(df.head())  # paréntesis
    print(df.dtypes)

    # Convertir fechas
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce").dt.date
    df["fecha_fin"] = pd.to_datetime(df["fecha_fin"], errors="coerce").dt.date

    # Asegurar columnas no proporcionadas
    df["hora_inicio"] = "00:00:00"
    df["hora_fin"] = "00:00:00"
    df["aula_actual"] = ""

    # Crear DataFrame de programas únicos
    df_programas = df[["cod_programa", "la_version", "nombre"]].drop_duplicates()
    df_programas["horas_lectivas"] = 0 #AGREGAR UNA NUEVA COLUMNA 
    df_programas["horas_productivas"] = 0

    print(df_programas.head())

    # # Eliminar la columna nombre del df.
    # df = df.drop('nombre', axis=1)
    # print(df.head())

    df_centros = df[["cod_centro","nombre_centro","cod_regional","nombre_regional"]].drop_duplicates()
    print(df_centros.head())

    resultados = insertar_datos_en_bd(db, df_programas, df_centros)
    return resultados