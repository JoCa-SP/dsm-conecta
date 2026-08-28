from fastapi import APIRouter, HTTPException
from ..database import get_db_connection
from ..models.schemas import PresencaCreate
from datetime import datetime
import json

router = APIRouter()

@router.post("/registrar")
def registrar_presenca(presenca: PresencaCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    # Insere na tabela telemetria como categoria 'presenca'
    payload = {
        "session_id": presenca.session_id,
        "evento_id": presenca.evento_id,
        "metodo": presenca.metodo
    }
    cur.execute(
        "INSERT INTO telemetria (categoria, dados_json, timestamp) VALUES (%s, %s, %s)",
        ("presenca", json.dumps(payload), datetime.now())
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Presença registrada com sucesso"}