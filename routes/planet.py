from fastapi import APIRouter, HTTPException
from config.db import conn
from models.planet import Planet
from schemas.planet import planetEntity, planetsEntity
from bson import ObjectId
import requests
from config.utils import get_planet_from_swapi, get_film_from_swapi, format_name

planet = APIRouter()

#root - show all planets in the database
@planet.get('/')
async def get_all_planets():
    return planetsEntity(conn.planet.find())

#show an especific planet from the database by the id
@planet.get('/{id}')
async def get_one_planet(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Error: Invalid ID')
    selected_planet = conn.planet.find_one({'_id':ObjectId(id)})
    if not selected_planet:
        raise HTTPException(status_code=404, detail='Error: Planet not found')
    return planetEntity(selected_planet)


#insert a planet
@planet.post('/')
async def add_planet(planet: Planet):
    new_planet = dict(planet)
    new_planet['name'] = format_name(new_planet['name'])
    if(len(new_planet['name']) == 0):
        raise HTTPException(status_code=422, detail='Error: Invalid Name')

    #searching for the planet in the starwars api, if the planet is found then insert the api planet in the local database
    from_api = 0
    planet_from_swapi = get_planet_from_swapi(new_planet['name'])
    if planet_from_swapi != False:
        new_planet['name'] = planet_from_swapi['name']
        new_planet['climate'] = planet_from_swapi['climate']
        new_planet['diameter'] = int(planet_from_swapi['diameter'])
        new_planet['population'] = planet_from_swapi['population']
        new_planet['films'] = planet_from_swapi['films']
        from_api = 1

    #checking if the planet is already in the database and get the id, if not then insert
    planet_found = conn.planet.find_one({'name' : new_planet['name']})
    if(planet_found):
        raise HTTPException(status_code=400, detail='Error: Planet already in database')

    #inserting/checking the films in the database and making the relations with the _id
    films = list()
    for film_name in new_planet['films']:

        if(from_api == 1):
            #from_api means the film_name is actually a url from the starwars api
            film_api = requests.get(film_name)
            film_api = film_api.json()
            film_name = film_api['title']
            release_date = film_api['release_date']
        else:
            film_name = format_name(film_name)
            #checking if the film is in the starwars api if it is then get the title and date
            film_from_swapi = get_film_from_swapi(film_name)
            if film_from_swapi != False:
                film_name = film_from_swapi['title']
                release_date = film_from_swapi['release_date']
            else:
                release_date = ''

        #checking if the film is already in the database and get the id, if not then insert
        film_found = conn.film.find_one({'name' : film_name})
        if(film_found):
            films.append(str(film_found['_id']))
        else:
            new_film = conn.film.insert_one({'name':film_name, 'release_date':release_date})
            films.append(str(new_film.inserted_id))


    new_planet['films'] = films        

    id = conn.planet.insert_one(new_planet)
    return planetEntity(conn.planet.find_one({'_id':ObjectId(id.inserted_id)}))


#update a planet
@planet.put('/{id}')
async def update_planet(id: str, planet: Planet):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Error: Invalid ID')

    new_planet_data = dict(planet)
    new_planet_data['name'] = format_name(new_planet_data['name'])
    if(len(new_planet_data['name']) == 0):
        raise HTTPException(status_code=422, detail='Error: Invalid Name')

    #checking if the planet is already in the database and get the id, if not then insert
    planet_found = conn.planet.find_one({'name' : new_planet_data['name'], '_id': {'$ne' : ObjectId(id)}})
    if(planet_found):
        raise HTTPException(status_code=400, detail='Error: Planet already in database')

    films = list()
    for film_name in new_planet_data['films']:
        film_name = format_name(film_name)

        #checking if the film is in the starwars api if it is then get the title and date
        film_from_swapi = get_film_from_swapi(film_name)
        if film_from_swapi != False:
            film_name = film_from_swapi['title']
            release_date = film_from_swapi['release_date']
        else:
            release_date = ''

        #checking if the film is already in the database and get the id, if not then insert
        film_found = conn.film.find_one({'name' : film_name})
        if(film_found):
            films.append(str(film_found['_id']))
        else:
            new_film = conn.film.insert_one({'name':film_name, 'release_date':release_date})
            films.append(str(new_film.inserted_id))

    new_planet_data['films'] = films

    updated_planet = conn.planet.find_one_and_update({'_id':ObjectId(id)},{'$set':new_planet_data})
    if not updated_planet:
        raise HTTPException(status_code=404, detail='Error: Planet not found or could not be updated')
    return planetEntity(conn.planet.find_one({'_id':ObjectId(id)}))

#delete a planet
@planet.delete('/{id}')
async def delete_planet(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Error: Invalid ID')
    deleted_planet = conn.planet.find_one_and_delete({'_id':ObjectId(id)})
    if not deleted_planet:
        raise HTTPException(status_code=404, detail='Error: Planet not found')
    return planetEntity(deleted_planet)