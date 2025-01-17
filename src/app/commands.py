from flask import Blueprint
import asyncio

from .services.data_loader import PokeAPIDataLoader

appdata_bp = Blueprint("appdata", __name__)


@appdata_bp.cli.command("load_data")
def load_data():
    """Loads initial data"""
    data_loader = PokeAPIDataLoader()

    asyncio.run(data_loader.load_pokemon_data())
