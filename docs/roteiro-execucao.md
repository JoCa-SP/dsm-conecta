# Roteiro - DSM Conecta Web

## Pré-requisitos
- Docker, Git, Node.js 18+, Python 3.10+

## Subir a infra
1. Clone: `git clone ... && cd dsm-conecta-web`
2. Copie `.env.example` para `.env`
3. Suba os containers: `docker-compose -f infra/docker-compose.yml up -d`
4. Verifique: `docker ps`

## Rodar o Frontend Web (desenvolvimento)
```bash
cd frontend/web
npm install
npm run dev