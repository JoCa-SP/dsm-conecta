-- Habilita a extensão TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Cria a tabela de telemetria
CREATE TABLE IF NOT EXISTS telemetria (
    id SERIAL,
    categoria VARCHAR(50) NOT NULL,
    dados_json JSONB NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL
);

-- Converte para hypertable (particionamento por tempo)
SELECT create_hypertable('telemetria', 'timestamp');

-- Índice para consultas por categoria e tempo
CREATE INDEX idx_telemetria_categoria_timestamp ON telemetria (categoria, timestamp DESC);

-- Índice para busca por sensor_id (via JSONB)
CREATE INDEX idx_telemetria_sensor_id ON telemetria ((dados_json->>'sensor_id'));

-- Política de retenção: dados brutos por 30 dias
SELECT add_retention_policy('telemetria', INTERVAL '30 days');

-- Agregação contínua: média de contagem por hora (para totem)
CREATE MATERIALIZED VIEW IF NOT EXISTS avg_contagem_hora
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', timestamp) AS bucket,
    categoria,
    AVG((dados_json->>'contagem')::INT) AS avg_contagem
FROM telemetria
WHERE categoria = 'totem'
GROUP BY bucket, categoria
WITH NO DATA;

-- Atualiza a agregação a cada hora
SELECT add_continuous_aggregate_policy('avg_contagem_hora',
    start_offset => INTERVAL '1 day',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour'
);