"""
Exposes query methods from the pokemon module, uses orm to fetch data
"""

from app.pokemon.models import (
    Location,
    LocationArea,
    Pokemon,
    pokemon_location_area_table,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select


class PokemonQueryService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def query_location_by_name(self, name):
        location_query = select(Location).where(Location.name == name)
        return self.db.session.execute(location_query).scalar()

    def create_location(self, data):
        location = Location(
            api_id=data["api_id"], name=data["name"], region=data["region"]
        )

        self.db.session.add(location)
        self.db.session.commit()
        return location

    def query_location_area_by_name(self, name):
        location_area_query = select(LocationArea).where(
            LocationArea.name == name
        )
        return self.db.session.execute(location_area_query).scalar()

    def create_location_area(self, data):
        location_area = LocationArea(
            api_id=data["api_id"],
            name=data["name"],
            location_id=data["location_id"],
        )

        self.db.session.add(location_area)
        self.db.session.commit()
        return location_area

    def query_pokemon_by_name(self, name):
        pokemon_query = select(Pokemon).where(Pokemon.name == name)
        return self.db.session.execute(pokemon_query).scalar()

    def create_pokemon(self, data):
        pokemon = Pokemon(
            api_id=data["api_id"],
            name=data["name"],
            height=data["height"],
            weight=data["weight"],
            sprite=data["sprite"],
            type_one=data["type_one"],
            type_two=data.get("type_two"),
        )
        self.db.session.add(pokemon)
        self.db.session.commit()
        return pokemon

    def insert_pokemon_id_location_area_ids(
        self, pokemon_id, location_area_ids
    ):
        self.db.session.execute(
            pokemon_location_area_table.insert().values(
                [
                    {"pokemon_id": pokemon_id, "location_area_id": la_id}
                    for la_id in location_area_ids
                ]
            )
        )
        self.db.session.commit()
        return pokemon_id

    def delete_all_data(self):
        try:
            rows_pokemon = self.db.session.query(Pokemon).delete()
            rows_location_area = self.db.session.query(LocationArea).delete()
            rows_location = self.db.session.query(Location).delete()
            rows_linked_table = self.db.session.query(
                pokemon_location_area_table
            ).delete()
            self.db.session.commit()
            return (
                rows_pokemon
                + rows_location_area
                + rows_location
                + rows_linked_table
            )
        except Exception:
            self.db.session.rollback()
