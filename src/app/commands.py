import click
import asyncio
from flask import Blueprint

from .services.data_loader import PokeAPIDataLoader
from .services.pokemon_query import PokemonQueryService
from app import db

appdata_bp = Blueprint("appdata", __name__)


@appdata_bp.cli.command("load_data")
def load_data():
    """Load data from the default list
    Pikachu, Dhelmise, Charizard, Parasect, Aerodactyl and Kingler"""
    data_loader = PokeAPIDataLoader()

    asyncio.run(data_loader.load_pokemon_data_concurrent())


@appdata_bp.cli.command("drop_data")
def drop_data():
    """Clears all the data from the database"""
    query_svc = PokemonQueryService(db)
    total_deleted = query_svc.delete_all_data()
    print(f"{total_deleted} rows deleted")


@appdata_bp.cli.command("load_pokemon")
@click.argument("pokemon")
def load_pokemon(pokemon):
    """Load a single pokemon by name"""
    data_loader = PokeAPIDataLoader()

    asyncio.run(data_loader.load_pokemon_data_concurrent([pokemon]))
