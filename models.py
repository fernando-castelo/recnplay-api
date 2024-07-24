from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class Participante(BaseModel):
    nome: str
    email: str
    contato: str
    foto: str

class Card(BaseModel):
    nome: str
    descricao: str
    data: datetime
    duracao: int
    participantes: List[Participante] 