from flask import Blueprint, request

from . import controllers

pokemon_bp = Blueprint("pokemon", __name__)


@pokemon_bp.route("/pokemon", methods=["GET"])
def list_pokemons():
    if request.method == "GET":
        return controllers.list_all_pokemon_controller()
    return "Method not allowed", 405
