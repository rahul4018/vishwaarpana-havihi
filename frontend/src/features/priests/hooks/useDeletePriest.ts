import { useMutation, useQueryClient } from "@tanstack/react-query";

import { priestService } from "../services/priest.service";

export function useDeletePriest() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: priestService.delete,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["priests"],
      });
    },
  });
}