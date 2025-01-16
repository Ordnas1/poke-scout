import aiohttp


BASE_URL = "https://pokeapi.co/api/v2/"


async def fetch_pokemon(pokemon):
    async with aiohttp.ClientSession(BASE_URL) as session:
        async with session.get(f"pokemon/{pokemon}") as resp:
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


async def fetch_location_area_urls(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            shaped_data = [la["location_area"]["url"] for la in data]
            return shaped_data


async def fetch_location_area(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            shaped_data = {
                "api_id": data["id"],
                "name": data["name"],
                "location_url": data["location"]["url"],
            }
            return shaped_data
        

async def fetch_location(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            shaped_data = {
                "api_id": data["id"],
                "name": data["name"],
                "region": data["region"]["name"],
            }
            return shaped_data
