"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/store/auth.store";

export function AuthInitializer() {
  const loadFromStorage = useAuthStore((state) => state.loadFromStorage);

  useEffect(() => {
    loadFromStorage();
  }, [loadFromStorage]);

  return null;
}