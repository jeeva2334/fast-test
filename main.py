from fastapi import *
import uvicorn
import random
import string
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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

def generate_api_key(length):
    character_pool = string.ascii_letters + string.digits
    api_key = ""

    for _ in range(length):
        # Randomly select a character from the character pool
        random_index = random.randint(0, len(character_pool) - 1)
        api_key += character_pool[random_index]

    # Ensure that the API key is unique (check against existing keys in the database, if applicable)
    if is_duplicate(api_key):
        # Regenerate the API key
        return generate_api_key(length)

    return api_key

def is_duplicate(api_key):
    # Replace this function with your own logic to check if the API key is duplicate
    # For example, you could check against existing keys in a database
    # For this example, we assume there are no duplicates
    return False


@app.get("/")
def hello():
    return "Working fine"

@app.get("/get_api")
def create_api():
    api_key = generate_api_key(12)
    return f"cx-{str(api_key)}"

@app.post('/get_ans')
def get_ans(ques: Questions):
    print(ques.question)
    return {"ans":ques.question}
