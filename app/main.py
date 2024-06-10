import asyncio

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.v1.endpoints import health, pokemon, pokemons, users
from app.database import Base, SessionLocal, engine, get_db

from . import models, pokemon_fetcher

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
  db = SessionLocal()
  await pokemon_fetcher.fetch_all_pokemons(db)
  db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pokemon.router, prefix="/v1/pokemon", tags=["pokemons"])
app.include_router(pokemons.router, prefix="/v1/pokemons", tags=["pokemons"])
app.include_router(health.router, prefix="/v1/health", tags=["health"])
app.include_router(users.router, prefix="/v1/users", tags=["users"])