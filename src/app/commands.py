import click
import asyncio
from flask import Blueprint

from .services.data_loader import PokeAPIDataLoader
from .services.pokemon_query import PokemonQueryService
from app import app, db

appdata_bp = Blueprint("appdata", __name__)


@appdata_bp.cli.command("load_data")
def load_data():
    """Loads initial data"""
    data_loader = PokeAPIDataLoader()

    asyncio.run(data_loader.load_pokemon_data())


@appdata_bp.cli.command("drop_data")
def drop_data():
    """Clears all the data from the database"""
    query_svc = PokemonQueryService(db)
    total_deleted = query_svc.delete_all_data()
    app.app.logger.info(f"Deleted {total_deleted} records")


@appdata_bp.cli.command("load_pokemon")
@click.argument("pokemon")
def load_pokemon(pokemon):
    """Load a single pokemon"""
    data_loader = PokeAPIDataLoader()

    asyncio.run(data_loader.load_pokemon_data([pokemon]))


@appdata_bp.cli.command("load_data_concurrent")
def load_data_concurrent():
    """Loads initial data concurrent"""
    data_loader = PokeAPIDataLoader()

    asyncio.run(data_loader.load_pokemon_data_concurrent())
