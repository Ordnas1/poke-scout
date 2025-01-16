from flask import Blueprint
import asyncio

from .services.data_fetch import fetch_pokemon

appdatabp = Blueprint("appdata", __name__)


@appdatabp.cli.command("load_data")
def load_data():
    """Loads initial data"""
    
    asyncio.run(fetch_pokemon())
