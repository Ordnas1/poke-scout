import pytest
from app import create_app, db
from app.services.pokemon_query import PokemonQueryService


@pytest.fixture()
def app():
    app = create_app("testing")

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def pokemon_query():
    return PokemonQueryService(db)