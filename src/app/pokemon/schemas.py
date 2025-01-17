from marshmallow import fields
from app import ma
from .models import Pokemon, LocationArea, Location


class LocationAreaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationArea


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location


class PokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pokemon
        include_fk = True

    location_areas = fields.List(fields.Nested(LocationAreaSchema))


list_pokemon_schema = PokemonSchema(many=True)
