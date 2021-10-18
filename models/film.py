from pydantic import BaseModel, Field

class Film(BaseModel):
    name: str =  Field(...,min_length=1,max_length=350)
    release_date: str = Field(None)