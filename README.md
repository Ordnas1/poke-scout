# Poke Scout

## Introduction
Poke-Scout is a web application that allows users to explore Pokémon data fetched from the PokeAPI. The application provides detailed information about Pokémon, their information and the locations in which they can be found.

## Installation
From the top of the project:
- create and activate a virtualenv (highly, highly recommended).
- run the `make install` command or `pip install -r requirements.txt`.

## Usage
### Database
The project uses SQLite3 as a database. Before using the app, we must configure it.
To load the db schemas and tables, run `make init-db` on the project root or `flask db upgrade`

### Data loader
The application needs to initially load the pokemon data before it can be effectively used. On the app folder you can use the following commands:

- `flask appdata load_data` will load the initial data for `Pikachu, Dhelmise, Charizard, Parasect, Aerodactyl and Kingler`.
- `flask appadata load_pokemon <pokemon>` will load the data for any `<pokemon` given any pokemon's name.
- `flask appdata drop_data` will delete all the data from the database.

You can also edit the `pokemon_to_load` list on the `PokeAPIDataLoader` class.

### Flask API
to serve the API, from the app folder run `flask run`, or run `make serve` from the project root.

## API Endpoints
### Pokémon Endpoints
- `GET /api/v1/pokemon`: List all Pokémon
- `GET /api/v1/pokemon/<id_or_name>`: Get details of a specific Pokémon by ID or name.

### Location Endpoints
- `GET /api/v1/locations`: List all locations
- `GET /api/v1/locations/<id_or_name>`: Get details of a specific location by ID or name.

## Testing
From the project root, run either `make test` or `coverage run -m pytest`. You can get a coverage report by running `coverage report`.