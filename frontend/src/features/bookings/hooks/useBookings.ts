import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { bookingService } from "../services/booking.service";

import type {
  CreateBookingRequest,
  UpdateBookingRequest,
} from "../types/booking.types";

export function useBookings() {
  return useQuery({
    queryKey: ["bookings"],
    queryFn: bookingService.getAll,
  });
}

export function useBooking(id: string) {
  return useQuery({
    queryKey: ["bookings", id],
    queryFn: () => bookingService.getById(id),
    enabled: !!id,
  });
}

export function useCreateBooking() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateBookingRequest) =>
      bookingService.create(data),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["bookings"],
      });
    },
  });
}

export function useUpdateBooking() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: string;
      data: UpdateBookingRequest;
    }) =>
      bookingService.update(id, data),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["bookings"],
      });

      queryClient.invalidateQueries({
        queryKey: ["bookings", variables.id],
      });
    },
  });
}

export function useDeleteBooking() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) =>
      bookingService.delete(id),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["bookings"],
      });
    },
  });
}