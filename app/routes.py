from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, utils
from pydantic import BaseModel

# Definir el router
router = APIRouter()

# Esquema de Pydantic para el cuerpo de la solicitud al crear o actualizar un usuario
class UserCreate(BaseModel):
    full_name: str
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    full_name: str
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: str

    class Config:
        orm_mode = True

# Endpoint para crear un nuevo usuario
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(database.get_db)):
    # Verificar si el usuario o el email ya existen
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear el nuevo usuario con la contraseña encriptada
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Endpoint para obtener los detalles de un usuario por ID
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Endpoint para actualizar un usuario
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Actualizar los campos
    db_user.full_name = user.full_name
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

# Endpoint para eliminar un usuario
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
