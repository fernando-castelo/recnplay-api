from typing import List
from dotenv import load_dotenv
import requests
import json
import os
from models import Card, Participante

load_dotenv()
pipefy_key = os.getenv("PIPEFY_KEY")

url = "https://api.pipefy.com/graphql"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {pipefy_key}"
}

def create_card(card: Card) -> Card:
    query = {
        "query": """
            mutation {
                createCard(input: {
                    pipe_id: "304509333"
                    fields_attributes:[
                        {field_id:"nome_do_solicitante", field_value:"%s"},
                        {field_id:"descri_o", field_value:"%s"},
                        {field_id:"data", field_value:"%s"},
                        {field_id:"dura_o_da_atividade_em_horas_por_dia", field_value:"%s"}
                    ]
                }) {
                    clientMutationId
                    card {
                        id
                    }
                }
            }
        """ % (card.nome, card.descricao, card.data.isoformat(), card.duracao)
    }

    card_response = requests.post(url, json=query, headers=headers)
    card_response_dict = json.loads(card_response.text)
    card_id = card_response_dict['data']['createCard']['card']['id']

    participantes_ids = handle_participante_creation(card.participantes)
    handle_card_update(card_id, participantes_ids)
    return participantes_ids

def handle_participante_creation(participantes: List[Participante]):
   participantes_ids = []
   for participante in participantes:
        try:
            participante_id = create_participante(participante)
            participantes_ids.append(participante_id)
        except Exception as e:
            print(f"Failed to create participante {participante.nome}: {e}")

   return participantes_ids
   
def create_participante(participante: Participante):
    query = {
    "query": """
        mutation {
        createTableRecord(input: {
            table_id: "304509429"
            fields_attributes: [
            {field_id: "nome", field_value: "%s"},
            {field_id: "email", field_value: "%s"},
            {field_id: "contato", field_value: "%s"},
            {field_id: "foto", field_value: "%s"}
            ]
        }) {
            clientMutationId
            table_record {
                id
            }
        }
        }
    """ % (participante.nome, participante.email, participante.contato, participante.foto)
    }

    response = requests.post(url, json=query, headers=headers)
    response_dict = json.loads(response.text)
    return response_dict['data']['createTableRecord']['table_record']['id']

def handle_card_update(card_id, participantes_id):
    
    valor_id_list = []
    for id in participantes_id:
        try: 
            valor_id_list.append(id)
        except Exception as e:
            print(f"Failed to update card: {e}")
        update_card(card_id, id)


def update_card(card_id, id):
   query = {
                "query": """
                mutation{
                        updateCardField(input:{
                            card_id: "%s",
                            field_id:"participantes"
                            new_value: "%s"
                        }) {
                            clientMutationId
                        }
                    }
                """ % (card_id, id)
            }
   response = requests.post(url, json=query, headers=headers)
   print(response)

