from fastapi import APIRouter, HTTPException
from ..database import get_db_connection
from ..models.schemas import MetricaGeral
from datetime import datetime

router = APIRouter()

@router.get("/geral", response_model=MetricaGeral)
def metricas_gerais():
    conn = get_db_connection()
    cur = conn.cursor()
    # Visitantes ativos: contagem de session_id únicos nos últimos 5 minutos
    cur.execute("""
        SELECT COUNT(DISTINCT dados_json->>'session_id') as ativos
        FROM telemetria
        WHERE categoria = 'navegacao'
          AND timestamp > NOW() - INTERVAL '5 minutes'
    """)
    ativos = cur.fetchone()['ativos'] or 0

    # Total de presenças
    cur.execute("SELECT COUNT(*) as total FROM telemetria WHERE categoria = 'presenca'")
    presencas = cur.fetchone()['total'] or 0

    cur.close()
    conn.close()
    return MetricaGeral(
        visitantes_ativos=ativos,
        total_presencas=presencas,
        ultima_atualizacao=datetime.now()
    )

@router.get("/sensores")
def dados_sensores(limit: int = 10):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, categoria, dados_json, timestamp
        FROM telemetria
        WHERE categoria = 'totem'
        ORDER BY timestamp DESC
        LIMIT %s
    """, (limit,))
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados