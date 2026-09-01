import { useEffect, useState } from 'react';
import { getEventos } from '../../api/endpoints';

function Agenda() {
  const [eventos, setEventos] = useState([]);

  useEffect(() => {
    getEventos()
      .then((res) => setEventos(res.data))
      .catch(() => {
        setEventos([
          { id: 1, titulo: 'Fatec Portas Abertas', data: '2026-09-15', descricao: 'Visita guiada para alunos do ensino médio.' },
          { id: 2, titulo: 'Hackathon DSM', data: '2026-10-20', descricao: 'Maratona de programação com premiação para os melhores projetos.' },
          { id: 3, titulo: 'Processo Seletivo 2027', data: '2026-11-10', descricao: 'Início das inscrições para o vestibular.' },
          { id: 4, titulo: 'Tech Talk: IA e Futuro', data: '2026-12-05', descricao: 'Palestra com especialistas em Inteligência Artificial.' },
        ]);
      });
  }, []);

  return (
    <div className="agenda">
      <h1>📅 Agenda de Eventos</h1>
      <p>Fique por dentro dos eventos, prazos e etapas do processo seletivo.</p>

      {eventos.map((ev) => (
        <div key={ev.id} className="evento-card">
          <h3>{ev.titulo}</h3>
          <p><strong>Data:</strong> {new Date(ev.data).toLocaleDateString('pt-BR')}</p>
          <p>{ev.descricao}</p>
        </div>
      ))}
    </div>
  );
}

export default Agenda;