from app import db
from app.pokemon.models import Location


def test_location_model(app):
    with app.app_context():
        location = Location(id=1, api_id=1, name="dev-area", region="kanto")
        db.session.add(location)
        db.session.commit()

        assert db.session.query(Location).one()
