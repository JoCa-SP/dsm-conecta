import pytest
from datetime import datetime

def test_validar_mensagem_evento_tela():
    mensagem = {
        "session_id": "abc1234567",
        "timestamp": datetime.now().isoformat(),
        "pagina": "home",
        "origem": "web"
    }
    
    # Esta importação ainda vai falhar (red phase)
    from backend.ingestao.validador import validar_mensagem
    
    assert validar_mensagem(mensagem) == True
    
def test_validar_mensagem_sem_campo_obrigatorio():
    mensagem = {
        "session_id": "abc1234567",
        "timestamp": "2026-08-25T16:00:00",
        # "pagina" ausente
    }
    from backend.ingestao.validador import validar_mensagem
    assert validar_mensagem(mensagem) == False

def test_validar_mensagem_session_id_curto():
    mensagem = {
        "session_id": "abc",
        "timestamp": "2026-08-25T16:00:00",
        "pagina": "home"
    }
    from backend.ingestao.validador import validar_mensagem
    assert validar_mensagem(mensagem) == False

def test_validar_mensagem_timestamp_invalido():
    mensagem = {
        "session_id": "abc1234567",
        "timestamp": "data invalida",
        "pagina": "home"
    }
    from backend.ingestao.validador import validar_mensagem
    assert validar_mensagem(mensagem) == False

def test_validar_mensagem_pagina_invalida():
    mensagem = {
        "session_id": "abc1234567",
        "timestamp": "2026-08-25T16:00:00",
        "pagina": "pagina_inexistente"
    }
    from backend.ingestao.validador import validar_mensagem
    assert validar_mensagem(mensagem) == False