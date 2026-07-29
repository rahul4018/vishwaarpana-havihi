import { useMutation, useQueryClient } from "@tanstack/react-query";

import { templeService } from "../services/temple.service";

export function useCreateTemple() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: templeService.create,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["temples"],
      });
    },
  });
}