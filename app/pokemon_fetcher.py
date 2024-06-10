import asyncio

import httpx
from sqlalchemy.orm import Session

from . import models


async def fetch_pokemon_data(client, url):
    response = await client.get(url)
    response.raise_for_status()
    data = response.json()

    types = [t["type"]["name"] for t in data["types"]]
    abilities = [a["ability"]["name"] for a in data["abilities"]]
    species_url = data["species"]["url"]

    species_response = await client.get(species_url)
    species_response.raise_for_status()
    species_data = species_response.json()

    description = next((flavor_text["flavor_text"] for flavor_text in species_data["flavor_text_entries"] if flavor_text["language"]["name"] == "en"), "")

    official_artwork_url = data["sprites"]["other"]["official-artwork"]["front_default"] if "official-artwork" in data["sprites"]["other"] else None
    gender_rate = data.get("gender_rate", None)

    return {
        "id": data["id"],
        "name": data["name"],
        "types": types,
        "description": description,
        "height": data["height"],
        "weight": data["weight"],
        #"species": species_data["genera"][0]["genus"],
        "abilities": abilities,
        "gender_rate": gender_rate,
        "official_artwork": official_artwork_url,
        "stats": data["stats"],
    }


def get_pokemon_by_id(db: Session, pokemon_id: int):
    return db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()

async def fetch_all_pokemons(db: Session):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://pokeapi.co/api/v2/pokemon?limit=10000")
        response.raise_for_status()
        data = response.json()
        results = data["results"]

        tasks = []
        for result in results:
            tasks.append(fetch_pokemon_data(client, result["url"]))

        pokemons_data = await asyncio.gather(*tasks)

        for pokemon_data in pokemons_data:
            if not get_pokemon_by_id(db, pokemon_data["id"]):
                db.add(models.Pokemon(**pokemon_data))
        db.commit()
