from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app import crud, models, schemas
from app.database import SessionLocal
from app.utils import security

router = APIRouter()

@router.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: SessionLocal = Depends()):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    return crud.create_user(db, user) 
@router.post("/login/")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}
