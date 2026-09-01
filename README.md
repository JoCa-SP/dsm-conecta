# 🚀 DSM Conecta

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://reactjs.org/)

> **Aplicação multiplataforma de divulgação do curso de Desenvolvimento de Software Multiplataforma da Fatec Zona Sul, com coleta e análise de dados em tempo real.**

---

## 📖 Sobre o Projeto

O **DSM Conecta** é uma aplicação web desenvolvida para divulgar o curso superior de tecnologia em **Desenvolvimento de Software Multiplataforma** da Fatec Zona Sul. O sistema combina:

- **Divulgação institucional**: informações sobre o curso, matriz curricular, projetos dos alunos, depoimentos e agenda de eventos.
- **Interação com o usuário**: questionário de afinidade vocacional e registro de presença em eventos (QR Code).
- **Coleta e análise em tempo real**: monitoramento de visitantes ativos, registros de presença e leituras de sensores (totem simulado).
- **Painel administrativo**: gestão de conteúdo e visualização de indicadores em tempo real.

O projeto foi desenvolvido como parte da disciplina **Laboratório de Desenvolvimento de Software Multiplataforma**, sob orientação do Prof. Dr. Winston Aparecido Andrade, no 2º semestre de 2026.

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** – API REST com documentação automática (OpenAPI).
- **Paho-MQTT** – Cliente MQTT para comunicação com o broker.
- **psycopg2-binary** – Conexão com PostgreSQL/TimescaleDB.
- **TimescaleDB** – Banco de dados de séries temporais com particionamento e agregações contínuas.
- **Python 3.10+**

### Frontend
- **React 18** – Biblioteca para construção de interfaces.
- **Vite** – Build tool moderna e rápida.
- **React Router** – Navegação entre páginas.
- **Axios** – Cliente HTTP para consumo da API.
- **CSS3** – Estilização personalizada com design responsivo.

### Infraestrutura e Qualidade
- **Docker** – Orquestração dos serviços (Mosquitto, TimescaleDB).
- **Mosquitto** – Broker MQTT para mensageria.
- **GitHub Actions** – Pipeline de integração contínua (CI) com flake8, pytest e cobertura.
- **Pytest** – Testes unitários e de integração.
- **k6** – Teste de carga para validação de escalabilidade.

---

## 🏗️ Arquitetura da Solução

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Frontend      │────▶│   API (FastAPI) │────▶│   TimescaleDB   │
│   (React/Vite)  │     │   (REST/WS)     │     │   (Hypertable)  │
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Mosquitto     │
                        │   (MQTT Broker) │
                        └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
            ┌───────────┐ ┌───────────┐ ┌───────────┐
            │  Ingestor │ │  Simulador│ │  Frontend │
            │  (Python) │ │  (Totem)  │ │  (MQTT)   │
            └───────────┘ └───────────┘ └───────────┘
```

### Componentes principais:
- **Ingestor**: consome mensagens MQTT, valida, deduplica e persiste no TimescaleDB.
- **API**: expõe dados via REST e WebSocket para o frontend.
- **Frontend**: interface web com páginas públicas e painel administrativo.
- **Simulador de totem**: gera dados simulados de contagem de visitantes.
- **Gerador de carga**: insere dados sintéticos para testes de desempenho.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- **Docker Desktop** (para Windows/Mac) ou **Docker Engine** (Linux)
- **Python 3.10+** (com `pip` e `venv`)
- **Node.js 18+** (com `npm`)
- **Git** (para clonar o repositório)
- **k6** (opcional, para testes de carga)

### 1. Clone o repositório

```bash
git clone https://github.com/JoCa-SP/dsm-conecta.git
cd dsm-conecta
```

### 2. Configure o ambiente

Crie um arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Edite as variáveis se necessário (ex: credenciais do banco).

### 3. Suba a infraestrutura (MQTT + TimescaleDB)

```bash
docker compose -f infra/docker-compose.yml up -d
```

Verifique se os containers estão rodando:

```bash
docker ps
```

Você deve ver `infra-mosquitto-1` e `infra-timescaledb-1`.

### 4. Configure o backend

Crie e ative o ambiente virtual Python:

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate            # Windows
```

Instale as dependências:

```bash
pip install -r requirements-dev.txt
```

### 5. Execute o Ingestor (consome mensagens MQTT)

```bash
python backend/ingestao/ingestor.py
```

Deixe este terminal aberto – ele vai processar as mensagens em tempo real.

### 6. Execute a API

Em outro terminal, com o ambiente virtual ativado:

```bash
cd backend/api
python -m uvicorn src.main:app --reload
```

A API estará disponível em `http://localhost:8000`.  
A documentação Swagger estará em `http://localhost:8000/docs`.

### 7. Execute o Frontend

Em um terceiro terminal:

```bash
cd frontend/web
npm install
npm run dev
```

O frontend estará disponível em `http://localhost:5173`.

### 8. (Opcional) Execute o Simulador de Totem

Para gerar dados simulados de contagem de visitantes:

```bash
python iot-simulator/simulador.py
```

---

## 🧪 Executando os Testes

### Testes unitários e de integração (backend)

```bash
pytest tests/ -v --cov=backend/ingestao --cov-report=term
```

### Análise estática (flake8)

```bash
flake8 backend/ tests/
```

---

## 📊 Teste de Carga (k6)

O projeto inclui um script de teste de carga para validar a escalabilidade da API.

### 1. Instale o k6

- **Windows (com winget):**
  ```bash
  winget install GrafanaLabs.k6
  ```
- **Linux/Mac:**
  ```bash
  brew install k6
  ```

### 2. Execute o teste

Com o backend e o ingestor rodando, execute:

```bash
k6 run load-test.js
```

O resultado será exibido no terminal com métricas de desempenho (latência, taxa de erro, throughput).

---

## 📂 Dados Abertos

O sistema exporta dados agregados e anonimizados para análise pública.

### Exportar dataset

```bash
python tools/export_dataset.py
```

O arquivo `dados_abertos.csv` será gerado na raiz do projeto com a estrutura:

| data       | categoria   | total |
| :--------- | :---------- | :---- |
| 2026-09-01 | presenca    | 1200  |
| 2026-09-01 | totem       | 86    |
| 2026-09-01 | navegacao   | 450   |

O dicionário de dados está disponível em `docs/dicionario-dados.md`.

---

## 📚 Documentação

- [API (OpenAPI)](http://localhost:8000/docs) – Disponível quando a API estiver rodando.
- [Relatório do Ensaio de Carga](docs/load-test-report.md)
- [Guia de Implantação](docs/guia-implantacao.md)
- [Manual do Usuário](docs/manual-usuario.md)
- [Dicionário de Dados](docs/dicionario-dados.md)
- [Contratos MQTT](docs/contratos/mqtt-schemas/)

---

## 📁 Estrutura do Repositório

```
dsm-conecta/
├── backend/
│   ├── api/                 # API FastAPI
│   └── ingestao/            # Serviço de ingestão MQTT
├── frontend/
│   └── web/                 # Frontend React (Vite)
├── infra/
│   ├── docker-compose.yml   # Orquestração dos serviços
│   └── mosquitto/           # Configuração do broker MQTT
├── iot-simulator/           # Simulador de totem (contagem)
├── tools/
│   ├── export_dataset.py    # Exportação de dados abertos
│   └── load_generator.py    # Gerador de carga sintética
├── docs/
│   ├── atas/                # Registros de reuniões
│   ├── contratos/           # Esquemas MQTT, OpenAPI, modelo de dados
│   └── load-test-report.md  # Relatório do ensaio de carga
├── tests/
│   └── unit/                # Testes unitários (pytest)
├── .github/workflows/       # Pipeline CI (GitHub Actions)
├── .env.example             # Exemplo de variáveis de ambiente
├── requirements-dev.txt     # Dependências Python
├── load-test.js             # Script de teste de carga (k6)
├── dados_abertos.csv        # Dataset anonimizado (gerado)
└── README.md                # Este arquivo
```

---

## 📜 Licença

Este projeto é de uso **acadêmico e educacional**.  
Consulte a Fatec Zona Sul para autorização de uso comercial.

---

## 👥 Autores

- **João Carlos** – Desenvolvimento e documentação
- **Prof. Dr. Winston Aparecido Andrade** – Orientação

Curso Superior de Tecnologia em **Desenvolvimento de Software Multiplataforma**  
Fatec Zona Sul – 2026/2

---

## 🙏 Agradecimentos

- Ao corpo docente da Fatec Zona Sul pelo suporte e orientação.
- Aos alunos e egressos que contribuíram com depoimentos e feedback.
- Aos parceiros da ação de divulgação (escolas e empresas participantes).

---

**DSM Conecta – Divulgando o futuro do desenvolvimento de software!** 🚀