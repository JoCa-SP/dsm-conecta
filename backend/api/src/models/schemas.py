from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ConteudoBase(BaseModel):
    titulo: str
    corpo: str
    tipo: str


class ConteudoCreate(ConteudoBase):
    pass


class ConteudoResponse(ConteudoBase):
    id: int
    data_criacao: datetime

    class Config:
        orm_mode = True


class MetricaGeral(BaseModel):
    visitantes_ativos: int
    total_presencas: int
    ultima_atualizacao: datetime


class TelemetriaResponse(BaseModel):
    id: int
    categoria: str
    dados_json: dict
    timestamp: datetime


class PresencaCreate(BaseModel):
    evento_id: int
    metodo: str
    session_id: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
