import mqtt from 'paho-mqtt';

const clientId = 'webclient_' + Math.random().toString(16).substr(2, 8);
const client = new mqtt.Client('localhost', 9001, clientId);

let conectado = false;

client.connect({
    onSuccess: () => {
        console.log('✅ Conectado ao broker MQTT');
        conectado = true;
    },
    onFailure: (err) => {
        console.error('❌ Falha na conexão MQTT:', err);
    }
});

/**
 * Publica um evento no broker MQTT
 * @param {string} topic - Tópico MQTT (ex: dsm/prod/app/interacao/tela)
 * @param {object} payload - Objeto JSON com os dados do evento
 */
export function publicarEvento(topic, payload) {
    if (!conectado) {
        console.warn('⚠️ MQTT não conectado. Evento não enviado:', topic);
        return;
    }

    const mensagem = new mqtt.Message(JSON.stringify(payload));
    mensagem.destinationName = topic;
    mensagem.qos = 1;  // QoS 1: entrega garantida pelo menos uma vez
    mensagem.retained = false;
    client.send(mensagem);
    console.log(`📤 Evento publicado: ${topic}`, payload);
}