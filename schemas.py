from pydantic import BaseModel

class CreateApiBot(BaseModel):
    color: str
    textColor: str
    title: str
    initial: str
    imageUrl: str

class fetch(BaseModel):
    apikey: str