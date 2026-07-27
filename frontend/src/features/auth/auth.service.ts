import { api } from "@/services/api";

import type {
  LoginRequest,
  LoginResponse,
  RefreshResponse,
  RefreshTokenRequest,
  RegisterRequest,
  User,
} from "./auth.types";

const BASE_URL = "/auth";

export const authService = {
  register: async (data: RegisterRequest) => {
    const response = await api.post(`${BASE_URL}/register`, data);
    return response.data;
  },

  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>(
      `${BASE_URL}/login`,
      data
    );

    return response.data;
  },

  refresh: async (
    data: RefreshTokenRequest
  ): Promise<RefreshResponse> => {
    const response = await api.post<RefreshResponse>(
      `${BASE_URL}/refresh`,
      data
    );

    return response.data;
  },

  me: async (): Promise<User> => {
    const response = await api.get<User>(`${BASE_URL}/me`);
    return response.data;
  },
};