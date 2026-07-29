import { api } from "@/services/api";

import type {
  Priest,
  PriestListResponse,
  CreatePriestRequest,
  UpdatePriestRequest,
} from "../types/priest.types";

export const priestService = {
  getAll: async (): Promise<PriestListResponse> => {
    const { data } = await api.get("/priests");
    return data;
  },

  getById: async (
    id: string
  ): Promise<Priest> => {
    const { data } = await api.get(
      `/priests/${id}`
    );

    return data;
  },

  create: async (
    payload: CreatePriestRequest
  ): Promise<Priest> => {
    const { data } = await api.post(
      "/priests",
      payload
    );

    return data;
  },

  update: async (
    id: string,
    payload: UpdatePriestRequest
  ): Promise<Priest> => {
    const { data } = await api.put(
      `/priests/${id}`,
      payload
    );

    return data;
  },

  delete: async (
    id: string
  ): Promise<void> => {
    await api.delete(`/priests/${id}`);
  },
};