"use client";

import { useMutation, useQuery } from "@tanstack/react-query";

import { authService } from "./auth.service";
import { useAuthStore } from "./auth.store";
import type { LoginRequest } from "./auth.types";

export function useLogin() {
  const setAuth = useAuthStore((state) => state.setAuth);

  return useMutation({
    mutationFn: (data: LoginRequest) => authService.login(data),

    onSuccess: (response) => {
      setAuth({
        user: response.user,
        accessToken: response.tokens.access_token,
        refreshToken: response.tokens.refresh_token,
      });
    },
  });
}

export function useCurrentUser(enabled = true) {
  return useQuery({
    queryKey: ["me"],
    queryFn: authService.me,
    enabled,
    retry: false,
  });
}