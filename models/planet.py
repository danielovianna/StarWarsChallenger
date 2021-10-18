from pydantic import BaseModel, Field

class Planet(BaseModel):
    name: str =  Field(...,min_length=1,max_length=350)
    climate: str = Field(None,min_length=1,max_length=350)
    diameter: int = Field(None, ge=0)
    population: str = Field(None)
    films: list = Field(None)