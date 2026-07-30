import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { priestAvailabilityService } from "../services/priestAvailability.service";

import type {
  CreatePriestAvailabilityRequest,
  UpdatePriestAvailabilityRequest,
} from "../types/priestAvailability.types";

export function usePriestAvailability() {
  return useQuery({
    queryKey: ["priest-availability"],
    queryFn: priestAvailabilityService.getAll,
  });
}

export function usePriestAvailabilityById(
  id: string
) {
  return useQuery({
    queryKey: ["priest-availability", id],
    queryFn: () =>
      priestAvailabilityService.getById(id),
    enabled: !!id,
  });
}

export function usePriestAvailabilityByPriest(
  priestId: string
) {
  return useQuery({
    queryKey: [
      "priest-availability",
      "priest",
      priestId,
    ],
    queryFn: () =>
      priestAvailabilityService.getByPriest(
        priestId
      ),
    enabled: !!priestId,
  });
}

export function usePriestAvailabilityByDate(
  availableDate: string
) {
  return useQuery({
    queryKey: [
      "priest-availability",
      "date",
      availableDate,
    ],
    queryFn: () =>
      priestAvailabilityService.getByDate(
        availableDate
      ),
    enabled: !!availableDate,
  });
}

export function useCreatePriestAvailability() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (
      data: CreatePriestAvailabilityRequest
    ) =>
      priestAvailabilityService.create(data),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["priest-availability"],
      });
    },
  });
}

export function useUpdatePriestAvailability() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: string;
      data: UpdatePriestAvailabilityRequest;
    }) =>
      priestAvailabilityService.update(
        id,
        data
      ),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["priest-availability"],
      });

      queryClient.invalidateQueries({
        queryKey: [
          "priest-availability",
          variables.id,
        ],
      });
    },
  });
}

export function useDeletePriestAvailability() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) =>
      priestAvailabilityService.delete(id),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["priest-availability"],
      });
    },
  });
}