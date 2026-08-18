import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types/api';
import { authApi } from '../api/auth';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('rubber_stress_token'));
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchUser = async () => {
      if (token) {
        try {
          const u = await authApi.getMe();
          setUser(u);
        } catch {
          localStorage.removeItem('rubber_stress_token');
          setToken(null);
          setUser(null);
        }
      }
      setIsLoading(false);
    };
    fetchUser();
  }, [token]);

  const login = async (newToken: string) => {
    localStorage.setItem('rubber_stress_token', newToken);
    setToken(newToken);
    try {
      const u = await authApi.getMe();
      setUser(u);
    } catch (e) {
      console.error('Failed to load user profile after login:', e);
    }
  };

  const logout = () => {
    localStorage.removeItem('rubber_stress_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated: !!token, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
