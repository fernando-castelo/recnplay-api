from fastapi import FastAPI
from models import Card
from pipefy_service import create_card;
import os

app = FastAPI()

@app.post("/api/v1/cards")
def register_card(card: Card):
    ids = create_card(card)
    return {"ids": ids}