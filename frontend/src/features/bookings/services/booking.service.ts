import { api } from "@/services/api";

import type {
  Booking,
  BookingListResponse,
  CreateBookingRequest,
  UpdateBookingRequest,
} from "../types/booking.types";

export const bookingService = {
  getAll: async (): Promise<BookingListResponse> => {
    const { data } = await api.get("/bookings");
    return data;
  },

  getById: async (
    id: string
  ): Promise<Booking> => {
    const { data } = await api.get(
      `/bookings/${id}`
    );

    return data;
  },

  create: async (
    payload: CreateBookingRequest
  ): Promise<Booking> => {
    const { data } = await api.post(
      "/bookings",
      payload
    );

    return data;
  },

  update: async (
    id: string,
    payload: UpdateBookingRequest
  ): Promise<Booking> => {
    const { data } = await api.put(
      `/bookings/${id}`,
      payload
    );

    return data;
  },

  delete: async (
    id: string
  ): Promise<void> => {
    await api.delete(`/bookings/${id}`);
  },
};