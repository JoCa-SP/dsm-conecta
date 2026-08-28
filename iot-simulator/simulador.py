import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# ===== CONFIGURAÇÃO =====
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPICO_CONTAGEM = "dsm/prod/totem/sensor/contagem"
TOPICO_STATUS = "dsm/prod/totem/status"

# ===== CALLBACKS =====
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado ao broker MQTT")
        # Publica status online com retain=True (novos assinantes recebem imediatamente)
        client.publish(TOPICO_STATUS, "online", qos=1, retain=True)
    else:
        print(f"❌ Falha na conexão, código: {rc}")

def on_disconnect(client, userdata, rc):
    print("⚠️ Desconectado do broker")
    # Publica status offline com retain=True
    client.publish(TOPICO_STATUS, "offline", qos=1, retain=True)

# ===== CONFIGURAÇÃO DO CLIENTE =====
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Last Will: mensagem enviada se o cliente desconectar inesperadamente (ex: queda de energia)
client.will_set(TOPICO_STATUS, "offline", qos=1, retain=True)

# Conecta ao broker
client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_start()

# ===== LOOP DE PUBLICAÇÃO =====
try:
    contador = 0
    while True:
        contador += random.randint(1, 5)
        payload = {
            "sensor_id": "totem-01",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "contagem": contador
        }
        # Publica com QoS 1 (entrega garantida)
        client.publish(TOPICO_CONTAGEM, json.dumps(payload), qos=1)
        print(f"📤 Publicado: {payload}")
        time.sleep(5)  # Publica a cada 5 segundos
except KeyboardInterrupt:
    print("⏹️ Encerrando simulador...")
    client.disconnect()
    client.loop_stop()