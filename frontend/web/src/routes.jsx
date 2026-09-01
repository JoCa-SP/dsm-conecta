import { createBrowserRouter } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Home from './components/public/Home';
import Sobre from './components/public/Sobre';
import Projetos from './components/public/Projetos';
import Depoimentos from './components/public/Depoimentos';
import Agenda from './components/public/Agenda';
import Quiz from './components/public/Quiz';
import Presenca from './components/public/Presenca';
import Contato from './components/public/Contato';
import Login from './components/admin/Login';
import Dashboard from './components/admin/Dashboard';
import ProtectedRoute from './components/admin/ProtectedRoute';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'sobre', element: <Sobre /> },
      { path: 'projetos', element: <Projetos /> },
      { path: 'depoimentos', element: <Depoimentos /> },
      { path: 'agenda', element: <Agenda /> },
      { path: 'quiz', element: <Quiz /> },
      { path: 'presenca', element: <Presenca /> },
      { path: 'contato', element: <Contato /> },
      { path: 'login', element: <Login /> },
      {
        path: 'admin',
        element: <ProtectedRoute />,
        children: [
          { index: true, element: <Dashboard /> },
          { path: 'conteudo', element: <ConteudoList /> },
          { path: 'conteudo/novo', element: <ConteudoForm /> },
          // ... outras rotas admin
        ],
      },
    ],
  },
]);

export default router;