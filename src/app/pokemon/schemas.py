from marshmallow import fields
from app import ma
from .models import Pokemon, LocationArea, Location


class LocationAreaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationArea

    pokemons = fields.List(
        fields.Nested(lambda: PokemonSchema(exclude=("location_areas",)))
    )


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location


class PokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pokemon
        include_fk = True

    location_areas = fields.List(fields.Nested(LocationAreaSchema))


list_pokemon_schema = PokemonSchema(many=True)
single_pokemon_schema = PokemonSchema()

list_location_areas_schema = LocationAreaSchema(many=True)
single_location_area_schema = LocationAreaSchema()
