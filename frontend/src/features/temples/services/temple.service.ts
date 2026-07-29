import { api } from "@/services/api";

import type {
  Temple,
  TempleListResponse,
  CreateTempleRequest,
  UpdateTempleRequest,
} from "../types/temple.types";

export const templeService = {
  getAll: async (): Promise<TempleListResponse> => {
    const { data } = await api.get("/temples");
    return data;
  },

  getById: async (id: string): Promise<Temple> => {
    const { data } = await api.get(`/temples/${id}`);
    return data;
  },

  create: async (
    payload: CreateTempleRequest
  ): Promise<Temple> => {
    const { data } = await api.post(
      "/temples",
      payload
    );

    return data;
  },

  update: async (
    id: string,
    payload: UpdateTempleRequest
  ): Promise<Temple> => {
    const { data } = await api.put(
      `/temples/${id}`,
      payload
    );

    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/temples/${id}`);
  },
};