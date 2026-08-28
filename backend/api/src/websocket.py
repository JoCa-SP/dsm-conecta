from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
from .analytics import janela_visitantes
from .database import get_db_connection

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # A cada 2 segundos, enviar dados atualizados
            await asyncio.sleep(2)
            # Buscar número de visitantes ativos do banco
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT COUNT(DISTINCT dados_json->>'session_id') FROM telemetria
                WHERE categoria='navegacao' AND timestamp > NOW() - INTERVAL '5 minutes'
            """)
            ativos = cur.fetchone()[0] or 0
            cur.close()
            conn.close()
            # Atualizar a janela e verificar anomalia
            janela_visitantes.adicionar(ativos)
            media = janela_visitantes.media_movel()
            z = janela_visitantes.z_score(ativos)
            alerta = z > 3.0
            payload = {
                "visitantes_ativos": ativos,
                "media_movel": media,
                "z_score": z,
                "alerta": alerta
            }
            await manager.broadcast(json.dumps(payload))
    except WebSocketDisconnect:
        manager.disconnect(websocket)