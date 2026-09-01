import { Link } from 'react-router-dom';

function Header() {
  return (
    <nav className="navbar">
      <div className="nav-left">
        <Link to="/" className="brand">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z" />
            <path d="M2 17l10 5 10-5" />
            <path d="M2 12l10 5 10-5" />
          </svg>
          DSM Conecta
        </Link>
      </div>
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/projetos">Projetos</Link>
        <Link to="/depoimentos">Depoimentos</Link>
        <Link to="/agenda">Agenda</Link>
        <Link to="/quiz">Quiz</Link>
        <Link to="/presenca">Presença</Link>
        <Link to="/contato">Contato</Link>
        <Link to="/admin" className="admin-link">Admin</Link>
      </div>
    </nav>
  );
}

export default Header;