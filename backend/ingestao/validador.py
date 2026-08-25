from datetime import datetime


def validar_mensagem(mensagem: dict) -> bool:
    campos_obrigatorios = ["session_id", "timestamp", "pagina"]
    for campo in campos_obrigatorios:
        if campo not in mensagem:
            return False

    if len(mensagem["session_id"]) < 10:
        return False

    try:
        datetime.fromisoformat(mensagem["timestamp"])
    except (ValueError, TypeError):
        return False

    paginas_validas = ["home", "matriz", "projetos", "quiz", "contato"]
    if mensagem["pagina"] not in paginas_validas:
        return False

    return True