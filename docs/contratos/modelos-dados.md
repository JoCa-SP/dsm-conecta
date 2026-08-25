# Modelo de Dados (Web)

## Relacionais
- **conteudo**: id, titulo, corpo, tipo (noticia/evento), data_criacao
- **projeto**: id, nome, descricao, imagem_url, tecnologias
- **depoimento**: id, estudante_nome, texto
- **usuario_admin**: id, email, senha_hash

## Telemetria (TimescaleDB)
- **telemetria**: 
  - particionada por dia (timestamp)
  - campos: id, session_id, categoria, dados_json (ex: {pagina, quiz_respostas})
  - índice: (categoria, timestamp)
- **Retenção**: 90 dias brutos, 5 anos agregados.