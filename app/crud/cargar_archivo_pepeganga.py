# crud/cargar_archivo.py
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)




def insertar_datos_en_bd(db: Session, df_proyectos):
    db.execute(text("TRUNCATE TABLE proyectos_innovacion"))
    registros_insertados = 0
    errores = []

    insert_sql = text("""
        INSERT INTO proyectos_innovacion (
            codigo_centro, centro_formacion, vigencia_proyecto, sgps_proyecto_investigacion,
            nombre_completo_proyecto, instructor_lider_proyecto, tipo_vinculacion_instructor,
            programas_formacion_impacta, grupo_investigacion_coinvestigador,
            enlace_inventario_equipos, enlace_documentacion_proyecto, lineas_tecnologicas,
            presupuesto, titulo_producto, descripcion_producto, anio_publicacion_producto,
            autores_producto, correos_autores, telefonos_autores, programas_impacto_producto,
            uso_producto, tipologia_producto, area_conocimiento, enlace_repositorio,
            grupo_investigacion, codigo_grupo_investigacion, instructor_lider_grupo,
            semillero_proyecto, instructor_lider_semillero, programas_impacta_semillero,
            linea_investigacion_semillero, tematicas_semillero, lineas_tecnologicas_semillero
        ) VALUES (
            :codigo_centro, :centro_formacion, :vigencia_proyecto, :sgps_proyecto_investigacion,
            :nombre_completo_proyecto, :instructor_lider_proyecto, :tipo_vinculacion_instructor,
            :programas_formacion_impacta, :grupo_investigacion_coinvestigador,
            :enlace_inventario_equipos, :enlace_documentacion_proyecto, :lineas_tecnologicas,
            :presupuesto, :titulo_producto, :descripcion_producto, :anio_publicacion_producto,
            :autores_producto, :correos_autores, :telefonos_autores, :programas_impacto_producto,
            :uso_producto, :tipologia_producto, :area_conocimiento, :enlace_repositorio,
            :grupo_investigacion, :codigo_grupo_investigacion, :instructor_lider_grupo,
            :semillero_proyecto, :instructor_lider_semillero, :programas_impacta_semillero,
            :linea_investigacion_semillero, :tematicas_semillero, :lineas_tecnologicas_semillero
        )
    """)

    for idx, row in df_proyectos.iterrows():
        try:
            row_dict = row.to_dict()
            row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
            db.execute(insert_sql, row_dict)
            registros_insertados += 1
        except SQLAlchemyError as e:
            msg = f"Error al insertar proyecto (índice {idx}): {e}"
            errores.append(msg)
            logger.error(msg)
            db.rollback()

    db.commit()

    # 👇 Devuelve también una vista previa (máx. 100 filas) como lista de dict
    preview = df_proyectos.head(100).fillna("").to_dict(orient="records")

    return {
        "registros_insertados": registros_insertados,
        "errores": errores,
        "mensaje": "Carga completada con errores" if errores else "Carga completada exitosamente",
        "datos": preview  # 👈 esto es nuevo
    }