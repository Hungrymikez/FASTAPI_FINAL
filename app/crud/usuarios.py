from fastapi import HTTPException , status
from sqlalchemy.orm import Session
from sqlalchemy import text, true
from typing import Optional
import logging

from sqlalchemy.exc import SQLAlchemyError

from app.schemas.usuarios import CrearUsuario, EditarPass, Editar_usuario, RetornoUsuario
from core.security import get_hashed_password, verify_password

logger = logging.getLogger(__name__)

def create_user(db: Session, user: CrearUsuario) -> Optional[bool]:
    try: #AQUI VA EL SQL
        # dataUser = user.model_dump()
        # contra_original = dataUser["contra_encript"]
        # print(contra_original)

        # contra_encriptada = get_hashed_password(contra_original)
        # print(contra_encriptada)

        dataUser = user.model_dump()
        
        contra_original = dataUser["contra_encript"]
        
        contra_encriptada = get_hashed_password(contra_original)

        dataUser["contra_encript"] = contra_encriptada





        query = text(""" 
            INSERT INTO usuario (
                nombre_completo, num_documento, 
                correo, contra_encript, id_rol,
                estado
            ) VALUES (
                :nombre_completo, :num_documento,
                :correo, :contra_encript, :id_rol,
                :estado
            )
        """)
        db.execute(query, dataUser)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al crear el usuario")



def get_user_by_id(db: Session, id_usuario: int) -> RetornoUsuario:
    try:
        query = text("""
                    SELECT 
                        usuario.id_usuario, 
                        usuario.nombre_completo,
                        usuario.num_documento,
                        usuario.correo,
                        usuario.contra_encript,
                        usuario.id_rol,
                        usuario.estado, rol.nombre_rol
                    FROM usuario 
                    INNER JOIN rol ON usuario.id_rol = rol.id_rol 
                    WHERE usuario.id_usuario = :id_user
            
        """)
        result = db.execute(query,{"id_user": id_usuario}). mappings().first() ##ESTO SE USA PARA EJECUTAR EL QUERY DANDOLE EL PARAMETRO DEL ID USUARIO 
        
        return result

    except SQLAlchemyError as e:
        # db.rollback()   ESTO NO SE NECESITA YA QUE SOLO SE ESTA CONSULTANDO 
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al consultar el usuario")
    

def get_user_by_email(db: Session, un_correo: str):
    try:
        query = text("""
                    SELECT 
                        usuario.id_usuario, 
                        usuario.nombre_completo,
                        usuario.num_documento,
                        usuario.correo,
                        usuario.contra_encript,
                        usuario.id_rol,
                        usuario.estado, rol.nombre_rol
                    FROM usuario 
                    INNER JOIN rol ON usuario.id_rol = rol.id_rol 
                    WHERE usuario.correo = :email
            
        """)
        #TOCA MANDAR LA CLAVE Y EL VALOR DE LO QUE SE VA A BUSCAR
        result = db.execute(query,{"email": un_correo}). mappings().first() ##ESTO SE USA PARA EJECUTAR EL QUERY DANDOLE EL PARAMETRO DEL ID USUARIO 
        
        return result

    except SQLAlchemyError as e:
        # db.rollback()   ESTO NO SE NECESITA YA QUE SOLO SE ESTA CONSULTANDO 
        logger.error(f"Error al buscar usuario por email: {e}")
        raise Exception("Error de base de datos al buscar el usuario")
    

#ELIMINAR USUARIO
def user_delete(db: Session, id: int):
    try:
                            # ESTO SE DEBE DE PONER WHERE usuario.id_usuario = :el_id
        query = text("""
                    DELETE FROM usuario
                    WHERE id_usuario = :el_id
            
        """)
        db.execute(query,{"el_id": id})
        db.commit()
        return true

        # result = db.execute(query,{"el_id": id})
        # db.commit()
        # if result.rowcount == 0:
        #     raise Exception(f"No se encontró el usuario con id {id}")
        # # Devolver confirmación
        # return {"mensaje": f"Usuario con id {id} eliminado correctamente"}


        #return True
        #TOCA MANDAR LA CLAVE Y EL VALOR DE LO QUE SE VA A BUSCAR
        # result = db.execute(query,{"el_id": id}) ##ESTO SE USA PARA EJECUTAR EL QUERY DANDOLE EL PARAMETRO DEL ID USUARIO 

    except SQLAlchemyError as e:
        # db.rollback()   ESTO NO SE NECESITA YA QUE SOLO SE ESTA CONSULTANDO
        db.rollback()
        logger.error(f"Error al eliminar usuario por id: {e}")
        raise Exception("Error de base de datos al eliminar el usuario")
    


#ACTUALIZAR USUARIO

def update_user(db: Session, user_id: int, user_update: Editar_usuario) -> bool:
    try:
        fields = user_update.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["user_id"] = user_id

        query = text(f"UPDATE usuario SET {set_clause} WHERE id_usuario = :user_id")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")



def update_password(db: Session, user_data: EditarPass) -> bool:
    try:
        datos_usuario = user_data.model_dump()
        contra_encript = get_hashed_password(datos_usuario['contra_nueva'])
        datos_usuario['pass_encript'] = contra_encript

        query = text(f""" UPDATE usuario SET contra_encript = :pass_encript 
                        WHERE id_usuario = :id_usuario """)
        db.execute(query, datos_usuario)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")


def verify_user_pass(db: Session, user_data: EditarPass) -> bool:
    try:
        query = text("""
            SELECT usuario.contra_encript
            FROM usuario
            WHERE usuario.id_usuario = :id_user
        """)

        result = db.execute(query, {"id_user": user_data.id_usuario }).mappings().first()
        contra_en_db = result.contra_encript
        contra_anterior = user_data.contra_anterior
        print(contra_en_db)
        print(contra_anterior)

        validated = verify_password(contra_anterior, contra_en_db)

        if not validated:
            return False
        else:
            return True
    
    except SQLAlchemyError as e:
        logger.error(f"Error al bucar validar la contraseña: {e}")
        raise Exception("Error de base de datos al validar la contraseña")