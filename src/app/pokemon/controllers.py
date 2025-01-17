from sqlalchemy.orm import joinedload
from .models import Pokemon


def list_all_pokemon_controller():
    pokemon = Pokemon.query.options(joinedload(Pokemon.location_area)).all()
    