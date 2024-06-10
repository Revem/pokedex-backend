from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal
from app.semaphore import with_semaphore

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def read_pokemons(skip: int = 0, limit: int = 151, db: Session = Depends(get_db), depends=[Depends(with_semaphore)]):
    pokemons = crud.get_pokemons(db, skip=skip, limit=limit)
    return pokemons

@router.get("/{pokemon_id}", response_model=schemas.Pokemon, dependencies=[Depends(with_semaphore)])
async def read_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon_by_id(db, pokemon_id=pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return JSONResponse(content=jsonable_encoder(db_pokemon))
