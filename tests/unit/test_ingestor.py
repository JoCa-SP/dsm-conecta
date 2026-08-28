import pytest
from backend.ingestao.ingestor import is_duplicate, persistir_mensagem
from datetime import datetime

def test_is_duplicate(monkeypatch):
    # Simula uma conexão que retorna True (duplicata)
    monkeypatch.setattr('backend.ingestao.ingestor.get_db_connection', lambda: None)
    # Implemente mocks para testar
    assert is_duplicate("navegacao", "sessao_123", datetime.now()) == False

def test_persistir_mensagem():
    # Teste de persistência (mock do banco)
    pass