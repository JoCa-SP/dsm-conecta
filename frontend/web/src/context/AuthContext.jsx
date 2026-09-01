import { createContext, useState, useContext } from 'react';
import { login as apiLogin } from '../api/endpoints';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await apiLogin({ email, password });
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      setUser({ email });
      return { success: true };
    } catch (error) {
      console.error('Erro no login:', error);
      return { success: false, error: error.response?.data?.detail || 'Erro ao fazer login' };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// ⚠️ ESSA É A FUNÇÃO QUE ESTAVA FALTANDO
export function useAuth() {
  return useContext(AuthContext);
}