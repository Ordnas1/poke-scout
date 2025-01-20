from sqlalchemy import insert
from flask_sqlalchemy import SQLAlchemy
from app.pokemon.models import (
    Location,
    LocationArea,
    Pokemon,
    pokemon_location_area_table,
)


def load_test_db(db: SQLAlchemy):
    locations = [
        {"id": 1, "api_id": 1, "name": "dev-area", "region": "kanto"},
        {"id": 2, "api_id": 2, "name": "stage-area", "region": "johto"},
    ]

    location_areas = [
        {"id": 1, "api_id": 1, "name": "dev-area-north", "location_id": 1},
        {"id": 2, "api_id": 2, "name": "dev-area-south", "location_id": 1},
        {"id": 3, "api_id": 100, "name": "stage-area-north", "location_id": 2},
        {"id": 4, "api_id": 101, "name": "stage-area-south", "location_id": 2},
    ]

    pokemons = [
        {
            "id": 1,
            "api_id": 1,
            "name": "Poke_test_1",
            "height": 1,
            "weight": 1,
            "sprite": "example.com/sprite1",
            "type_one": "ghost",
            "type_two": "dark",
        },
        {
            "id": 2,
            "api_id": 100,
            "name": "Poke_test_2",
            "height": 1,
            "weight": 1,
            "sprite": "example.com/sprite2",
            "type_one": "ghost",
            "type_two": "dark",
        },
        {
            "id": 3,
            "api_id": 103,
            "name": "Poke_test_3",
            "height": 1,
            "weight": 1,
            "sprite": "example.com/sprite3",
            "type_one": "ghost",
            "type_two": "dark",
        },
        {
            "id": 4,
            "api_id": 151,
            "name": "Poke_test_4",
            "height": 1,
            "weight": 1,
            "sprite": "example.com/sprite4",
            "type_one": "ghost",
            "type_two": "dark",
        },
    ]
    pokemon_location_area_ids = [
        {"pokemon_id": 1, "location_area_id": 1},
        {"pokemon_id": 1, "location_area_id": 2},
        {"pokemon_id": 1, "location_area_id": 3},
        {"pokemon_id": 1, "location_area_id": 4},
        {"pokemon_id": 3, "location_area_id": 2},
        {"pokemon_id": 3, "location_area_id": 3},
        {"pokemon_id": 4, "location_area_id": 1},
        {"pokemon_id": 4, "location_area_id": 3},
        {"pokemon_id": 4, "location_area_id": 4},
    ]

    try:
        db.session.execute(insert(Location).values(locations))
        db.session.execute(insert(LocationArea).values(location_areas))
        db.session.execute(insert(Pokemon).values(pokemons))
        db.session.execute(
            insert(pokemon_location_area_table).values(
                pokemon_location_area_ids
            )
        )
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
