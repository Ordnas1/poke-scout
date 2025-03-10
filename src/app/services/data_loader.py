"""
The data_loader service is the central authority regarding the loading of
the data from the PokeAPI
It will coordinate the multiple phases of data loading, from fetching the data
from the API, sanitizing and loading it on the database
"""

import itertools
import asyncio
from .data_fetch import (
    PokeAPISessionManager,
    PokeAPIService,
)

from .pokemon_query import PokemonQueryService

from app import db


class PokeAPIDataLoader:
    # if you wish to load other pokemons, you can also edit this list
    pokemon_to_load = [
        "pikachu",
        "dhelmise",
        "charizard",
        "parasect",
        "terodactyl",
        "kingler",
    ]

    query_service = PokemonQueryService(db)

    async def load_pokemon_data_concurrent(self, pokemon_list=None):
        """Loads pokemon into database using PokeApiService and
        PokemonQueryService

        Args:
            pokemon_list (_type_, optional): a list of pokemon names. Defaults
            to None.
        """
        # 1. for each pokemon in pokemon list, if not on db
        # already gather all pk and then fetch all data.
        # 2. create a pokemon:area location name map by fetching the
        # location_area_encounters
        # 3. for each location_area, check if they're not in db already
        # then gather and fetch all
        # 4. create a la:l mapinf
        # 5. for each area, check if exists on db
        # 6. fetch all areas
        # 7. add all location to db
        # 8. add all location areas to db, use mapping to locate
        # 9. add all pokemons to db, use mapping to populate crosstable
        if not pokemon_list:
            pokemon_list = self.pokemon_to_load

        async with PokeAPISessionManager(PokeAPIService()) as svc:
            pokemon_to_fetch = []
            for pokemon in pokemon_list:
                pokemon_in_db = self.query_service.query_pokemon_by_name(
                    pokemon
                )
                if pokemon_in_db:
                    print(f"{pokemon} in db. skipping")
                    continue
                else:
                    pokemon_to_fetch.append(pokemon)

            pokemon_data = [
                p
                for p in await asyncio.gather(
                    *svc.get_fetch_all_pokemon_coroutines(pokemon_to_fetch),
                    return_exceptions=True,
                )
                if not isinstance(p, Exception)
            ]

            pokemon_la_map = {
                p["name"]: p["location_area_encounters"] for p in pokemon_data
            }

            pokemon_location_area_list = await asyncio.gather(
                *svc.get_fetch_location_areas_mapping_coroutines(
                    pokemon_la_map
                ),
                return_exceptions=True,
            )

            location_area_url_list = list(
                itertools.chain(*[p[1] for p in pokemon_location_area_list])
            )

            location_area_to_fetch = []
            la_l_map = None
            for la in location_area_url_list:
                location_area_in_db = (
                    self.query_service.query_location_area_by_name(la["name"])
                )
                if not location_area_in_db:
                    location_area_to_fetch.append(la["url"])
            if location_area_to_fetch:
                location_area_data = await asyncio.gather(
                    *svc.get_fetch_location_area_coroutines(
                        list(set(location_area_to_fetch))
                    ),
                    return_exceptions=True,
                )

                la_l_map = {
                    la["name"]: la["location_name"]
                    for la in location_area_data
                }

                location_name_url_list = [
                    {"name": la["location_name"], "url": la["location_url"]}
                    for la in location_area_data
                ]

                location_to_fetch = []
                for loc in location_name_url_list:
                    location_in_db = self.query_service.query_location_by_name(
                        loc["name"]
                    )
                    if not location_in_db:
                        location_to_fetch.append(loc["url"])

                if location_to_fetch:
                    location_data = await asyncio.gather(
                        *svc.get_fetch_all_location_coroutines(
                            list(set(location_to_fetch))
                        ),
                        return_exceptions=True,
                    )

                    self.query_service.insert_bulk_locations(location_data)

                queried_locations = {
                    loc.name: loc.id
                    for loc in self.query_service.select_bulk_locations_by_name(
                        la_l_map.values()
                    )
                }

                location_area_location_id_map = {
                    key: queried_locations.get(value)
                    for key, value in la_l_map.items()
                }

                location_area_data = [
                    dict(
                        item,
                        location_id=location_area_location_id_map.get(
                            item["name"]
                        ),
                    )
                    for item in location_area_data
                ]

                self.query_service.insert_bulk_location_areas(
                    location_area_data
                )

                pokemon_location_areas_id_mapping = {
                    elem[0]: [loc_area["name"] for loc_area in elem[1]]
                    for elem in pokemon_location_area_list
                }

                queried_location_areas = {
                    la.name: la.id
                    for la in self.query_service.select_bulk_location_areas_by_name(
                        list(
                            itertools.chain(
                                *pokemon_location_areas_id_mapping.values()
                            )
                        )
                    )
                }

                pokemon_location_areas_id_mapping = {
                    key: list(
                        set(
                            [
                                queried_location_areas.get(value)
                                for value in values
                            ]
                        )
                    )
                    for key, values in pokemon_location_areas_id_mapping.items()
                }

                self.query_service.insert_bulk_pokemons(pokemon_data)
                pokemon_names = [p["name"] for p in pokemon_data]
                pokemon_id_location_area_id_mapping = {
                    p.id: pokemon_location_areas_id_mapping.get(p.name)
                    for p in self.query_service.select_bulk_pokemons_by_name(
                        pokemon_names
                    )
                }

                pokemon_id_location_area_id_objects = [
                    {"pokemon_id": key, "location_area_id": value}
                    for key, values in pokemon_id_location_area_id_mapping.items()
                    for value in values
                ]

                self.query_service.insert_bulk_pokemon_location_area_links(
                    pokemon_id_location_area_id_objects
                )

            else:
                pass
