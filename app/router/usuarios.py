
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.usuarios import CrearUsuario, EditarPass, Editar_usuario, RetornoUsuario
from core.database import get_db
from app.crud import usuarios as crud_users

from sqlalchemy.exc import SQLAlchemyError
from app.router.dependencies import get_current_user
router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)#DECORADOR
def create_user(
    user: CrearUsuario, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)

):
    print(user_token)
    try:
        if user_token.id_rol != 1:
                # raise HTTPException(status_code=500, detail="No tienes permisos")
                raise HTTPException(status_code=403, detail="No tienes permisos")


        crud_users.create_user(db, user)
        return {"message": "Usuario creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/consultar_id/{id_usuario}", status_code=status.HTTP_201_CREATED, response_model=RetornoUsuario) #DECORADOR
def get_by_id(id_usuario: int, 
              db: Session = Depends(get_db),
              user_token: RetornoUsuario = Depends(get_current_user)):


    try:
        # return crud_users.get_user_by_id(db, id_usuario)
        if user_token.id_rol != 1:
        # raise HTTPException(status_code=500, detail="No tienes permisos")
            raise HTTPException(status_code=403, detail="No tienes permisos")

        result = crud_users.get_user_by_id(db, id_usuario)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Usuario No encontrado")
        return result 
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/consultar_por_gmail/{correo}", status_code=status.HTTP_201_CREATED, response_model=RetornoUsuario) #DECORADOR
def get_by_email(correo: str, db: Session = Depends(get_db),user_token: RetornoUsuario = Depends(get_current_user)):

    try:
        # return crud_users.get_user_by_id(db, id_usuario)
        if user_token.id_rol != 1:
        # raise HTTPException(status_code=500, detail="No tienes permisos")
            raise HTTPException(status_code=403, detail="No tienes permisos")
        

        result = crud_users.get_user_by_email(db, correo)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Usuario No encontrado")
        return result 
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    



#RUTA PARA ELIMINAR UN USUARIO POR SU ID 
@router.delete("/eliminar_usuario/{id_usuario}", status_code=status.HTTP_201_CREATED, response_model=RetornoUsuario) #DECORADOR
def delete_user_by_id(id_usuario: int, db: Session = Depends(get_db),user_token: RetornoUsuario = Depends(get_current_user)):

    try:
        if user_token.id_rol != 1:
        # raise HTTPException(status_code=500, detail="No tienes permisos")
            raise HTTPException(status_code=403, detail="No tienes permisos")


        # return crud_users.get_user_by_id(db, id_usuario)
        result = crud_users.user_delete(db, id_usuario)
        if result :
            return {"message": "Usuario eliminado correctamente"}
            #return result
         
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    




#RUTA PARA ACTUALIZAR
@router.put("/editar/{user_id}")
def update_user(user_id: int, user: Editar_usuario, db: Session = Depends(get_db),user_token: RetornoUsuario = Depends(get_current_user)):
    try:
        if user_token.id_rol != 1:
        # raise HTTPException(status_code=500, detail="No tienes permisos")
            raise HTTPException(status_code=403, detail="No tienes permisos")



        success = crud_users.update_user(db, user_id, user)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")
        return {"message": "Usuario actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/editar-contrasenia")
def update_password(user: EditarPass, db: Session = Depends(get_db),user_token: RetornoUsuario = Depends(get_current_user)):
    try:
        if user_token.id_rol != 1:
        # raise HTTPException(status_code=500, detail="No tienes permisos")
            raise HTTPException(status_code=403, detail="No tienes permisos")


        verificar = crud_users.verify_user_pass(db, user)
        if not verificar:
            raise HTTPException(status_code=400, detail="La contraseña actual no es igual a la enviada")

        success = crud_users.update_password(db, user)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la contraseña del usuario")
        return {"message": "Contraseña actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    





@router.get("/obtener-todos}", status_code=status.HTTP_200_OK, response_model=List[RetornoUsuario])
def get_all(db: Session = Depends(get_db)):
    try:
        users = crud_users.get_all_user(db)
        if users is None:
            raise HTTPException(status_code=404, detail="Usuarios no encontrados")
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))