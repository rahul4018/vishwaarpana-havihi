import { api } from "@/services/api";

import type {
  Pooja,
  PoojaListResponse,
  CreatePoojaRequest,
  UpdatePoojaRequest,
} from "../types/pooja.types";

export const poojaService = {
  getAll: async (): Promise<PoojaListResponse> => {
    const { data } = await api.get("/poojas");
    return data;
  },

  getById: async (
    id: string
  ): Promise<Pooja> => {
    const { data } = await api.get(
      `/poojas/${id}`
    );

    return data;
  },

  create: async (
    payload: CreatePoojaRequest
  ): Promise<Pooja> => {
    const { data } = await api.post(
      "/poojas",
      payload
    );

    return data;
  },

  update: async (
    id: string,
    payload: UpdatePoojaRequest
  ): Promise<Pooja> => {
    const { data } = await api.put(
      `/poojas/${id}`,
      payload
    );

    return data;
  },

  delete: async (
    id: string
  ): Promise<void> => {
    await api.delete(`/poojas/${id}`);
  },
};