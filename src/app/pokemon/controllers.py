from sqlalchemy.orm import joinedload
from .models import Pokemon, LocationArea
from .schemas import (
    list_pokemon_schema,
    single_pokemon_schema,
    list_location_areas_schema,
    single_location_area_schema,
)


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


def list_all_location_areas():
    locations = LocationArea.query.options(
        joinedload(LocationArea.pokemons)
    ).all()

    return list_location_areas_schema.dump(locations)


def get_location_area(id_or_name):
    query = LocationArea.query.options(joinedload(LocationArea.pokemons))

    if id_or_name.isdigit():
        location_area = query.filter_by(id=int(id_or_name)).first()
    else:
        location_area = query.filter_by(name=id_or_name).first()

    if location_area:
        return single_location_area_schema.dump(location_area)
    else:
        return {"error": "Pokemon not found"}, 404
