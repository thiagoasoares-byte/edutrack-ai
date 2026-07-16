import axios from 'axios';
import Cookies from 'js-cookie';

// Base URL - matches the default from your original Streamlit app
const BASE_URL = process.env.NEXT_PUBLIC_XANO_URL ||
  "https://x8ki-letl-twmt.n7.xano.io/api";

// Group IDs matching your original Streamlit app
const GROUP_CANONICAL_IDS = {
  "auth": "yMJziCve",
  "subject": "yCLJBTsI",
  "academic_tasks": "academic_tasks"
};

// Construct the full group base URLs
const GROUPS = Object.fromEntries(
  Object.entries(GROUP_CANONICAL_IDS).map(([group, id]) => [
    group,
    `${BASE_URL}:${id}`
  ])
);

/**
 * Get headers with authentication token
 */
const getHeaders = () => {
  const token = Cookies.get('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
  };
};

/**
 * Handle API response - throw error on non-2xx status
 */
const handleResponse = async (response) => {
  if (!response.ok) {
    let errorMsg = 'Unknown error';
    try {
      const errorData = await response.json();
      errorMsg = errorData.message || errorData.error || errorMsg;
    } catch (e) {
      errorMsg = response.statusText || 'Unknown error';
    }
    throw new Error(errorMsg);
  }
  return response.json();
};

/**
 * GET request
 */
export const get = async (group, path, params = {}) => {
  const url = `${GROUPS[group]}${path}`;
  const queryString = new URLSearchParams(params).toString();
  const fullUrl = queryString ? `${url}?${queryString}` : url;

  const response = await fetch(fullUrl, {
    method: 'GET',
    headers: getHeaders(),
  });

  return await handleResponse(response);
};

/**
 * POST request
 */
export const post = async (group, path, data = {}) => {
  const url = `${GROUPS[group]}${path}`;

  const response = await fetch(url, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(data),
  });

  return await handleResponse(response);
};

/**
 * PATCH request
 */
export const patch = async (group, path, data = {}) => {
  const url = `${GROUPS[group]}${path}`;

  const response = await fetch(url, {
    method: 'PATCH',
    headers: getHeaders(),
    body: JSON.stringify(data),
  });

  return await handleResponse(response);
};

/**
 * DELETE request
 */
export const del = async (group, path, params = {}) => {
  const url = `${GROUPS[group]}${path}`;
  const queryString = new URLSearchParams(params).toString();
  const fullUrl = queryString ? `${url}?${queryString}` : url;

  const response = await fetch(fullUrl, {
    method: 'DELETE',
    headers: getHeaders(),
  });

  return await handleResponse(response);
};

export default { get, post, patch, del };