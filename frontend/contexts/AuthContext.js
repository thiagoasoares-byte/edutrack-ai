import React, { createContext, useContext, useState, useEffect } from 'react';
import Cookies from 'js-cookie';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const userData = Cookies.get('user');
    const token = Cookies.get('token');

    if (userData && token) {
      try {
        setUser(JSON.parse(userData));
      } catch (e) {
        console.error('Failed to parse user cookie', e);
      }
    }
    setLoading(false);
  }, []);

  const login = (userData, token) => {
    Cookies.set('user', JSON.stringify(userData), { expires: 1 });
    Cookies.set('token', token, { expires: 1 });
    setUser(userData);
  };

  const logout = () => {
    Cookies.remove('user');
    Cookies.remove('token');
    setUser(null);
    window.location.href = '/';
  };

  const value = {
    user,
    login,
    logout,
    isAuthenticated: !!user,
    loading
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};