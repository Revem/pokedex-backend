from sqlalchemy.orm import Session

from app import models, schemas

from .utils.security import get_password_hash, verify_password


def get_pokemons(db: Session, skip: int = 0,  limit: int = 20):
  return db.query(models.Pokemon).offset(skip).limit(limit).all()

def get_pokemon_by_id(db: Session, pokemon_id: int):
    return db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()

def get_user_by_username(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def create_user(user: schemas.UserCreate, db: Session):
  hashed_password = get_password_hash(user.password) 
  db_user = models.User(username=user.username, hashed_password=hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def authenticate_user(username: str, password: str, db: Session):
  user = get_user_by_username(db, username) 
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user

def search_pokemon(db: Session, query: str):
    return db.query(models.Pokemon).filter(
        (models.Pokemon.name.ilike(f"%{query}%")) |
        (models.Pokemon.id == query) 
    ).all()