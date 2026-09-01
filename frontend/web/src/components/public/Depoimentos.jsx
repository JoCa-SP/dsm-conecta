function Depoimentos() {
  const depoimentos = [
    { id: 1, nome: 'Ana Silva', texto: 'O curso me preparou para o mercado de trabalho com projetos práticos desde o primeiro semestre.' },
    { id: 2, nome: 'Carlos Souza', texto: 'Aprendi a trabalhar com metodologias ágeis e hoje atuo como Scrum Master em uma startup.' },
    { id: 3, nome: 'Mariana Costa', texto: 'As microcertificações me ajudaram a conseguir meu primeiro estágio ainda durante o curso.' },
    { id: 4, nome: 'João Pedro', texto: 'A infraestrutura da Fatec Zona Sul e os professores são diferenciais incríveis.' },
  ];

  return (
    <div className="depoimentos">
      <h1>🗣️ Depoimentos</h1>
      <p>O que nossos alunos e egressos dizem sobre o curso.</p>

      {depoimentos.map((dep) => (
        <div key={dep.id} className="depoimento-card">
          <p>"{dep.texto}"</p>
          <strong>- {dep.nome}</strong>
        </div>
      ))}
    </div>
  );
}

export default Depoimentos;