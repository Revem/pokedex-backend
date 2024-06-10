import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal, get_db

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/search", response_model=List[schemas.Pokemon])
def search_pokemon(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    logging.info(f"Searching for pokemons with query: {query}")
    pokemons = crud.search_pokemon(db, query=query)
    if not pokemons:
        logging.error("No pokemons found")
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return pokemons