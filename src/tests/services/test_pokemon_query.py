from tests.db_test_utils import load_test_db
from app.db import db
from app.pokemon.models import (
    Pokemon,
    Location,
    LocationArea,
    pokemon_location_area_table,
)


def test_query_location_by_name(app, pokemon_query):
    with app.app_context():
        load_test_db(db)
        location = pokemon_query.query_location_by_name("dev-area")

    assert location.name == "dev-area"


def test_query_location_area_by_name(app, pokemon_query):
    with app.app_context():
        load_test_db(db)
        location = pokemon_query.query_location_area_by_name("dev-area-north")

    assert location.name == "dev-area-north"


def test_query_pokemon_by_name(app, pokemon_query):
    with app.app_context():
        load_test_db(db)
        location = pokemon_query.query_pokemon_by_name("Poke_test_1")

    assert location.name == "Poke_test_1"


def test_delete_all_data(app, pokemon_query):
    with app.app_context():
        load_test_db(db)

        assert db.session.query(Pokemon).count() != 0
        assert db.session.query(LocationArea).count() != 0
        assert db.session.query(Location).count() != 0
        assert db.session.query(pokemon_location_area_table).count() != 0

        pokemon_query.delete_all_data()

        assert db.session.query(Pokemon).count() == 0
        assert db.session.query(LocationArea).count() == 0
        assert db.session.query(Location).count() == 0
        assert db.session.query(pokemon_location_area_table).count() == 0


def test_insert_bulk_locations(app, pokemon_query):
    location_data = [
        {"api_id": 1, "name": "dev-area", "region": "kanto"},
        {"api_id": 2, "name": "stage-area", "region": "johto"},
    ]

    with app.app_context():
        pokemon_query.insert_bulk_locations(location_data)

        assert db.session.query(Location).count() == 2


def test_insert_bulk_location_areas(app, pokemon_query):
    location_areas_data = [
        {"id": 1, "api_id": 1, "name": "dev-area-north", "location_id": 1},
        {"id": 2, "api_id": 2, "name": "dev-area-south", "location_id": 1},
        {"id": 3, "api_id": 100, "name": "stage-area-south", "location_id": 2},
        {"id": 4, "api_id": 101, "name": "stage-area-south", "location_id": 2},
    ]

    with app.app_context():
        pokemon_query.insert_bulk_location_areas(location_areas_data)

        assert db.session.query(LocationArea).count() == 4


def test_insert_bulk_pokemons(app, pokemon_query):
    pokemon_data = [
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
    ]

    with app.app_context():
        pokemon_query.insert_bulk_pokemons(pokemon_data)
        assert db.session.query(Pokemon).count() == 3


def test_insert_bulk_pokemon_location_area_links(app, pokemon_query):
    with app.app_context():
        pokemon_location_area_links = [
            {"pokemon_id": 1, "location_area_id": 1},
            {"pokemon_id": 2, "location_area_id": 2},
        ]
        pokemon_query.insert_bulk_pokemon_location_area_links(
            pokemon_location_area_links
        )
        links = db.session.query(pokemon_location_area_table).all()
        assert len(links) == 2
        assert links[0].pokemon_id == 1
        assert links[0].location_area_id == 1
        assert links[1].pokemon_id == 2
        assert links[1].location_area_id == 2


def test_select_bulk_locations_by_name(app, pokemon_query):
    locations_names = ["dev-area", "stage-area"]

    with app.app_context():
        load_test_db(db)
        loc_list = pokemon_query.select_bulk_locations_by_name(locations_names)

        assert len(loc_list) == 2
        assert loc_list[0].name == "dev-area"


def test_select_bulk_location_areas_by_name(app, pokemon_query):
    location_areas = ["dev-area-north", "stage-area-south"]

    with app.app_context():
        load_test_db(db)
        loc_list = pokemon_query.select_bulk_location_areas_by_name(
            location_areas
        )

        assert len(loc_list) == 2
        assert loc_list[0].name == "dev-area-north"


def test_select_bulk_pokemons_by_name(app, pokemon_query):
    pokemon_list = ["Poke_test_3", "Poke_test_1"]

    with app.app_context():
        load_test_db(db)
        loc_list = pokemon_query.select_bulk_pokemons_by_name(pokemon_list)

        assert len(loc_list) == 2
        assert loc_list[0].name == "Poke_test_1"
