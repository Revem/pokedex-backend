from sqlalchemy import JSON, Column, Integer, String

from .database import Base


class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    types = Column(JSON)  # Lista de tipos do Pokémon
    description = Column(String)  # Descrição do Pokémon
    height = Column(Integer)  # Altura do Pokémon
    weight = Column(Integer)  # Peso do Pokémon
    species = Column(String)  # Categoria do Pokémon
    abilities = Column(JSON)  # Lista de habilidades do Pokémon
    gender_rate = Column(Integer)  # Taxa de gênero do Pokémon
    stats = Column(JSON)  # Estatísticas do Pokémon
    official_artwork = Column(String)  # URL da arte oficial do Pokémon