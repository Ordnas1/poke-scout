"""Exposes query methods from the pokemon module, uses orm to fetch data
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
    """Service class for querying and manipulating
    Pokémon, Location, and LocationArea data.

    Attributes:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def query_location_by_name(self, name):
        """
        Queries a Location by its name.

        Args:
            name (str): The name of the location.

        Returns:
            Location: The Location object if found, else None.
        """
        location_query = select(Location).where(Location.name == name)
        return self.db.session.execute(location_query).scalar()

    def query_location_area_by_name(self, name):
        """
        Queries a LocationArea by its name.

        Args:
            name (str): The name of the location area.

        Returns:
            LocationArea: The LocationArea object if found, else None.
        """
        location_area_query = select(LocationArea).where(
            LocationArea.name == name
        )
        return self.db.session.execute(location_area_query).scalar()

    def query_pokemon_by_name(self, name):
        """
        Queries a Pokemon by its name.

        Args:
            name (str): The name of the Pokemon.

        Returns:
            Pokemon: The Pokemon object if found, else None.
        """
        pokemon_query = select(Pokemon).where(Pokemon.name == name)
        return self.db.session.execute(pokemon_query).scalar()

    def delete_all_data(self):
        """
        Deletes all data from the Pokemon, LocationArea,
        Location, and pokemon_location_area_table tables.

        Returns:
            int: The total number of rows deleted from all tables.
        """
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
        """
        Inserts multiple Location records into the database.

        Args:
            location_data_list (list): A list of dictionaries
            containing location data.
        """
        try:
            self.db.session.execute(insert(Location), location_data_list)
            self.db.session.commit()
        except Exception as e:
            print(e)
            self.db.session.rollback()

    def insert_bulk_location_areas(self, location_area_data_list):
        """
        Inserts multiple LocationArea records into the database.

        Args:
            location_area_data_list (list): A list of dictionaries
            containing location area data.
        """
        try:
            self.db.session.execute(
                insert(LocationArea), location_area_data_list
            )
            self.db.session.commit()
        except Exception as e:
            print(e)
            self.db.session.rollback()

    def insert_bulk_pokemons(self, pokemon_data_list):
        """
        Inserts multiple Pokemon records into the database.

        Args:
            pokemon_data_list (list):
            A list of dictionaries containing Pokemon data.
        """
        try:
            self.db.session.execute(insert(Pokemon), pokemon_data_list)
            self.db.session.commit()
        except Exception as e:
            print(e)
            self.db.session.rollback()

    def insert_bulk_pokemon_location_area_links(
        self, pokemon_location_area_links
    ):
        """
        Inserts multiple links between Pokemon and LocationArea
        records into the pokemon_location_area_table.

        Args:
            pokemon_location_area_links (list): A list of dictionaries
            containing Pokemon and LocationArea link data.
        """
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
        """
        Selects multiple Location records by their names.

        Args:
            location_name_list (list): A list of location names.

        Returns:
            list: A list of Location objects.
        """
        return (
            self.db.session.execute(
                select(Location).where(Location.name.in_(location_name_list))
            )
            .scalars()
            .all()
        )

    def select_bulk_location_areas_by_name(self, location_area_name_list):
        """
        Selects multiple LocationArea records by their names.

        Args:
            location_area_name_list (list): A list of location area names.

        Returns:
            list: A list of LocationArea objects.
        """
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
        """
        Selects multiple Pokemon records by their names.

        Args:
            pokemon_name_list (list): A list of Pokemon names.

        Returns:
            list: A list of Pokemon objects.
        """
        return (
            self.db.session.execute(
                select(Pokemon).where(Pokemon.name.in_(pokemon_name_list))
            )
            .scalars()
            .all()
        )
