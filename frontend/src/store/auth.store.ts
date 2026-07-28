"use client";

import { create } from "zustand";

import type { User } from "@/features/auth/auth.types";
import { cookieStorage } from "@/utils/cookies";

interface AuthState {
  user: User | null;

  accessToken: string | null;
  refreshToken: string | null;

  isAuthenticated: boolean;

  setAuth: (
    user: User,
    accessToken: string,
    refreshToken: string
  ) => void;

  logout: () => void;

  loadFromStorage: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,

  accessToken: null,
  refreshToken: null,

  isAuthenticated: false,

  setAuth: (user, accessToken, refreshToken) => {
    cookieStorage.setAccessToken(accessToken);
    cookieStorage.setRefreshToken(refreshToken);

    localStorage.setItem("user", JSON.stringify(user));

    set({
      user,
      accessToken,
      refreshToken,
      isAuthenticated: true,
    });
  },

  logout: () => {
    cookieStorage.clear();
    localStorage.removeItem("user");

    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    });
  },

  loadFromStorage: () => {
    const accessToken = cookieStorage.getAccessToken();
    const refreshToken = cookieStorage.getRefreshToken();
    const user = localStorage.getItem("user");

    if (!accessToken || !refreshToken || !user) {
      return;
    }

    set({
      accessToken,
      refreshToken,
      user: JSON.parse(user),
      isAuthenticated: true,
    });
  },
}));