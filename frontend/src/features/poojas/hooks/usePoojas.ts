import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { poojaService } from "../services/pooja.service";

import type {
  CreatePoojaRequest,
  UpdatePoojaRequest,
} from "../types/pooja.types";

export function usePoojas() {
  return useQuery({
    queryKey: ["poojas"],
    queryFn: poojaService.getAll,
  });
}

export function usePooja(id: string) {
  return useQuery({
    queryKey: ["poojas", id],
    queryFn: () => poojaService.getById(id),
    enabled: !!id,
  });
}

export function useCreatePooja() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreatePoojaRequest) =>
      poojaService.create(data),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["poojas"],
      });
    },
  });
}

export function useUpdatePooja() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: string;
      data: UpdatePoojaRequest;
    }) =>
      poojaService.update(id, data),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["poojas"],
      });

      queryClient.invalidateQueries({
        queryKey: ["poojas", variables.id],
      });
    },
  });
}

export function useDeletePooja() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) =>
      poojaService.delete(id),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["poojas"],
      });
    },
  });
}