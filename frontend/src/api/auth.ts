import client from './client';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export const authAPI = {
  login: (data: LoginRequest) =>
    client.post<AuthResponse>('/auth/token', new URLSearchParams({
      username: data.email,
      password: data.password,
    }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }),

  register: (data: RegisterRequest) =>
    client.post<AuthResponse>('/auth/register', data),

  getCurrentUser: () =>
    client.get('/auth/me'),
};
