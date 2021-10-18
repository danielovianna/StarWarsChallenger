from fastapi import APIRouter, HTTPException
from config.db import conn
from models.film import Film
from schemas.film import filmEntity, filmsEntity
from bson import ObjectId
from config.utils import format_name, validate_date, get_film_from_swapi, format_name

film = APIRouter()

#root - show all films in the database
@film.get('/')
async def get_all_films():
    return filmsEntity(conn.film.find())

#show an especific film from the database by the id
@film.get('/{id}')
async def get_one_film(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Error: Invalid ID')
    selected_film = conn.film.find_one({'_id':ObjectId(id)})
    if not selected_film:
        raise HTTPException(status_code=404, detail='Error: Film not found')
    return filmEntity(selected_film)

#insert a film
@film.post('/')
async def add_film(film: Film):
    new_film = dict(film)
    new_film['name'] = format_name(new_film['name'])
    if(len(new_film['name']) == 0):
        raise HTTPException(status_code=422, detail='Error: Invalid Name')

    #searching for the film in the starwars api, if the film is found then insert the api film in the local database
    film_from_swapi = get_film_from_swapi(new_film['name'])
    if film_from_swapi != False:
        new_film['name'] = film_from_swapi['title']
        new_film['release_date'] = film_from_swapi['release_date']
    else:
        if(new_film['release_date'] != ''):
            validate_date(new_film['release_date']) #checking if the release_date is a valid date

    #checking if the film is already in the database
    film_found = conn.film.find_one({'name' : new_film['name']})
    if(film_found):
        raise HTTPException(status_code=400, detail='Error: Film already in database')
    
    #inserting the film in the database
    id = conn.film.insert_one(new_film)
    return filmEntity(conn.film.find_one({'_id':ObjectId(id.inserted_id)}))

#update a film
@film.put('/{id}')
async def update_film(id: str, film: Film):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Error: Invalid ID')

    new_film_data = dict(film)
    new_film_data['name'] = format_name(new_film_data['name'])
    if(len(new_film_data['name']) == 0):
        raise HTTPException(status_code=422, detail='Error: Invalid Name')

    #checking if the film is already in the database
    film_found = conn.film.find_one({'name' : new_film_data['name'], '_id': {'$ne' : ObjectId(id)}})
    if(film_found):
        raise HTTPException(status_code=400, detail='Error: Film already in database')

    if(new_film_data['release_date'] != ''):
        validate_date(new_film_data['release_date'])

    updated_film = conn.film.find_one_and_update({'_id':ObjectId(id)},{'$set':new_film_data})
    if not updated_film:
        raise HTTPException(status_code=404, detail='Error: Film not found or could not be updated')
    return filmEntity(conn.film.find_one({'_id':ObjectId(id)}))

#delete a film
@film.delete('/{id}')
async def delete_film(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Error: Invalid ID')
    deleted_film = conn.film.find_one_and_delete({'_id':ObjectId(id)})
    if not deleted_film:
        raise HTTPException(status_code=404, detail='Error: Film not found')

    #deleting the relationships in planet collection
    conn.planet.update_many({ }, { '$pull': {'films': id }})
    return filmEntity(deleted_film)