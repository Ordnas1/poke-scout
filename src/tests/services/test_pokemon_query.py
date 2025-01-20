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
