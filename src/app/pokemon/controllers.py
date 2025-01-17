from sqlalchemy.orm import joinedload
from .models import Pokemon
from .schemas import list_pokemon_schema, single_pokemon_schema


def list_all_pokemon_controller():
    pokemons = Pokemon.query.options(joinedload(Pokemon.location_areas)).all()

    return list_pokemon_schema.dump(pokemons)


def get_pokemon(id_or_name):
    query = Pokemon.query.options(joinedload(Pokemon.location_areas))

    if id_or_name.isdigit():
        pokemon = query.filter_by(id=int(id_or_name)).first()
    else:
        pokemon = query.filter_by(name=id_or_name).first()

    if pokemon:
        return single_pokemon_schema.dump(pokemon)
    else:
        return {"error": "Pokemon not found"}, 404
