import { useEffect, useState } from 'react';
import { getMetricasGerais, getDadosSensores } from '../../api/endpoints';
import { useWebSocket } from "../../hooks/useWebSocket";

function Dashboard() {
  const [metricas, setMetricas] = useState(null);
  const [sensores, setSensores] = useState([]);
  const { isConnected, lastMessage } = useWebSocket('ws://localhost:8000/ws');

  useEffect(() => {
    getMetricasGerais()
      .then((res) => setMetricas(res.data))
      .catch((err) => console.error('Erro ao buscar métricas:', err));

    getDadosSensores(20)
      .then((res) => setSensores(res.data))
      .catch((err) => console.error('Erro ao buscar sensores:', err));
  }, []);

  return (
    <div className="dashboard">
      <h1>📊 Painel Administrativo</h1>

      <div className="status-ws">
        WebSocket: {isConnected ? '🟢 Conectado' : '🔴 Desconectado'}
      </div>

      {metricas && (
        <div className="metricas">
          <h2>Métricas Gerais</h2>
          <div className="metricas-grid">
            <div className="card-metrica">
              <span className="numero">{metricas.visitantes_ativos}</span>
              <span className="label">👥 Visitantes ativos</span>
            </div>
            <div className="card-metrica">
              <span className="numero">{metricas.total_presencas}</span>
              <span className="label">✅ Presenças</span>
            </div>
            <div className="card-metrica">
              <span className="numero">{new Date(metricas.ultima_atualizacao).toLocaleTimeString()}</span>
              <span className="label">🕒 Última atualização</span>
            </div>
          </div>
        </div>
      )}

      {lastMessage && (
        <div className="dados-tempo-real">
          <h2>📡 Dados em tempo real</h2>
          <div>👥 Visitantes ativos: <strong>{lastMessage.visitantes_ativos}</strong></div>
          <div>📈 Média móvel: <strong>{lastMessage.media_movel?.toFixed(2)}</strong></div>
          <div>📊 Z-score: <strong>{lastMessage.z_score?.toFixed(2)}</strong></div>
          {lastMessage.alerta && (
            <div className="alerta">🚨 Alerta: Pico de acessos detectado!</div>
          )}
        </div>
      )}

      <div className="sensores">
        <h2>📡 Últimas leituras dos sensores</h2>
        {sensores.length === 0 && <p>Nenhum dado de sensor disponível.</p>}
        {sensores.map((s) => (
          <div key={s.id} className="sensor-item">
            <span>{s.dados_json.sensor_id || 'Sensor'}</span>
            <span>Contagem: {s.dados_json.contagem || 'N/A'}</span>
            <span>{new Date(s.timestamp).toLocaleTimeString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;