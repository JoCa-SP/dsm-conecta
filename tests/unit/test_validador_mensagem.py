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