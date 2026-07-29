import { useMutation, useQueryClient } from "@tanstack/react-query";

import { templeService } from "../services/temple.service";
import type {
  Temple,
  UpdateTempleRequest,
} from "../types/temple.types";

interface UpdateTemplePayload {
  id: string;
  data: UpdateTempleRequest;
}

export function useUpdateTemple() {
  const queryClient = useQueryClient();

  return useMutation<
    Temple,
    Error,
    UpdateTemplePayload
  >({
    mutationFn: ({ id, data }) =>
      templeService.update(id, data),

    onSuccess: (updatedTemple, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["temples"],
      });

      queryClient.invalidateQueries({
        queryKey: ["temples", variables.id],
      });

      queryClient.setQueryData(
        ["temples", variables.id],
        updatedTemple
      );
    },
  });
}