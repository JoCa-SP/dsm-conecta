from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .routes import conteudo, metrics, presenca, admin
from .websocket import websocket_endpoint, manager
from .auth import oauth2_scheme
import uvicorn

app = FastAPI(title="DSM Conecta API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(conteudo.router, prefix="/api/v1/conteudo", tags=["Conteúdo"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["Métricas"])
app.include_router(presenca.router, prefix="/api/v1/presenca", tags=["Presença"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])

# WebSocket
@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)