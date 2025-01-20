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
from sqlalchemy import select, insert


class PokemonQueryService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def query_location_by_name(self, name):
        location_query = select(Location).where(Location.name == name)
        return self.db.session.execute(location_query).scalar()

    def query_location_area_by_name(self, name):
        location_area_query = select(LocationArea).where(
            LocationArea.name == name
        )
        return self.db.session.execute(location_area_query).scalar()

    def query_pokemon_by_name(self, name):
        pokemon_query = select(Pokemon).where(Pokemon.name == name)
        return self.db.session.execute(pokemon_query).scalar()

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

    def insert_bulk_locations(self, location_data_list):
        try:
            self.db.session.execute(insert(Location), location_data_list)
            self.db.session.commit()
        except Exception as e:
            print(e)
            self.db.session.rollback()

    def insert_bulk_location_areas(self, location_area_data_list):
        try:
            self.db.session.execute(
                insert(LocationArea), location_area_data_list
            )
            self.db.session.commit()
        except Exception as e:
            print(e)
            self.db.session.rollback()

    def insert_bulk_pokemons(self, pokemon_data_list):
        try:
            self.db.session.execute(insert(Pokemon), pokemon_data_list)
            self.db.session.commit()
        except Exception as e:
            print(e)
            self.db.session.rollback()

    def insert_bulk_pokemon_location_area_links(
        self, pokemon_location_area_links
    ):
        try:
            self.db.session.execute(
                pokemon_location_area_table.insert(),
                pokemon_location_area_links,
            )
            self.db.session.commit()
        except Exception as e:
            print(e)
            self.db.session.rollback()

    def select_bulk_locations_by_name(self, location_name_list):
        return (
            self.db.session.execute(
                select(Location).where(Location.name.in_(location_name_list))
            )
            .scalars()
            .all()
        )

    def select_bulk_location_areas_by_name(self, location_area_name_list):
        return (
            self.db.session.execute(
                select(LocationArea).where(
                    LocationArea.name.in_(location_area_name_list)
                )
            )
            .scalars()
            .all()
        )

    def select_bulk_pokemons_by_name(self, pokemon_name_list):
        return (
            self.db.session.execute(
                select(Pokemon).where(Pokemon.name.in_(pokemon_name_list))
            )
            .scalars()
            .all()
        )
