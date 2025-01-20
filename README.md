# Poke Scout

## Introduction
Poke-Scout is a web application that allows users to explore Pokémon data fetched from the PokeAPI. The application provides detailed information about Pokémon, their information and the locations in which they can be found.

## Installation
From the top of the project run the `make install` command or `pip install -r requirements.txt`

## Usage
### Data loader
The application needs to initially load the pokemon data before it can be effectively used. On the app folder you can use the following commands

- `flask appdata load_data` will load the initial data for `Pikachu, Dhelmise, Charizard, Parasect, Aerodactyl and Kingler`
- `flask appadata load_pokemon <pokemon>` will load the data for any `<pokemon` given any pokemon's name
- `flask appdata drop_data` will delete all the data from the database

## API Endpoints
### Pokémon Endpoints
- `GET /api/v1/pokemon`: List all Pokémon
- `GET /api/v1/pokemon/<id_or_name>`: Get details of a specific Pokémon by ID or name

### Location Endpoints
- `GET /api/v1/locations`: List all locations
- `GET /api/v1/locations/<id_or_name>`: Get details of a specific location by ID or name


