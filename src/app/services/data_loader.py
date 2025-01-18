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

from app import db, app


class PokeAPIDataLoader:
    pokemon_to_load = [
        "pikachu",
        "dhelmise",
        "charizard",
        "parasect",
        "aerodactyl",
        "kingler",
    ]
    query_service = PokemonQueryService(db)

    async def load_pokemon_data(self, pokemon_list=None):
        app.app.logger.info("Initializing pokemon data loading")
        if not pokemon_list:
            pokemon_list = self.pokemon_to_load
            
        async with PokeAPISessionManager(PokeAPIService()) as svc:
            for pokemon in pokemon_list:
                pokemon_in_db = self.query_service.query_pokemon_by_name(
                    pokemon
                )
                if pokemon_in_db:
                    app.app.logger.debug(
                        f"Pokemon {pokemon_in_db} already exists, skipping"
                    )
                    continue

                app.app.logger.debug(f"fetching data for {pokemon}")

                try:
                    pokemon_data = await svc.fetch_pokemon(pokemon)
                except Exception as e:
                    app.app.logger.warning(f"Exception {e}, skipping")
                    continue

                location_area_encounters_url = pokemon_data[
                    "location_area_encounters"
                ]
                app.app.logger.debug(
                    "fetching location area encounters data for {pokemon}"
                )
                location_area_encounters_list = (
                    await svc.fetch_location_area_urls_data(
                        location_area_encounters_url
                    )
                )
                location_area_ids = []
                if location_area_encounters_list:
                    app.app.logger.debug(
                        "list non-empty, fetching location area"
                    )
                    for data in location_area_encounters_list:

                        location_area_in_db = (
                            self.query_service.query_location_area_by_name(
                                data["name"]
                            )
                        )

                        if not location_area_in_db:
                            app.app.logger.debug("no location area in db")
                            app.app.logger.debug(
                                f"fetching data for {data['name']}"
                            )
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
                                app.app.logger.debug("no location in db")
                                app.app.logger.debug(
                                    f"fetching data for {location_area_data[
                                        'location_name'
                                    ]}"
                                )
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
                    app.app.logger.info(f"Pokemon {pokemon_in_db} loaded")

                else:
                    pokemon_in_db = self.query_service.create_pokemon(
                        pokemon_data
                    )
                    app.app.logger.info(f"Pokemon {pokemon_in_db} loaded")
