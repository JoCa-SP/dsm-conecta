import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // sobe para 20 usuários
    { duration: '1m', target: 50 },    // sobe para 50
    { duration: '2m', target: 100 },   // sobe para 100
    { duration: '1m', target: 0 },     // desce
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% das requisições < 500ms
    http_req_failed: ['rate<0.01'],   // menos de 1% de falhas
  },
};

export default function () {
  // 1. Testa a API de métricas
  const res = http.get('http://localhost:8000/api/v1/metrics/geral');
  check(res, {
    'status é 200': (r) => r.status === 200,
    'tempo de resposta < 500ms': (r) => r.timings.duration < 500,
  });

  // 2. Simula uma presença
  const payload = JSON.stringify({
    evento_id: 1,
    metodo: 'qr',
    session_id: 'k6_' + __VU + '_' + Date.now(),
  });
  const presenca = http.post('http://localhost:8000/api/v1/presenca/registrar', payload, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(presenca, {
    'presença registrada com sucesso': (r) => r.status === 200,
  });

  sleep(1);
}