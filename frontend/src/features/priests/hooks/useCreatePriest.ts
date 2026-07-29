import { useMutation, useQueryClient } from "@tanstack/react-query";

import { priestService } from "../services/priest.service";
import type {
  CreatePriestRequest,
  Priest,
} from "../types/priest.types";

export function useCreatePriest() {
  const queryClient = useQueryClient();

  return useMutation<Priest, Error, CreatePriestRequest>({
    mutationFn: priestService.create,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["priests"],
      });
    },
  });
}