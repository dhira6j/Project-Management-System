import { User, UserCreate } from '@/types/user'; // Assuming type definitions exist or will be created
import { Token } from '@/types/auth';     // Assuming type definitions

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Helper to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Unknown error occurred' }));
    throw new Error(errorData.detail || "API request failed");
  }
  return response.json();
}

export const authService = {
  login: async (email: string, password: string): Promise<Token> => {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: email, password: password }),
    });
    return handleResponse<Token>(response);
  },

  register: async (userData: UserCreate): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    return handleResponse<User>(response);
  },

  getCurrentUser: async (token: string): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/api/v1/users/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse<User>(response);
  },

  // refreshToken: async (refreshToken: string): Promise<Token> => {
  //   // The backend /refresh endpoint expects refresh_token_str as a direct body string or specific param
  //   // Adjust this if backend expects JSON or form data for refresh token
  //   const response = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' }, // Or 'text/plain' if backend expects raw string
  //     body: JSON.stringify({ refresh_token_str: refreshToken }) // Assuming backend expects JSON now
  //   });
  //   return handleResponse<Token>(response);
  // }
};

// Basic types (can be moved to a types/ directory)
// types/user.ts
// export interface User { id: number; email: string; full_name?: string; role: string; is_active: boolean; is_verified: boolean; }
// export interface UserCreate { email: string; password: string; full_name?: string; role?: string;}

// types/auth.ts
// export interface Token { access_token: string; refresh_token?: string; token_type: string; }
