import requests
import datetime
from fastapi import HTTPException

def format_name(name):
    name = name.strip()
    name = name.lower()
    name = name.title()
    return name

#check the starwars api for a planet with the same name and return all the planet data for the insert
def get_planet_from_swapi(planet_name):
    planet_name = format_name(planet_name)
    api = f'https://swapi.dev/api/planets/?search={planet_name}'
    result = requests.get(api)
    result = result.json()
    if result['count'] == 1:
        return result['results'][0]
    return False


#check the starwars api for the film with the same name and return all the film data for the insert
def get_film_from_swapi(film_name):
    film_name = format_name(film_name)
    api = f'https://swapi.dev/api/films/?search={film_name}'
    result = requests.get(api)
    result = result.json()
    if result['count'] == 1:
        return result['results'][0]
    return False

#check if the release_date is a valid and real date
def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=422, detail='Error: Invalid Date')

