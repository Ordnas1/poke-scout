from app import db
from app.pokemon.models import Location, LocationArea, Pokemon


def test_location_model(app):
    with app.app_context():
        location = Location(id=1, api_id=1, name="dev-area", region="kanto")
        db.session.add(location)
        db.session.commit()

        assert db.session.query(Location).one()


def test_location_area_model(app):
    with app.app_context():
        location = Location(id=1, api_id=1, name="dev-area", region="kanto")
        db.session.add(location)
        db.session.commit()

        location_area = LocationArea(
            id=1, api_id=1, name="area-1", location_id=location.id
        )
        db.session.add(location_area)
        db.session.commit()

        assert db.session.query(LocationArea).one()


def test_pokemon_model(app):
    with app.app_context():
        pokemon = Pokemon(
            id=1,
            api_id=1,
            name="pikachu",
            height=0.4,
            weight=6.0,
            sprite="url",
            type_one="electric",
            type_two=None,
        )
        db.session.add(pokemon)
        db.session.commit()

        assert db.session.query(Pokemon).one()
