# DSM Conecta

Projeto de divulgação do curso de Desenvolvimento de Software Multiplataforma da Fatec Zona Sul, com coleta e análise de dados em tempo real.

## Tecnologias
- Python (FastAPI, Paho-MQTT)
- Node.js (Frontend Web)
- Docker (Mosquitto, TimescaleDB)
- GitHub Actions (CI)

## Como executar
1. Clone o repositório.
2. Suba os containers: `docker compose -f infra/docker-compose.yml up -d`
3. Instale as dependências: `pip install -r requirements-dev.txt`
4. Rode os testes: `python -m pytest tests/ -v`

## Contratos
- OpenAPI: `docs/contratos/openapi.yaml`
- Modelo de Dados: `docs/contratos/modelo-dados.md`
- Esquemas MQTT: `docs/contratos/mqtt-schemas/`