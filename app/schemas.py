from typing import List

from pydantic import BaseModel


class Pokemon(BaseModel):
  id: int
  name: str
  type: str

  class Config:
    orm_mode = True

class PokemonList(BaseModel):
  count: int
  pokemons: List[Pokemon]

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True