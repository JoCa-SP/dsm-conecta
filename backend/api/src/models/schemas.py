from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Conteúdo
class ConteudoBase(BaseModel):
    titulo: str
    corpo: str
    tipo: str  # 'noticia' ou 'evento'

class ConteudoCreate(ConteudoBase):
    pass

class ConteudoResponse(ConteudoBase):
    id: int
    data_criacao: datetime
    class Config:
        orm_mode = True

# Métricas
class MetricaGeral(BaseModel):
    visitantes_ativos: int
    total_presencas: int
    ultima_atualizacao: datetime

class TelemetriaResponse(BaseModel):
    id: int
    categoria: str
    dados_json: dict
    timestamp: datetime

# Presença
class PresencaCreate(BaseModel):
    evento_id: int
    metodo: str  # 'qr' ou 'geolocalizacao'
    session_id: str

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None