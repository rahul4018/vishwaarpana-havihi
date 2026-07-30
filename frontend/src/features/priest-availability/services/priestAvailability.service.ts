import { api } from "@/services/api";

import type {
  PriestAvailability,
  CreatePriestAvailabilityRequest,
  UpdatePriestAvailabilityRequest,
} from "../types/priestAvailability.types";

export const priestAvailabilityService = {
  getAll: async (): Promise<PriestAvailability[]> => {
    const { data } = await api.get("/priest-availability");
    return data;
  },

  getById: async (
    id: string
  ): Promise<PriestAvailability> => {
    const { data } = await api.get(
      `/priest-availability/${id}`
    );

    return data;
  },

  getByPriest: async (
    priestId: string
  ): Promise<PriestAvailability[]> => {
    const { data } = await api.get(
      `/priest-availability/priest/${priestId}`
    );

    return data;
  },

  getByDate: async (
    date: string
  ): Promise<PriestAvailability[]> => {
    const { data } = await api.get(
      `/priest-availability/date/${date}`
    );

    return data;
  },

  create: async (
    payload: CreatePriestAvailabilityRequest
  ): Promise<PriestAvailability> => {
    const { data } = await api.post(
      "/priest-availability",
      payload
    );

    return data;
  },

  update: async (
    id: string,
    payload: UpdatePriestAvailabilityRequest
  ): Promise<PriestAvailability> => {
    const { data } = await api.put(
      `/priest-availability/${id}`,
      payload
    );

    return data;
  },

  delete: async (
    id: string
  ): Promise<void> => {
    await api.delete(`/priest-availability/${id}`);
  },
};