import Cookies from 'js-cookie';
import { post } from './api';

/**
 * Check if user is logged in
 */
export const isLoggedIn = () => {
  return !!Cookies.get('token');
};

/**
 * Login user
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise<Object>} User data and token
 */
export const login = async (email, password) => {
  const data = await post('auth', '/login', { email, password });

  // Store token and user in cookies
  Cookies.set('token', data.auth_token, { expires: 1 });
  Cookies.set('user', JSON.stringify(data.user), { expires: 1 });

  return data.user;
};

/**
 * Sign up new user
 * @param {string} name - User name
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise<Object>} User data and token
 */
export const signup = async (name, email, password) => {
  const data = await post('auth', '/signup', { name, email, password });

  // Store token and user in cookies
  Cookies.set('token', data.auth_token, { expires: 1 });
  Cookies.set('user', JSON.stringify(data.user), { expires: 1 });

  return data.user;
};

/**
 * Logout user
 */
export const logout = () => {
  Cookies.remove('token');
  Cookies.remove('user');
  window.location.href = '/';
};

/**
 * Get current user from cookies
 */
export const getCurrentUser = () => {
  const userJson = Cookies.get('user');
  if (!userJson) return null;

  try {
    return JSON.parse(userJson);
  } catch (e) {
    console.error('Failed to parse user cookie', e);
    return null;
  }
};

/**
 * Update user profile
 * @param {Object} userData - User data to update
 * @returns {Promise<Object>} Updated user data
 */
export const updateProfile = async (userData) => {
  const data = await patch('auth', '/update_profile', userData);

  // Update user cookie
  Cookies.set('user', JSON.stringify(data), { expires: 1 });

  return data;
};

export default {
  isLoggedIn,
  login,
  signup,
  logout,
  getCurrentUser,
  updateProfile
};