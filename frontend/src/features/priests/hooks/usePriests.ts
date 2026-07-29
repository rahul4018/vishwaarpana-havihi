import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { priestService } from "../services/priest.service";

import type {
  CreatePriestRequest,
  UpdatePriestRequest,
} from "../types/priest.types";

export function usePriests() {
  return useQuery({
    queryKey: ["priests"],
    queryFn: priestService.getAll,
  });
}

export function usePriest(id: string) {
  return useQuery({
    queryKey: ["priests", id],
    queryFn: () => priestService.getById(id),
    enabled: !!id,
  });
}

export function useCreatePriest() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreatePriestRequest) =>
      priestService.create(data),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["priests"],
      });
    },
  });
}

export function useUpdatePriest() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: string;
      data: UpdatePriestRequest;
    }) => priestService.update(id, data),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["priests"],
      });

      queryClient.invalidateQueries({
        queryKey: ["priests", variables.id],
      });
    },
  });
}

export function useDeletePriest() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) =>
      priestService.delete(id),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["priests"],
      });
    },
  });
}