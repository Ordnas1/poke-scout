from app.db import db
from tests.db_test_utils import load_test_db

BASE_URL = "/api/v1"


def test_get_single_pokemon(app, client):
    with app.app_context():
        load_test_db(db)

    resp = client.get(f"{BASE_URL}/pokemon/1")

    assert resp.status_code == 200
    assert resp.json == {
        "api_id": 1,
        "height": 1.0,
        "id": 1,
        "location_areas": [
            {"api_id": 1, "id": 1, "name": "dev-area-north"},
            {"api_id": 2, "id": 2, "name": "dev-area-south"},
            {"api_id": 100, "id": 3, "name": "stage-area-north"},
            {"api_id": 101, "id": 4, "name": "stage-area-south"},
        ],
        "name": "Poke_test_1",
        "sprite": "example.com/sprite1",
        "type_one": "ghost",
        "type_two": "dark",
        "weight": 1.0,
    }


def test_get_all_pokemon(app, client):
    with app.app_context():
        load_test_db(db)

    resp = client.get(f"{BASE_URL}/pokemon")

    assert resp.status_code == 200
    assert len(resp.json) == 4


def test_get_single_location_area(app, client):
    with app.app_context():
        load_test_db(db)

    resp = client.get(f"{BASE_URL}/location_area/1")
    assert resp.status_code == 200
    assert resp.json == {
        "api_id": 1,
        "id": 1,
        "name": "dev-area-north",
        "pokemons": [
            {
                "api_id": 1,
                "height": 1.0,
                "id": 1,
                "name": "Poke_test_1",
                "sprite": "example.com/sprite1",
                "type_one": "ghost",
                "type_two": "dark",
                "weight": 1.0,
            },
            {
                "api_id": 151,
                "height": 1.0,
                "id": 4,
                "name": "Poke_test_4",
                "sprite": "example.com/sprite4",
                "type_one": "ghost",
                "type_two": "dark",
                "weight": 1.0,
            },
        ],
    }


def test_get_all_location_areas(app, client):
    with app.app_context():
        load_test_db(db)

    resp = client.get(f"{BASE_URL}/location_area")

    assert resp.status_code == 200
    assert len(resp.json) == 4
