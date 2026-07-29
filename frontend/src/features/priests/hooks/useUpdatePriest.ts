import { useMutation, useQueryClient } from "@tanstack/react-query";

import { priestService } from "../services/priest.service";
import type {
  Priest,
  UpdatePriestRequest,
} from "../types/priest.types";

interface UpdatePriestPayload {
  id: string;
  data: UpdatePriestRequest;
}

export function useUpdatePriest() {
  const queryClient = useQueryClient();

  return useMutation<
    Priest,
    Error,
    UpdatePriestPayload
  >({
    mutationFn: ({ id, data }) =>
      priestService.update(id, data),

    onSuccess: (updatedPriest, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["priests"],
      });

      queryClient.invalidateQueries({
        queryKey: ["priests", variables.id],
      });

      queryClient.setQueryData(
        ["priests", variables.id],
        updatedPriest
      );
    },
  });
}