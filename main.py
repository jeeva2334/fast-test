from fastapi import *
import uvicorn
from database import SessionLocal
import random
import string
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models import *
from schemas import *
from sqlalchemy.orm import Session

class Questions(BaseModel):
    question: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_api_key(db):
    character_pool = string.ascii_letters + string.digits
    api_key = ""
    length = 16

    for _ in range(length):
        random_index = random.randint(0, len(character_pool) - 1)
        api_key += character_pool[random_index]

    # Ensure that the API key is unique (check against existing keys in the database, if applicable)
    if is_duplicate(api_key,db):
        return generate_api_key(length)

    return api_key

def is_duplicate(api_key,db):
    response = db.query(ApiBot).filter(ApiBot.apikey == api_key).all()
    if response:
        return True
    return False


@app.get("/")
def hello(db:Session = Depends(get_db)):
    response  = db.query(ApiBot).all()
    return response

@app.get("/get_api")
def create_api():
    api_key = generate_api_key(12)
    return f"cx-{str(api_key)}"

@app.post('/get_ans')
def get_ans(ques: Questions):
    print(ques.question)
    return {"ans":ques.question}

@app.post('/create_api')
def create_api(api: CreateApiBot,db: Session = Depends(get_db)):
    print(api) 
    apikey = f"cx-{generate_api_key(db)}"
    upload_api = ApiBot(apikey=apikey,image=api.imageUrl,color=api.color,textcolor=api.textColor,title=api.title,initial=api.initial)
    db.add(upload_api)
    db.commit()
    db.refresh(upload_api)
    return apikey

@app.post('/fetch_bot')
def fetch_bot(api:fetch,db: Session = Depends(get_db)):
    response  = db.query(ApiBot).filter(ApiBot.apikey == api.apikey).all()
    return response

# if __name__ == '__main__':
#     uvicorn.run(
#         "main:app",
#         host="localhost",
#         port=8081,
#         reload=True
#     )