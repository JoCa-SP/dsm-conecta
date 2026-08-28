import random
import psycopg2
from psycopg2.extras import Json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "dsm_conecta")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

def gerar_dados(total=1_000_000):
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()

    start_time = datetime(2026, 8, 1)
    batch = []
    for i in range(total):
        timestamp = start_time + timedelta(seconds=random.randint(0, 86400 * 30))
        categoria = random.choice(["navegacao", "totem"])
        if categoria == "navegacao":
            dados = {
                "session_id": f"session_{random.randint(1000, 9999)}",
                "pagina": random.choice(["home", "matriz", "projetos", "quiz", "contato"]),
                "user_agent": "Mozilla/5.0"
            }
        else:
            dados = {
                "sensor_id": f"totem-{random.randint(1, 5)}",
                "contagem": random.randint(1, 100)
            }
        batch.append((categoria, Json(dados), timestamp))

        if len(batch) >= 1000:
            cur.executemany(
                "INSERT INTO telemetria (categoria, dados_json, timestamp) VALUES (%s, %s, %s)",
                batch
            )
            conn.commit()
            print(f"✅ Inseridos {i+1} registros...")
            batch = []

    if batch:
        cur.executemany(
            "INSERT INTO telemetria (categoria, dados_json, timestamp) VALUES (%s, %s, %s)",
            batch
        )
        conn.commit()

    cur.close()
    conn.close()
    print(f"🎯 Concluído! {total} registros inseridos.")

if __name__ == "__main__":
    gerar_dados()