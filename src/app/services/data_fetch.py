import aiohttp


BASE_URL = "https://pokeapi.co/api/v2/"


class PokeAPIService:
    def __init__(self):
        self.session = None

    async def fetch_pokemon(self, pokemon):
        async with self.session.get(f"{BASE_URL}pokemon/{pokemon}") as resp:
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
        async with self.session.get(url) as resp:
            data = await resp.json()
            shaped_data = {
                "api_id": data["id"],
                "name": data["name"],
                "region": data["region"]["name"],
            }
            return shaped_data


class PokeAPISessionManager:
    def __init__(self, poke_api_service: PokeAPIService):
        self.poke_api_service = poke_api_service

    async def __aenter__(self):
        self.poke_api_service.session = aiohttp.ClientSession()
        return self.poke_api_service

    async def __aexit__(self, exc_type, exc_val, traceback):
        await self.poke_api_service.session.close()
