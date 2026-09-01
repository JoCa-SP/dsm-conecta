import { useState } from 'react';
import { registrarPresenca } from '../../api/endpoints';

function Presenca() {
  const [codigo, setCodigo] = useState('');
  const [mensagem, setMensagem] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const sessionId = localStorage.getItem('session_id') || 'anonimo_' + Date.now();

    registrarPresenca({
      evento_id: parseInt(codigo) || 1,
      metodo: 'qr',
      session_id: sessionId
    })
      .then(() => setMensagem('✅ Presença registrada com sucesso!'))
      .catch((err) => {
        console.error(err);
        setMensagem('❌ Erro ao registrar presença. Tente novamente.');
      });
  };

  return (
    <div className="presenca">
      <h1>📌 Registro de Presença</h1>
      <p>Digite o código QR do evento para registrar sua presença.</p>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Código do evento"
          value={codigo}
          onChange={(e) => setCodigo(e.target.value)}
          required
        />
        <button type="submit">Registrar</button>
      </form>

      {mensagem && <p className="mensagem">{mensagem}</p>}
    </div>
  );
}

export default Presenca;