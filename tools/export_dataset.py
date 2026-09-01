import csv
import os
import psycopg2
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "dsm_conecta")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

# Conecta ao banco
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    print("✅ Conectado ao banco de dados.")
except Exception as e:
    print(f"❌ Erro ao conectar ao banco: {e}")
    exit(1)

cur = conn.cursor()

# Consulta agregada (últimos 30 dias, por dia e categoria)
query = """
    SELECT
        DATE(timestamp) AS dia,
        categoria,
        COUNT(*) AS total
    FROM telemetria
    WHERE timestamp > NOW() - INTERVAL '30 days'
    GROUP BY dia, categoria
    ORDER BY dia DESC, categoria;
"""

try:
    cur.execute(query)
    resultados = cur.fetchall()
except Exception as e:
    print(f"❌ Erro ao executar consulta: {e}")
    conn.close()
    exit(1)

# Define o nome do arquivo de saída
output_file = "dados_abertos.csv"

# Escreve no CSV
try:
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['data', 'categoria', 'total'])
        writer.writerows(resultados)
    print(f"✅ Dataset exportado com sucesso para: {output_file}")
except Exception as e:
    print(f"❌ Erro ao escrever arquivo CSV: {e}")

# Fecha a conexão
cur.close()
conn.close()