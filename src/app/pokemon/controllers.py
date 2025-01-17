from sqlalchemy.orm import joinedload
from .models import Pokemon
from .schemas import list_pokemon_schema


def list_all_pokemon_controller():
    pokemons = Pokemon.query.options(joinedload(Pokemon.location_areas)).all()
            
    return list_pokemon_schema.dump(pokemons)
