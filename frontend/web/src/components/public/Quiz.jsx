import { useState } from 'react';
import { registrarPresenca } from '../../api/endpoints';

function Quiz() {
  const [respostas, setRespostas] = useState({});
  const [resultado, setResultado] = useState(null);

  const perguntas = [
    { id: 1, pergunta: 'Você gosta de resolver problemas lógicos?', opcoes: ['Sim', 'Não'] },
    { id: 2, pergunta: 'Prefere trabalhar em equipe ou sozinho(a)?', opcoes: ['Equipe', 'Sozinho(a)'] },
    { id: 3, pergunta: 'Tem interesse em programar aplicativos e sites?', opcoes: ['Sim', 'Não'] },
    { id: 4, pergunta: 'Gosta de aprender novas tecnologias?', opcoes: ['Sim', 'Não'] },
    { id: 5, pergunta: 'Você se considera uma pessoa criativa?', opcoes: ['Sim', 'Não'] },
  ];

  const handleSubmit = () => {
    const todasRespondidas = perguntas.every((q) => respostas[q.id]);
    if (!todasRespondidas) {
      alert('Responda todas as perguntas antes de ver o resultado.');
      return;
    }

    // Registra presença (opcional)
    registrarPresenca({
      evento_id: 1,
      metodo: 'quiz',
      session_id: localStorage.getItem('session_id') || 'anonimo_' + Date.now()
    }).catch((err) => console.error('Erro ao registrar presença:', err));

    const simCount = Object.values(respostas).filter((v) => v === 'Sim').length;
    if (simCount >= 4) {
      setResultado('✅ Você tem um perfil muito alinhado com o desenvolvimento de software!');
    } else if (simCount >= 2) {
      setResultado('📚 Você pode explorar mais a área, mas o curso também oferece ótimas oportunidades para quem quer aprender!');
    } else {
      setResultado('🧐 Talvez você se identifique mais com outras áreas da tecnologia, mas vale a pena conhecer o curso!');
    }
  };

  return (
    <div className="quiz">
      <h1>📊 Questionário de Afinidade</h1>
      <p>Descubra se a área de desenvolvimento de software combina com você!</p>

      {perguntas.map((q) => (
        <div key={q.id} className="pergunta">
          <p><strong>{q.pergunta}</strong></p>
          {q.opcoes.map((opcao) => (
            <label key={opcao}>
              <input
                type="radio"
                name={`pergunta_${q.id}`}
                value={opcao}
                onChange={(e) => setRespostas({ ...respostas, [q.id]: e.target.value })}
              />
              {opcao}
            </label>
          ))}
        </div>
      ))}

      <button onClick={handleSubmit}>Ver resultado</button>

      {resultado && <div className="resultado"><h3>{resultado}</h3></div>}
    </div>
  );
}

export default Quiz;