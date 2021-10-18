from fastapi import FastAPI
from routes.planet import planet
from routes.film import film

app = FastAPI()
app.include_router(planet, tags=['Planet'], prefix='/planet')
app.include_router(film, tags=['Film'], prefix='/film')


@app.get("/", tags=["Root"])
async def start_the_app():
    return {"message": "The Star Wars Challenger"}