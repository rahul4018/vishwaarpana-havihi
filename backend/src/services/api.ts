import axios, {
  AxiosError,
  AxiosInstance,
  InternalAxiosRequestConfig,
} from "axios";

import { cookieStorage } from "@/utils/cookies";

const api: AxiosInstance = axios.create({
  baseURL:
    process.env.NEXT_PUBLIC_API_URL ??
    "http://localhost:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: false,
});

// Attach access token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = cookieStorage.getAccessToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Handle expired access token
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    };

    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      const refreshToken = cookieStorage.getRefreshToken();

      if (!refreshToken) {
        cookieStorage.clear();

        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }

        return Promise.reject(error);
      }

      try {
        const response = await axios.post(
          `${
            process.env.NEXT_PUBLIC_API_URL ??
            "http://localhost:8000/api/v1"
          }/auth/refresh`,
          {
            refresh_token: refreshToken,
          }
        );

        const {
          access_token,
          refresh_token,
        } = response.data.tokens ?? response.data;

        cookieStorage.setAccessToken(access_token);

        if (refresh_token) {
          cookieStorage.setRefreshToken(refresh_token);
        }

        originalRequest.headers.Authorization = `Bearer ${access_token}`;

        return api(originalRequest);
      } catch {
        cookieStorage.clear();

        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }

        return Promise.reject(error);
      }
    }

    return Promise.reject(error);
  }
);

export default api;