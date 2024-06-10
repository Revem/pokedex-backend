import xml.etree.ElementTree as ET

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def read_pokemons_as_xml(skip: int = 0, limit: int = 10000, db: Session = Depends(get_db)):
    pokemons = crud.get_pokemons(db, skip=skip, limit=limit)
    xml_content = generate_xml(pokemons)
    return Response(content=xml_content, media_type="application/xml")

@router.get("/{pokemon_id}")
async def read_pokemon_as_xml(pokemon_id: int, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon_by_id(db, pokemon_id=pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    xml_content = generate_xml([db_pokemon])
    return Response(content=xml_content, media_type="application/xml")

def generate_xml(pokemons):
    root = ET.Element("Pokemons")
    for pokemon in pokemons:
        pokemon_element = ET.SubElement(root, "Pokemon")
        ET.SubElement(pokemon_element, "id").text = str(pokemon.id)
        ET.SubElement(pokemon_element, "name").text = pokemon.name
        ET.SubElement(pokemon_element, "types").text = ",".join(pokemon.types)
        ET.SubElement(pokemon_element, "official_artwork").text = pokemon.official_artwork
    xml_content = ET.tostring(root, encoding="unicode")
    return xml_content

