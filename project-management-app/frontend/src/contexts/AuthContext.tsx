import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService } from '@/services/authService';
import { User } from '@/types/user';
import { Token } from '@/types/auth';

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: any) => Promise<void>; // Use specific type later e.g. UserCreate
  logout: () => void;
  isLoading: boolean; // To handle initial token/user loading state
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('accessToken'));
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const attemptLoadUser = async () => {
      const storedToken = localStorage.getItem('accessToken');
      if (storedToken) {
        setToken(storedToken);
        try {
          const currentUser = await authService.getCurrentUser(storedToken);
          setUser(currentUser);
        } catch (error) {
          console.error('Failed to fetch current user on load:', error);
          localStorage.removeItem('accessToken'); // Clear invalid token
          localStorage.removeItem('refreshToken');
          setToken(null);
          setUser(null);
        }
      }
      setIsLoading(false);
    };
    attemptLoadUser();
  }, []);

  const login = async (email: string, password: string) => {
    const tokenData = await authService.login(email, password);
    localStorage.setItem('accessToken', tokenData.access_token);
    if (tokenData.refresh_token) {
      localStorage.setItem('refreshToken', tokenData.refresh_token);
    }
    setToken(tokenData.access_token);
    const currentUser = await authService.getCurrentUser(tokenData.access_token);
    setUser(currentUser);
  };

  const register = async (userData: any) => { // Replace 'any' with UserCreate
    await authService.register(userData);
    // Optionally login user automatically after registration
    // await login(userData.email, userData.password);
    // For now, user will be redirected to login page after registration.
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setUser(null);
    setToken(null);
    // Navigate to login page will be handled by ProtectedRoute or in component
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated: !!token && !!user, user, token, login, register, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
