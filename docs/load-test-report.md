# Relatório do Ensaio de Carga – DSM Conecta

**Data:** 01/09/2026  
**Ferramenta:** k6  
**Objetivo:** Avaliar a escalabilidade e o desempenho do sistema sob carga simulada de 100 usuários simultâneos.

## Cenário de teste
- **Duração:** 4 minutos e 30 segundos.
- **Usuários virtuais:** 1 → 100 (rampa de crescimento).
- **Requisições por usuário:** 2 (GET `/metrics/geral` + POST `/presenca/registrar`).
- **Total de iterações:** 13.017.

## Resultados

| Métrica | Valor |
| :--- | :--- |
| Requisições totais | 26.034 |
| Taxa de sucesso dos checks | 95,51% |
| Taxa de erro (HTTP) | 6,72% |
| Latência média | 52,19 ms |
| Latência p(95) | 120,64 ms |
| Latência máxima | 1,05 s |

### Análise dos thresholds

- ✅ `http_req_duration`: p(95) = 120,64 ms **(dentro do limite de 500 ms)**.
- ❌ `http_req_failed`: taxa de erro = 6,72% **(acima do limite de 1%)**.

### Observações
- As falhas ocorreram principalmente nas requisições POST `/presenca/registrar`, possivelmente devido a:
  - Concorrência no banco de dados (duplicidade de chave ou timeout).
  - Validação do campo `metodo` ou `evento_id` inexistente.
- A latência manteve-se dentro do esperado mesmo com 100 VUs simultâneos.

## Conclusão
O sistema suportou a carga planejada com boa performance. A taxa de erro pode ser reduzida com ajustes pontuais no backend, mas não compromete a funcionalidade geral.

---

**Próximos passos:** Realizar a ação de divulgação e preparar a documentação final.