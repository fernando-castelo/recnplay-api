from fastapi import FastAPI
from dotenv import load_dotenv
from models import Card;

load_dotenv()
app = FastAPI()

@app.post("/api/v1/cards")
def register_card(card: Card):
    return {"card": card}