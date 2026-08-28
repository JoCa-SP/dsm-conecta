import json
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from backend.ingestao.ingestor import (
    get_db_connection,
    is_duplicate,
    persistir_mensagem,
    on_message
)


# ===== FIXTURES =====

@pytest.fixture
def mock_cursor():
    """Cria um cursor mockado que retorna resultados simples."""
    cursor = MagicMock()
    cursor.fetchone.return_value = None  # padrão: sem duplicata
    return cursor


@pytest.fixture
def mock_conn(mock_cursor):
    """Cria uma conexão mockada que retorna o cursor mockado."""
    conn = MagicMock()
    conn.cursor.return_value = mock_cursor
    return conn


# ===== TESTES =====

def test_get_db_connection():
    """Testa se a conexão é criada com os parâmetros corretos."""
    with patch('backend.ingestao.ingestor.psycopg2.connect') as mock_connect:
        mock_connect.return_value = MagicMock()
        conn = get_db_connection()
        assert conn is not None
        mock_connect.assert_called_once()


def test_is_duplicate_sem_duplicata(mock_conn):
    """Testa is_duplicate quando não há registro duplicado."""
    with patch('backend.ingestao.ingestor.get_db_connection', return_value=mock_conn):
        resultado = is_duplicate("navegacao", "sessao_123", datetime.now())
        assert resultado is False
        mock_conn.cursor.return_value.execute.assert_called_once()
        mock_conn.cursor.return_value.fetchone.assert_called_once()


def test_is_duplicate_com_duplicata(mock_conn):
    """Testa is_duplicate quando já existe um registro duplicado."""
    mock_conn.cursor.return_value.fetchone.return_value = (1,)  # Simula existência
    with patch('backend.ingestao.ingestor.get_db_connection', return_value=mock_conn):
        resultado = is_duplicate("totem", "totem-01", datetime.now())
        assert resultado is True


def test_persistir_mensagem(mock_conn):
    """Testa se persistir_mensagem executa o INSERT corretamente."""
    payload = {
        "sensor_id": "totem-01",
        "timestamp": datetime.now().isoformat(),
        "contagem": 42
    }
    with patch('backend.ingestao.ingestor.get_db_connection', return_value=mock_conn):
        persistir_mensagem("totem", payload)
        mock_conn.cursor.return_value.execute.assert_called_once()
        mock_conn.commit.assert_called_once()


@patch('backend.ingestao.ingestor.logging')
@patch('backend.ingestao.ingestor.validate')
@patch('backend.ingestao.ingestor.is_duplicate')
@patch('backend.ingestao.ingestor.persistir_mensagem')
def test_on_message_valido(
    mock_persistir,
    mock_is_duplicate,
    mock_validate,
    mock_logging
):
    """Testa o fluxo completo de on_message para uma mensagem válida."""
    mock_is_duplicate.return_value = False
    payload = {
        "session_id": "sessao_123456",
        "timestamp": datetime.now().isoformat(),
        "pagina": "home"
    }
    msg = MagicMock()
    msg.topic = "dsm/prod/app/interacao/tela"
    msg.payload = json.dumps(payload).encode()

    on_message(None, None, msg)

    mock_validate.assert_called_once()
    mock_is_duplicate.assert_called_once()
    mock_persistir.assert_called_once_with("navegacao", payload)


@patch('backend.ingestao.ingestor.logging')
def test_on_message_status_ignorado(mock_logging):
    """Testa se mensagens de status (/status) são ignoradas."""
    msg = MagicMock()
    msg.topic = "dsm/prod/totem/status"
    msg.payload = b"online"

    on_message(None, None, msg)

    mock_logging.info.assert_called_with("⏳ Mensagem de status ignorada")


@patch('backend.ingestao.ingestor.logging')
def test_on_message_json_invalido(mock_logging):
    """Testa se mensagens com JSON inválido são tratadas."""
    msg = MagicMock()
    msg.topic = "dsm/prod/app/interacao/tela"
    msg.payload = b"isso nao e json"

    on_message(None, None, msg)

    mock_logging.error.assert_called_with(
        "❌ Erro ao decodificar JSON (payload não é JSON válido)"
    )


@patch('backend.ingestao.ingestor.logging')
@patch('backend.ingestao.ingestor.validate')
def test_on_message_validacao_falha(mock_validate, mock_logging):
    """Testa se mensagens que falham na validação são rejeitadas."""
    from jsonschema import ValidationError
    mock_validate.side_effect = ValidationError("campo inválido")
    payload = {"session_id": "abc"}  # inválido
    msg = MagicMock()
    msg.topic = "dsm/prod/app/interacao/tela"
    msg.payload = json.dumps(payload).encode()

    on_message(None, None, msg)

    mock_logging.error.assert_called_with("❌ Erro de validação: campo inválido")


@patch('backend.ingestao.ingestor.logging')
@patch('backend.ingestao.ingestor.validate')
@patch('backend.ingestao.ingestor.is_duplicate')
def test_on_message_duplicata(
    mock_is_duplicate,
    mock_validate,
    mock_logging
):
    """Testa se mensagens duplicadas são ignoradas."""
    mock_is_duplicate.return_value = True
    payload = {
        "session_id": "sessao_123456",
        "timestamp": datetime.now().isoformat(),
        "pagina": "home"
    }
    msg = MagicMock()
    msg.topic = "dsm/prod/app/interacao/tela"
    msg.payload = json.dumps(payload).encode()

    on_message(None, None, msg)

    mock_logging.info.assert_called_with(
        f"⏳ Mensagem duplicada ignorada: {payload['session_id']} - {payload['timestamp']}"
    )
