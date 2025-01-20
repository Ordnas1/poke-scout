"""Here we save api versions and register the corresponding blueprints"""
from flask import Blueprint
from .pokemon.urls import pokemon_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api_v1_bp.register_blueprint(pokemon_bp)
