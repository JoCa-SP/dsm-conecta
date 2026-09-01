import { useState } from 'react';

function Contato() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [mensagem, setMensagem] = useState('');
  const [enviado, setEnviado] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Aqui você pode integrar com a API real de envio de e-mail
    console.log('Contato enviado:', { nome, email, mensagem });
    setEnviado(true);
    setNome('');
    setEmail('');
    setMensagem('');
    setTimeout(() => setEnviado(false), 5000);
  };

  return (
    <div className="contato">
      <h1>📧 Contato</h1>
      <p>Dúvidas? Envie uma mensagem para a coordenação do curso ou entre em contato pelos canais oficiais da unidade.</p>

      <div className="contato-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '1.5rem' }}>
        {/* COLUNA 1: FORMULÁRIO */}
        <div>
          <h2>📝 Envie sua mensagem</h2>
          {enviado && <p className="sucesso">✅ Mensagem enviada com sucesso!</p>}
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Seu nome"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              required
            />
            <input
              type="email"
              placeholder="Seu e-mail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <textarea
              placeholder="Sua mensagem"
              value={mensagem}
              onChange={(e) => setMensagem(e.target.value)}
              rows="5"
              required
            />
            <button type="submit">Enviar</button>
          </form>
        </div>

        {/* COLUNA 2: DADOS OFICIAIS */}
        <div>
          <h2>📌 Informações oficiais</h2>
          <div style={{ background: '#f8fafc', padding: '1.5rem', borderRadius: '12px' }}>
            <p style={{ marginBottom: '0.75rem' }}>
              <strong>📍 Endereço:</strong><br />
              Rua Frederico Grotte, 322 - Jardim São Luís<br />
              São Paulo - SP, 05818-270
            </p>
            <p style={{ marginBottom: '0.75rem' }}>
              <strong>📞 Telefone:</strong><br />
              (11) 5818-2700
            </p>
            <p style={{ marginBottom: '0.75rem' }}>
              <strong>✉️ E-mail:</strong><br />
              <a href="mailto:fatec.zs@fatec.sp.gov.br" style={{ color: '#2563eb', textDecoration: 'none' }}>
                fatec.zs@fatec.sp.gov.br
              </a>
            </p>
            <p style={{ marginBottom: '0.75rem' }}>
              <strong>🌐 Site:</strong><br />
              <a href="https://fateczonasul.edu.br" target="_blank" rel="noopener noreferrer" style={{ color: '#2563eb', textDecoration: 'none' }}>
                fateczonasul.edu.br
              </a>
            </p>
            <p style={{ marginBottom: '0' }}>
              <strong>🕒 Horário de atendimento:</strong><br />
              Segunda a sexta, das 8h às 22h
            </p>
          </div>
          <div style={{ marginTop: '1rem' }}>
            <a
              href="https://fateczonasul.edu.br"
              target="_blank"
              rel="noopener noreferrer"
              style={{ display: 'inline-block', background: '#2563eb', color: '#fff', padding: '0.6rem 1.5rem', borderRadius: '8px', textDecoration: 'none', fontWeight: '600' }}
            >
              Acessar site oficial →
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Contato;