import aiohttp


BASE_URL = "https://pokeapi.co/api/v2/"


async def fetch_pokemon():
    async with aiohttp.ClientSession(BASE_URL) as session:
        async with session.get("pokemon/ditto") as resp:
            print(resp.status)
            print(await resp.json())
