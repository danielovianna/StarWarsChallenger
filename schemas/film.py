def filmEntity(item) -> dict:
    return {
        'id':str(item['_id']),
        'name':item['name'],
        'release_date':item['release_date']
    }

def filmsEntity(entity) -> list:
    return [filmEntity(item) for item in entity]
