import { useEffect, useState } from 'react';
import { getNoticias } from '../../api/endpoints';

function Projetos() {
  const [projetos, setProjetos] = useState([]);

  useEffect(() => {
    getNoticias()
      .then((res) => setProjetos(res.data))
      .catch(() => {
        // Fallback com dados de exemplo
        setProjetos([
          { id: 1, titulo: 'Aplicativo de Mobilidade Urbana', corpo: 'App para otimizar rotas de transporte público usando IA.' },
          { id: 2, titulo: 'Sistema de Monitoramento IoT', corpo: 'Dashboard para sensores de temperatura e umidade em tempo real.' },
          { id: 3, titulo: 'Plataforma de E-commerce', corpo: 'Loja virtual com integração com redes sociais e pagamentos.' },
          { id: 4, titulo: 'App de Saúde Mental', corpo: 'Aplicativo com exercícios de respiração e monitoramento de humor.' },
        ]);
      });
  }, []);

  return (
    <div className="projetos">
      <h1>💻 Projetos dos Estudantes</h1>
      <p>Conheça alguns dos projetos desenvolvidos pelos alunos do curso.</p>

      <div className="lista-projetos">
        {projetos.map((proj) => (
          <div key={proj.id} className="projeto-card">
            <h3>{proj.titulo}</h3>
            <p>{proj.corpo}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Projetos;