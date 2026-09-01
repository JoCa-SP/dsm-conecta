import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

// Layout
import Layout from './components/layout/Layout';

// Páginas Públicas
import Home from './components/public/Home';
import { Navigate } from 'react-router-dom';
import Projetos from './components/public/Projetos';
import Depoimentos from './components/public/Depoimentos';
import Agenda from './components/public/Agenda';
import Quiz from './components/public/Quiz';
import Presenca from './components/public/Presenca';
import Contato from './components/public/Contato';

// Páginas Administrativas
import Login from './components/admin/Login';
import Dashboard from './components/admin/Dashboard';

import './index.css';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Rotas com Layout (Header + Footer) */}
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="sobre" element={<Navigate to="/" replace />} />
            <Route path="projetos" element={<Projetos />} />
            <Route path="depoimentos" element={<Depoimentos />} />
            <Route path="agenda" element={<Agenda />} />
            <Route path="quiz" element={<Quiz />} />
            <Route path="presenca" element={<Presenca />} />
            <Route path="contato" element={<Contato />} />
            <Route path="admin" element={<Dashboard />} />
            <Route path="login" element={<Login />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;