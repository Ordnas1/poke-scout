from flask import Blueprint, request

from . import controllers

pokemon_bp = Blueprint("pokemon", __name__)


@pokemon_bp.route("/pokemon", methods=["GET"])
def list_pokemons():
    if request.method == "GET":
        return controllers.list_all_pokemon_controller()
    return {"error": "Method not allowed"}, 405


@pokemon_bp.route("/pokemon/<id_or_name>", methods=["GET"])
def get_pokemon(id_or_name):
    if request.method == "GET":
        return controllers.get_pokemon(id_or_name)
    return {"error": "Method not allowed"}, 405


@pokemon_bp.route("/location_area", methods=["GET"])
def list_location_areas():
    if request.method == "GET":
        return controllers.list_all_location_areas()
    return {"error": "Method not allowed"}, 405


@pokemon_bp.route("/location_area/<id_or_name>", methods=["GET"])
def get_location_area(id_or_name):
    if request.method == "GET":
        return controllers.get_location_area(id_or_name)
    return {"error": "Method not allowed"}, 405
