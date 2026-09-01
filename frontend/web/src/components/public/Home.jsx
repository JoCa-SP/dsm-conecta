import { useEffect, useState } from 'react';
import { getMetricasGerais } from '../../api/endpoints';

function Home() {
  const [metricas, setMetricas] = useState(null);

  useEffect(() => {
    getMetricasGerais()
      .then((res) => setMetricas(res.data))
      .catch((err) => console.error('Erro ao buscar métricas:', err));
  }, []);

  return (
    <div className="home">
      {/* Seção Hero */}
      <div className="hero">
        <h1>🚀 DSM Conecta</h1>
        <p>
          O <strong>Curso Superior de Tecnologia em Desenvolvimento de Software Multiplataforma</strong> da Fatec Zona Sul
          forma profissionais capacitados para criar aplicações para Web, Desktop, Móvel, Nuvem e Internet das Coisas.
        </p>
      </div>

      {/* Diferenciais do curso */}
      <div className="destaques">
        <h2>📌 Diferenciais do curso</h2>
        <ul>
          <li>✅ Formação tecnológica prática desde o primeiro semestre</li>
          <li>✅ Microcertificações ao longo do curso</li>
          <li>✅ Metodologias ágeis e aprendizagem por projetos</li>
          <li>✅ Flexibilidade com aulas remotas no último ano</li>
          <li>✅ Integração com IoT, Nuvem e Inteligência Artificial</li>
          <li>✅ Corpo docente com experiência de mercado</li>
        </ul>
      </div>

      <div className="sobre-resumido" style={{ marginTop: '1.5rem', background: '#fff', padding: '1.5rem', borderRadius: '16px', boxShadow: '0 1px 3px rgba(0,0,0,0.06)' }}>
        <h2>🎯 Objetivo do Curso</h2>
        <p>
          Formar profissionais capazes de desenvolver softwares para diversas plataformas, empregando conceitos de
          Segurança da Informação e Inteligência Artificial, com visão ética e responsabilidade social.
        </p>

        <h2 style={{ marginTop: '1rem' }}>🧑‍🎓 Perfil do Egresso</h2>
        <ul>
          <li>Projeta, desenvolve e testa software para múltiplas plataformas.</li>
          <li>Seleciona e aplica conceitos de Linguagens de Programação, Banco de Dados, Engenharia de Software.</li>
          <li>Coordena projetos e equipes de desenvolvimento de software.</li>
          <li>Atua com ética, responsabilidade social e ambiental.</li>
        </ul>

        <h2 style={{ marginTop: '1rem' }}>📅 Duração e Turnos</h2>
        <ul>
          <li><strong>Duração:</strong> 3 anos (6 semestres)</li>
          <li><strong>Turno:</strong> Vespertino (40 vagas)</li>
          <li><strong>Modalidade:</strong> Presencial com algumas disciplinas on-line</li>
        </ul>

        <h2 style={{ marginTop: '1rem' }}>🏛️ Localização</h2>
        <p>
          Fatec Zona Sul "Dom Paulo Evaristo Arns"<br />
          Rua Frederico Grotte, 322 - Jardim São Luís, São Paulo - SP, 05818-270
        </p>

        <div style={{ marginTop: '0.5rem', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 1px 3px rgba(0,0,0,0.06)' }}>
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d263.87946095291704!2d-46.72976146076432!3d-23.66319465516872!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94ce519898114bc9%3A0xf63965c7d0dd6770!2sFaculdade%20de%20Tecnologia%20do%20Estado%20de%20S%C3%A3o%20Paulo%20Zona%20Sul%20-%20Dom%20Paulo%20Evaristo%20Arns!5e0!3m2!1spt-BR!2sbr!4v1788297818260!5m2!1spt-BR!2sbr"  // ← COLE A URL DO GOOGLE MAPS AQUI
            width="100%"
            height="350"
            style={{ border: 0, borderRadius: '12px' }}
            allowFullScreen=""
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
            title="Mapa da Fatec Zona Sul"
          ></iframe>
        </div>
      </div>

      {/* Métricas em tempo real */}
      {metricas && (
        <div className="metricas" style={{ marginTop: '1.5rem' }}>
          <h3>📊 Indicadores em tempo real</h3>
          <div>
            <div>👥 <strong>{metricas.visitantes_ativos}</strong> visitantes ativos</div>
            <div>✅ <strong>{metricas.total_presencas}</strong> presenças registradas</div>
            <div>🕒 Atualizado em: {new Date(metricas.ultima_atualizacao).toLocaleTimeString()}</div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;