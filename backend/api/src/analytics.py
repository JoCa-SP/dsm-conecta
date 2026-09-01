import math
from collections import deque
from datetime import datetime, timedelta


class JanelaDeslizante:
    def __init__(self, tamanho=60, intervalo_segundos=5):
        self.tamanho = tamanho
        self.intervalo = timedelta(seconds=intervalo_segundos)
        self.dados = deque(maxlen=tamanho)
        self.ultima_atualizacao = datetime.now()

    def adicionar(self, valor):
        agora = datetime.now()
        self.dados.append((agora, valor))
        # Remove dados antigos fora da janela temporal
        limite = agora - timedelta(seconds=self.tamanho * self.intervalo.total_seconds())
        while self.dados and self.dados[0][0] < limite:
            self.dados.popleft()

    def media_movel(self):
        if not self.dados:
            return None
        return sum(v for _, v in self.dados) / len(self.dados)

    def desvio_padrao(self):
        if len(self.dados) < 2:
            return None
        media = self.media_movel()
        variancia = sum((v - media) ** 2 for _, v in self.dados) / len(self.dados)
        return math.sqrt(variancia)

    def z_score(self, valor):
        media = self.media_movel()
        desvio = self.desvio_padrao()
        if desvio is None or desvio == 0:
            return 0
        return (valor - media) / desvio


# Instância global para métricas de visitantes ativos
janela_visitantes = JanelaDeslizante(tamanho=60, intervalo_segundos=5)


def detectar_anomalia(valor, limite=3.0):
    z = janela_visitantes.z_score(valor)
    if z > limite:
        return True, z
    return False, z
