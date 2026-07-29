import { useMutation, useQueryClient } from "@tanstack/react-query";

import { templeService } from "../services/temple.service";

export function useDeleteTemple() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => templeService.delete(id),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["temples"],
      });
    },
  });
}