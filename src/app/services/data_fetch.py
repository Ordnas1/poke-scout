"""Data fetching services based on aiohttp

Classes:
PokeAPIService -- Services that fetches data from the PokeAPI
PokeAPISessionManager -- Handles Async Context Management for
                        the PokeAPIService
"""

import aiohttp
import asyncio

BASE_URL = "https://pokeapi.co/api/v2/"


class PokeAPIService:
    """Service that handles basic fetching operations

    Attributes:
    session - an aiohttp.ClientSession
    """

    def __init__(self):
        self.session = None

    async def fetch_pokemon(self, pokemon, session=None):
        """Fetches pokemon data from the PokeAPI and transforms it

        Args:
            pokemon: A pokemon name
            session: An aiohttp.ClientSession Defaults to None.

        Returns:
            shaped pokemon data
        """
        if not session:
            session = self.session

        async with session.get(f"{BASE_URL}pokemon/{pokemon}") as resp:
            data = await resp.json()

            try:
                type_two = data["types"][1]["type"]["name"]
            except IndexError:
                type_two = None

            shapedData = {
                "api_id": data["id"],
                "name": data["name"],
                "height": data["height"],
                "weight": data["weight"],
                "sprite": data["sprites"]["other"]["official-artwork"][
                    "front_default"
                ],
                "type_one": data["types"][0]["type"]["name"],
                "type_two": type_two,
                "location_area_encounters": data.get(
                    "location_area_encounters"
                ),
            }
            return shapedData

    async def fetch_location_area_urls_data(self, url):
        """Fetches location area name and url data
        from the PokeAPI and transforms it

        Args:
            url: a Location area url
        Returns:
            a list of urls and location areas name
        """
        async with self.session.get(url) as resp:
            data = await resp.json()
            shaped_data = [
                {
                    "url": la["location_area"]["url"],
                    "name": la["location_area"]["name"],
                }
                for la in data
            ]
            return shaped_data

    async def fetch_location_area(self, url):
        """Fetches location data and transforms it

        Args:
            url: location area url

        Returns:
            location area data
        """
        async with self.session.get(url) as resp:
            data = await resp.json()
            shaped_data = {
                "api_id": data["id"],
                "name": data["name"],
                "location_url": data["location"]["url"],
                "location_name": data["location"]["name"],
            }
            return shaped_data

    async def fetch_location(self, url):
        """fetches location data

        Args:
            url: a location url

        Returns:
            location data
        """
        async with self.session.get(url) as resp:
            data = await resp.json()
            shaped_data = {
                "api_id": data["id"],
                "name": data["name"],
                "region": data["region"]["name"],
            }
            return shaped_data

    def get_fetch_all_pokemon_coroutines(self, pokemon_list):
        """From a list of pokemons' names returns a list of coroutines
        to fetch pokemons

        Args:
            pokemon_list: a list of pokemon names

        Returns:
            a list of asyncio tasks
        """
        tasks = []

        for pokemon in pokemon_list:
            task = asyncio.create_task(self.fetch_pokemon(pokemon))
            tasks.append(task)

        return tasks

    async def get_pokemon_location_area_coroutines(self, pokemon, lae_url):
        """from a pokemon name and a url returns a list with
        that pokemon name and a task to fetch location data urls associated
        with that pokemon

        Args:
            pokemon : Pokemon name
            lae_url : Location area encounter name

        Returns:
            a list with a pokemon name and a coroutine
        """
        return [pokemon, await self.fetch_location_area_urls_data(lae_url)]

    def get_fetch_location_areas_mapping_coroutines(self, p_lae_map):
        """
        Creates a list of asyncio tasks for fetching location areas
        based on a mapping.

        Args:
            p_lae_map (dict): A dictionary mapping Pokémon IDs to
            location area encounter URLs.

        Returns:
            list: A list of asyncio tasks for fetching location areas.
        """
        tasks = []

        for pk, lae_url in p_lae_map.items():
            task = asyncio.create_task(
                self.get_pokemon_location_area_coroutines(pk, lae_url)
            )
            tasks.append(task)
        return tasks

    def get_fetch_location_area_coroutines(self, location_area_urls):
        """
        Creates a list of asyncio tasks for fetching location areas.

        Args:
            location_area_urls (list): A list of URLs for location areas.

        Returns:
            list: A list of asyncio tasks for fetching location areas.
        """
        tasks = []

        for url in location_area_urls:
            task = asyncio.create_task(self.fetch_location_area(url))
            tasks.append(task)
        return tasks

    def get_fetch_all_location_coroutines(self, location_list):
        """
        Creates a list of asyncio tasks for fetching locations.

        Args:
            location_list (list): A list of location names or IDs.

        Returns:
            list: A list of asyncio tasks for fetching locations.
        """
        tasks = []

        for location in location_list:
            task = asyncio.create_task(self.fetch_location(location))
            tasks.append(task)

        return tasks


class PokeAPISessionManager:
    """Async context manager for PokeApiService
    """
    def __init__(self, poke_api_service: PokeAPIService):
        self.poke_api_service = poke_api_service

    async def __aenter__(self):
        self.poke_api_service.session = aiohttp.ClientSession()
        return self.poke_api_service

    async def __aexit__(self, exc_type, exc_val, traceback):
        await self.poke_api_service.session.close()
