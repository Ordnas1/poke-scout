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


class PokeAPIDataLoader:
    pokemon_to_load = ["ditto", "charizard"]

    async def load_pokemon_data(self):
        async with PokeAPISessionManager(PokeAPIService()) as svc:

            for pokemon in self.pokemon_to_load:
                pokemon_data = await svc.fetch_pokemon(pokemon)
                location_area_encounters_url = pokemon_data[
                    "location_area_encounters"
                ]
                location_area_urls = await svc.fetch_location_area_urls(
                    location_area_encounters_url
                )
                print(pokemon_data, location_area_urls)

                if location_area_urls:
                    for url in location_area_urls:
                        location_area_data = await svc.fetch_location_area(url)
                        location_url = location_area_data["location_url"]
                        location_data = await svc.fetch_location(location_url)
                        print(location_area_data, location_data)
