from fastapi import APIRouter, Depends
from ..database import get_db_connection
from ..models.schemas import ConteudoCreate, ConteudoResponse
from ..auth import get_current_user
from datetime import datetime

router = APIRouter()


@router.post("/conteudo", response_model=ConteudoResponse)
def criar_conteudo(item: ConteudoCreate, current_user=Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO conteudo (titulo, corpo, tipo, data_criacao) "
        "VALUES (%s, %s, %s, %s) RETURNING id, titulo, corpo, tipo, data_criacao",
        (item.titulo, item.corpo, item.tipo, datetime.now())
    )
    novo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return novo
