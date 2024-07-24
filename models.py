from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

class Participante(BaseModel):
    nome: str
    email: str
    contato: str
    foto: str

class Card(BaseModel):
    id: Optional[UUID] = uuid4
    nome: str
    descricao: str
    data: datetime
    duracao: float
    participantes: List[Participante] 