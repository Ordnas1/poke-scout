from app.db import db
from tests.db_test_utils import load_test_db

BASE_URL = "/api/v1"


def test_get_single_pokemon(app, client):
    with app.app_context():
        load_test_db(db)

        resp = client.get("/api/v1/pokemon")

        assert resp.status_code == 200
