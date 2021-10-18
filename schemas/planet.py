from schemas.film import filmEntity
from config.db import conn
from bson import ObjectId

def planetEntity(item) -> dict:

    films = list()
    for film_id in item['films']:
        if ObjectId.is_valid(film_id):
            film_found = conn.film.find_one({'_id':ObjectId(film_id)})
            if(film_found):
                films.append(filmEntity(film_found))        

    return {
        'id':str(item['_id']),
        'name':item['name'],
        'climate':item['climate'],
        'diameter':item['diameter'],
        'population':item['population'],
        'films': films
    }

def planetsEntity(entity) -> list:
    return [planetEntity(item) for item in entity]
