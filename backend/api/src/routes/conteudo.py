from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db_connection
from ..models.schemas import ConteudoCreate, ConteudoResponse

router = APIRouter()

@router.get("/noticias", response_model=list[ConteudoResponse])
def listar_noticias():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, corpo, tipo, data_criacao FROM conteudo WHERE tipo='noticia' ORDER BY data_criacao DESC")
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

@router.get("/eventos", response_model=list[ConteudoResponse])
def listar_eventos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, corpo, tipo, data_criacao FROM conteudo WHERE tipo='evento' ORDER BY data_criacao DESC")
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

# Endpoints CRUD (autenticados) em admin.py