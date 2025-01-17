"""
The data_loader service is the central authority regarding the loading of
the data from the PokeAPI
It will coordinate the multiple phases of data loading, from fetching the data
from the API, sanitizing and loading it on the database
"""

from .data_fetch import (
    PokeAPISessionManager,
    PokeAPIService,
)

from .pokemon_query import PokemonQueryService

from app import db


class PokeAPIDataLoader:
    pokemon_to_load = ["ditto", "charizard"]
    query_service = PokemonQueryService(db)

    async def load_pokemon_data(self):
        async with PokeAPISessionManager(PokeAPIService()) as svc:
            for pokemon in self.pokemon_to_load:
                pokemon_in_db = self.query_service.query_pokemon_by_name(
                    pokemon
                )
                if pokemon_in_db:
                    return

                pokemon_data = await svc.fetch_pokemon(pokemon)
                location_area_encounters_url = pokemon_data[
                    "location_area_encounters"
                ]
                location_area_encounters_list = (
                    await svc.fetch_location_area_urls_data(
                        location_area_encounters_url
                    )
                )
                location_area_ids = []
                if location_area_encounters_list:
                    for data in location_area_encounters_list:

                        location_area_in_db = (
                            self.query_service.query_location_area_by_name(
                                data["name"]
                            )
                        )

                        if not location_area_in_db:
                            location_area_data = await svc.fetch_location_area(
                                data["url"]
                            )

                            location_url = location_area_data["location_url"]
                            location_in_db = (
                                self.query_service.query_location_by_name(
                                    location_area_data["location_name"]
                                )
                            )

                            if not location_in_db:
                                location_data = await svc.fetch_location(
                                    location_url
                                )
                                location_in_db = (
                                    self.query_service.create_location(
                                        location_data
                                    )
                                )

                            location_area_data["location_id"] = (
                                location_in_db.id
                            )
                            location_area_in_db = (
                                self.query_service.create_location_area(
                                    location_area_data
                                )
                            )
                        location_area_ids.append(location_area_in_db.id)

                    pokemon_in_db = self.query_service.create_pokemon(
                        pokemon_data
                    )
                    self.query_service.insert_pokemon_id_location_area_ids(
                        pokemon_in_db.id, location_area_ids
                    )
                    print(f"Pokemon {pokemon_in_db} loaded")

                else:
                    pokemon_in_db = self.query_service.create_pokemon(
                        pokemon_data
                    )
                    print(f"Pokemon {pokemon_in_db} loaded")
