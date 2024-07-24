import requests
import json
import os

from models import Card

url = "https://api.pipefy.com/graphql"

pipefy_key = os.getenv("PIPEFY_KEY")

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "Bearer " + pipefy_key
}

def create_card(card_data: dict) -> Card:
    card = Card(**card_data)

    return card