import json
import os
import logging
import psycopg2
from psycopg2.extras import Json
import paho.mqtt.client as mqtt
from jsonschema import validate, ValidationError
from dotenv import load_dotenv

# ===== CONFIGURAÇÃO =====
load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "dsm_conecta")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

# Schemas (carregados dos arquivos de contrato)
SCHEMA_DIR = "docs/contratos/mqtt-schemas/"
SCHEMAS = {
    "interacao/tela": json.load(open(f"{SCHEMA_DIR}/evento_tela.json")),
    "totem/sensor/contagem": {
        "type": "object",
        "properties": {
            "sensor_id": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"},
            "contagem": {"type": "integer"}
        },
        "required": ["sensor_id", "timestamp", "contagem"]
    }
}


def get_db_connection():
    """Retorna uma conexão com o banco de dados."""
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )


def is_duplicate(categoria, sensor_id, timestamp):
    """Verifica se já existe um registro com o mesmo sensor_id e timestamp."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM telemetria WHERE categoria = %s "
        "AND dados_json->>'sensor_id' = %s AND timestamp = %s LIMIT 1",
        (categoria, sensor_id, timestamp)
    )
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists


def persistir_mensagem(categoria, payload):
    """Insere a mensagem na tabela telemetria."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO telemetria (categoria, dados_json, timestamp) VALUES (%s, %s, %s)",
        (categoria, Json(payload), payload.get("timestamp"))
    )
    conn.commit()
    cur.close()
    conn.close()
    logging.info(f"✅ Mensagem persistida: {categoria} - {payload.get('sensor_id')}")


def on_message(client, userdata, msg):
    """Callback principal para mensagens MQTT."""
    topic = msg.topic
    logging.info(f"📩 Mensagem recebida: {topic}")

    # Ignora mensagens de status (não JSON)
    if "/status" in topic:
        logging.info("⏳ Mensagem de status ignorada")
        return

    try:
        payload = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        logging.error("❌ Erro ao decodificar JSON (payload não é JSON válido)")
        return

    # Determina a categoria e o schema
    if "interacao/tela" in topic:
        categoria = "navegacao"
        schema = SCHEMAS["interacao/tela"]
        sensor_id = payload.get("session_id")
    elif "totem/sensor/contagem" in topic:
        categoria = "totem"
        schema = SCHEMAS["totem/sensor/contagem"]
        sensor_id = payload.get("sensor_id")
    else:
        logging.warning(f"⚠️ Tópico não mapeado: {topic}")
        return

    try:
        # 1. VALIDAÇÃO
        validate(instance=payload, schema=schema)

        # 2. DEDUPLICAÇÃO
        if is_duplicate(categoria, sensor_id, payload.get("timestamp")):
            logging.info(
                f"⏳ Mensagem duplicada ignorada: {sensor_id} - {payload.get('timestamp')}"
            )
            return

        # 3. PERSISTÊNCIA
        persistir_mensagem(categoria, payload)

    except ValidationError as e:
        logging.error(f"❌ Erro de validação: {e.message}")
    except Exception as e:
        logging.error(f"❌ Erro inesperado: {e}")


def main():
    """Ponto de entrada do ingestor."""
    logging.basicConfig(level=logging.INFO)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.subscribe("dsm/prod/#")
    logging.info("✅ Ingestor conectado e assinando tópicos")

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        logging.info("⏹️ Encerrando ingestor...")
        client.disconnect()


if __name__ == "__main__":
    main()
